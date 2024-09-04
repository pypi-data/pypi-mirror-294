import sys
import threading
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional, Union

from ._internal import worker_queue
from .client import Client, HudClientException, get_client
from .collectors import PerformanceMonitor, get_loaded_modules, runtime_info
from .config import config
from .declarations import Declaration, DeclarationsAggregator
from .exception_handler import FatalErrorData
from .hook import set_hook
from .logging import internal_logger, send_logs_handler
from .native import (
    check_marked_code,
    get_and_swap_aggregations,
)
from .run_mode import disable_hud, should_run_hud
from .schemas.events import Caller, Invocations, Sketch, WorkloadData
from .schemas.requests import Logs
from .utils import supress_exceptions
from .workload_metadata import get_cpu_limit, get_workload_metadata

if TYPE_CHECKING:
    from collections import deque  # noqa: F401
    from typing import Any  # noqa: F401
worker_thread = None  # type: Optional[threading.Thread]


@supress_exceptions(default_return_value=None)
def handle_item(
    item: Union[Declaration, Logs],
    declarations: DeclarationsAggregator,
    client: Client,
) -> None:
    if isinstance(item, Declaration):
        declarations.add_declaration(item)
    elif isinstance(item, Logs):
        client.send_logs(item)
    else:
        internal_logger.warning("Invalid item type: {}".format(type(item)))


def _get_and_clear_invocations(interval: int) -> List[Invocations]:
    invocations_c = get_and_swap_aggregations()
    if not invocations_c:
        return []
    invocations = [
        Invocations(
            count=invocation.total_calls,
            function_id=invocation.function_id,
            sampled_count=invocation.total_calls,
            sum_duration=invocation.total_time,
            sum_squared_duration=invocation.total_squared_time,
            timeslice=interval,
            timestamp=datetime.now(timezone.utc),
            callers=[
                Caller(
                    name=c.co_name,
                    file_name=c.co_filename,
                    start_line=c.co_firstlineno,
                    is_wrapped=check_marked_code(c),
                )
                for c in invocation.callers
                if c
            ],
            exceptions=invocation.exceptions,
            sketch=(
                Sketch(
                    bin_width=invocation.sketch_data.bin_width,
                    index_shift=invocation.sketch_data.index_shift,
                    data=invocation.sketch_data.data,
                )
                if invocation.sketch_data
                else Sketch(bin_width=0, index_shift=0, data=[])
            ),
        )
        for invocation in invocations_c.values()
    ]
    invocations_c.clear()
    return invocations


@supress_exceptions(default_return_value=None)
def _dump_invocations(client: Client, interval: int) -> None:
    invocations = _get_and_clear_invocations(interval)
    if invocations:
        client.send_invocations(invocations)


@supress_exceptions(default_return_value=None)
def _dump_declarations(declarations: DeclarationsAggregator, client: Client) -> None:
    latest_declarations = declarations.get_declarations()
    declarations.clear()
    if len(latest_declarations) > 0:
        client.send_declarations(latest_declarations)


@supress_exceptions(default_return_value=None)
def _send_workload_data(client: Client, workload_metadata: WorkloadData) -> None:
    client.send_workload_data(workload_metadata)


@supress_exceptions(default_return_value=None)
def _send_loaded_modules(client: Client) -> None:
    modules = get_loaded_modules()
    client.send_modules(modules)


@supress_exceptions(default_return_value=None)
def _send_performance(client: Client, perf_monitor: PerformanceMonitor) -> None:
    performance = perf_monitor.monitor_process()
    if config.log_performance:
        internal_logger.info("performance data", data=performance.to_json_data())
    client.send_performace(performance)


@supress_exceptions(default_return_value=None)
def _send_runtime(client: Client) -> None:
    runtime = runtime_info()
    client.send_runtime(runtime)


@supress_exceptions(default_return_value=None)
def _dump_logs(client: Client) -> None:
    logs = send_logs_handler.get_and_clear_logs()
    if len(logs.logs) == 0:
        return
    client.send_logs(logs)


def should_finalize_worker(worker_thread: threading.Thread) -> bool:
    for thread in threading.enumerate():
        if thread == worker_thread:
            continue
        if thread.daemon is False and thread.is_alive():
            return False
    return True


def process_queue(
    worker_queue,  # type: deque[Any]
    declarations: DeclarationsAggregator,
    client: Client,
) -> None:
    qsize = len(worker_queue)
    if hasattr(worker_queue, "maxlen") and worker_queue.maxlen == qsize:
        internal_logger.warning("Event queue is full")
    try:
        for item in iter(worker_queue.popleft, None):
            handle_item(item, declarations, client)
            qsize -= 1
            if qsize == 0:
                break
    except IndexError:
        pass


def init_hud_thread(key: Optional[str] = None, service: Optional[str] = None) -> None:
    set_hook()  # We enforce the hook to be set before starting the worker thread

    # Create new thread
    global worker_thread
    if worker_thread is not None and worker_thread.is_alive():
        internal_logger.info("Worker thread is already running")
        return

    if not should_run_hud():
        disable_hud()
        return

    def _target() -> None:
        internal_logger.info("Starting worker thread")

        try:
            client = get_client(key, service)
            client.init_session()
        except Exception as e:
            disable_hud()
            if not isinstance(e, HudClientException):
                internal_logger.exception("Failed to initialize client")
            return None

        pod_cpu_limit = get_cpu_limit()
        workload_metadata = get_workload_metadata(pod_cpu_limit)
        _send_workload_data(client, workload_metadata)
        _send_runtime(client)
        _send_loaded_modules(client)

        declarations = DeclarationsAggregator()
        perf_monitor = PerformanceMonitor(pod_cpu_limit)

        tick_count = 0
        last_invocations_dump = time.time()
        while True:
            if not should_run_hud():
                disable_hud()
                break

            if worker_thread and should_finalize_worker(worker_thread):
                process_queue(worker_queue, declarations, client)
                _dump_declarations(declarations, client)

                invocations_slice = int(time.time() - last_invocations_dump)
                last_invocations_dump = time.time()
                _dump_invocations(client, invocations_slice)

                _dump_logs(client)
                _send_workload_data(client, workload_metadata)
                break

            process_queue(worker_queue, declarations, client)
            tick_count += 1

            if tick_count % config.declarations_flush_interval == 0:
                _dump_declarations(declarations, client)
            if tick_count % config.invocations_flush_interval == 0:
                invocations_slice = int(time.time() - last_invocations_dump)
                last_invocations_dump = time.time()
                _dump_invocations(client, invocations_slice)
            if tick_count % config.logs_flush_interval == 0:
                _dump_logs(client)
            if tick_count % config.workload_data_flush_interval == 0:
                _send_workload_data(client, workload_metadata)
            if tick_count % config.modules_report_interval == 0:
                _send_loaded_modules(client)
            if tick_count % config.performace_report_interval == 0:
                _send_performance(client, perf_monitor)
            time.sleep(1)

    def target() -> None:
        try:
            _target()
        except Exception as e:
            try:
                disable_hud()
                internal_logger.exception(
                    "Exception in worker thread target: {}".format(e)
                )
                client = get_client(key, service)
                exc_type, exc_value, exc_traceback = sys.exc_info()
                fatal_error = FatalErrorData(
                    exc_type=exc_type,
                    exc_value=exc_value,
                    exc_traceback=exc_traceback,
                )
                client.send_fatal_error(fatal_error)
            except Exception as err:
                internal_logger.exception("Failed to send fatal error: {}".format(err))

    worker_thread = threading.Thread(target=target)
    worker_thread.start()
