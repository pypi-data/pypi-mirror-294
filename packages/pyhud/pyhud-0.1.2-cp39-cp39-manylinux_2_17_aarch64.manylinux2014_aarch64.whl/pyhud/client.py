import json
import os
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any, List, Optional, Sequence

import requests
from requests.adapters import HTTPAdapter, Retry

from . import version as hud_version
from .config import config
from .logging import internal_logger
from .schemas.events import (
    Event,
    FunctionDeclaration,
    Invocations,
    LoadedModules,
    Performance,
    Runtime,
    WorkloadData,
)
from .schemas.requests import (
    Batch as BatchRequest,
)
from .schemas.requests import (
    FatalError as FatalErrorRequest,
)
from .schemas.requests import (
    Init as InitRequest,
)
from .schemas.requests import (
    Logs as LogsRequest,
)
from .schemas.requests import (
    Send as SendRequest,
)

if TYPE_CHECKING:
    # We need it to avoid circular imports
    from .exception_handler import FatalErrorData


class HudClientException(Exception):
    pass


class SendDataError(HudClientException):
    pass


class Client(ABC):
    @abstractmethod
    def init_session(self) -> None:
        pass

    @abstractmethod
    def send_invocations(self, invocations: List[Invocations]) -> None:
        pass

    @abstractmethod
    def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        pass

    @abstractmethod
    def send_logs(self, logs: LogsRequest) -> None:
        pass

    @abstractmethod
    def send_workload_data(self, data: WorkloadData) -> None:
        pass

    @abstractmethod
    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        pass

    @abstractmethod
    def send_runtime(self, data: Runtime) -> None:
        pass

    @abstractmethod
    def send_performace(self, data: Performance) -> None:
        pass

    @abstractmethod
    def send_modules(self, modules: LoadedModules) -> None:
        pass


class ConsoleClient(Client):
    def init_session(self) -> None:
        print("init_session")

    def send_invocations(self, invocations: List[Invocations]) -> None:
        print("send_invocations for {} invocations".format(len(invocations)))
        for invocation in invocations:
            print(invocation.to_json_data())

    def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        print("send_declarations for {} declarations".format(len(declarations)))
        for declaration in declarations:
            print(declaration.to_json_data())

    def send_logs(self, logs: LogsRequest) -> None:
        print("send_logs for {} logs".format(len(logs.logs)))
        for log in logs.logs:
            print({"log": log.to_json_data()})

    def send_workload_data(self, data: WorkloadData) -> None:
        print("send_workload_data: {}".format(data.to_json_data()))

    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        fatal_error_request = FatalErrorRequest(
            fatal_error,
            send_time=datetime.now(timezone.utc),
        )
        print("send_fatal_error: {}".format(fatal_error_request.to_json_data()))

    def send_runtime(self, data: Runtime) -> None:
        print("send_runtime: {}".format(data.to_json_data()))

    def send_performace(self, data: Performance) -> None:
        print("send_performance: {}".format(data.to_json_data()))

    def send_modules(self, modules: LoadedModules) -> None:
        print("send_modules: {}".format(modules.to_json_data()))


class JSONClient(Client):
    def __init__(self, path: str) -> None:
        self.path = path

    def _write_to_json(self, data: Any) -> None:
        with open(self.path, mode="a") as file:
            file.write(json.dumps(data) + "\n")

    def init_session(self) -> None:
        self._write_to_json({"type": "init_session"})

    def send_invocations(self, invocations: List[Invocations]) -> None:
        for invocation in invocations:
            self._write_to_json({"type": "invocation", **invocation.to_json_data()})

    def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        for declaration in declarations:
            self._write_to_json({"type": "declaration", **declaration.to_json_data()})

    def send_logs(self, logs: LogsRequest) -> None:
        for log in logs.logs:
            self._write_to_json({"type": "log", **log.to_json_data()})

    def send_workload_data(self, data: WorkloadData) -> None:
        self._write_to_json({"type": "workload_data", **data.to_json_data()})

    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        fatal_error_request = FatalErrorRequest(
            fatal_error, send_time=datetime.now(timezone.utc)
        )
        self._write_to_json(
            {"type": "fatal_error", **fatal_error_request.to_json_data()}
        )

    def send_runtime(self, data: Runtime) -> None:
        self._write_to_json({"type": "runtime", **data.to_json_data()})

    def send_performace(self, data: Performance) -> None:
        self._write_to_json({"type": "performance", **data.to_json_data()})

    def send_modules(self, modules: LoadedModules) -> None:
        self._write_to_json({"type": "modules", **modules.to_json_data()})


class HttpClient(Client):
    source = "python-sdk"

    def __init__(self, host: str, api_key: str, service: str) -> None:
        self.host = host
        self.api_key = api_key
        self.service = service
        self.session = requests.session()
        self.session.mount(
            self.host,
            HTTPAdapter(
                max_retries=Retry(
                    total=config.api_max_retries,
                    backoff_factor=config.api_backoff_factor,
                    status_forcelist=[429, 500, 502, 503, 504],
                )
            ),
        )
        self.session_id = None  # type: Optional[str]

    def _http_send(self, uri: str, request: Any, request_type: str) -> Any:
        try:
            with self.session.post(
                "{}/{}".format(self.host, uri),
                json=request,
            ) as res:
                res.raise_for_status()
                return res.json()
        except Exception as e:
            internal_logger.error("Failed to send {}".format(request_type))
            raise SendDataError("Failed to send {}".format(request_type)) from e

    def _set_session_id(self, session_id: str) -> None:
        internal_logger.info("Setting session_id: {}".format(session_id))

        self.session_id = session_id
        self.session.headers["X-Session-ID"] = session_id

    def init_session(self) -> None:
        internal_logger.debug(
            "Initializing session for service: {}".format(self.service)
        )
        request = InitRequest(
            token=self.api_key,
            service=self.service,
            start_time=datetime.now(timezone.utc),
            type=self.source,
            sdk_version=hud_version,
        )
        res = self._http_send("sink/init", request.to_json_data(), "Init")

        session_id = res["sessionId"]
        self._set_session_id(session_id)

    def _send_batch(self, arr: Sequence[Event]) -> None:
        size = config.batch_size
        for i in range(0, len(arr), size):
            request = BatchRequest(
                arr=[i.to_json_data() for i in arr[i : i + size]],
                event_version=arr[0].get_version(),
                send_time=datetime.now(timezone.utc),
                source=self.source,
                type=arr[0].get_type(),
            )
            self._http_send("sink/batch", request.to_json_data(), arr[0].get_type())

    def _send_single(self, event: Event) -> None:
        request = SendRequest(
            event_version=event.get_version(),
            send_time=datetime.now(timezone.utc),
            source=self.source,
            type=event.get_type(),
            raw=event.to_json_data(),
        )
        self._http_send("sink/send", request.to_json_data(), event.get_type())

    def send_invocations(self, invocations: List[Invocations]) -> None:
        internal_logger.info(
            "Sending invocations for {} invocations".format(len(invocations))
        )
        self._send_batch(invocations)

    def send_declarations(self, declarations: List[FunctionDeclaration]) -> None:
        internal_logger.info(
            "Sending declarations for {} declarations".format(len(declarations))
        )
        self._send_batch(declarations)

    def send_logs(self, logs: LogsRequest) -> None:
        self._http_send("sink/logs", logs.to_json_data(), "Logs")

    def send_workload_data(self, data: WorkloadData) -> None:
        internal_logger.info("Sending workload data")
        self._send_single(data)

    def send_runtime(self, data: Runtime) -> None:
        internal_logger.info("Sending runtime data")
        self._send_single(data)

    def send_performace(self, data: Performance) -> None:
        internal_logger.info("Sending performance data")
        self._send_single(data)

    def send_modules(self, modules: LoadedModules) -> None:
        internal_logger.info("Sending modules data")
        self._send_single(modules)

    def send_fatal_error(self, fatal_error: "FatalErrorData") -> None:
        request = FatalErrorRequest(
            fatal_error,
            send_time=datetime.now(timezone.utc),
            token=self.api_key,
            service=self.service,
        )
        self._http_send("sink/redline", request.to_json_data(), "FatalError")


def get_client(key: Optional[str] = None, service: Optional[str] = None) -> Client:
    client_type = config.client_type
    if client_type == "console":
        return ConsoleClient()
    if client_type == "json":
        return JSONClient(config.json_path)
    if client_type == "http":
        host = config.host
        key = key or os.environ.get("HUD_KEY", None)
        service = service or os.environ.get("HUD_SERVICE", None)

        if not host:
            internal_logger.warning("HUD_HOST is not set")
            raise HudClientException("HUD_HOST is not set")
        if not key:
            internal_logger.warning("HUD_KEY is not set")
            raise HudClientException("HUD_KEY is not set")
        if not service:
            internal_logger.warning("HUD_SERVICE is not set")
            raise HudClientException("HUD_SERVICE is not set")

        return HttpClient(host, key, service)

    raise HudClientException("Unknown client type: {}".format(client_type))
