import ast
import os
import sys
from contextlib import contextmanager
from hashlib import sha1
from importlib.abc import Loader, PathEntryFinder
from importlib.machinery import FileFinder, ModuleSpec, SourceFileLoader
from random import randint
from types import CodeType
from typing import Any, Generator, List, Mapping, Optional, Tuple, Type, Union, cast
from uuid import uuid4

from pyhud.native import set_hud_running_mode
from pyhud.schemas.events import ScopeNode, ScopeType

from ._internal import worker_queue
from .config import config
from .declarations import Declaration
from .exception_handler import install_exception_handler
from .logging import internal_logger
from .run_mode import should_run_hud

paths_to_wrap = [
    os.getcwd(),
]  # type: List[str]


file_path = getattr(sys.modules["__main__"], "__file__", None)
if file_path:
    paths_to_wrap.append(os.path.dirname(os.path.abspath(file_path)))


class ASTTransformer(ast.NodeTransformer):
    def __init__(self, path: str, lines: List[bytes]) -> None:
        self.path = path
        self.lines = lines
        self.compiler_flags = 0
        self.scope = []  # type: List[ScopeNode]

    def get_function_source_code_hash(self, node: Union[ast.stmt, ast.expr]) -> str:
        if (sys.version_info.major, sys.version_info.minor) < (3, 8):
            return sha1(ast.dump(node).encode()).hexdigest()
        else:
            start_line = node.lineno - 1
            end_line = cast(int, node.end_lineno) - 1
            source_code = b"\n".join(self.lines[start_line : end_line + 1])
            return sha1(source_code).hexdigest()

    @staticmethod
    def get_and_remove_docstring(
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> Optional[ast.stmt]:
        """
        If the first expression in the function is a literal string (docstring), remove it and return it
        """
        if not node.body:
            return None
        if (
            isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            return node.body.pop(0)
        return None

    @contextmanager
    def scope_manager(
        self, node: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]
    ) -> Generator[None, None, None]:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            scope_type = ScopeType.FUNCTION
        elif isinstance(node, ast.ClassDef):
            scope_type = ScopeType.CLASS
        else:
            try:
                yield
            finally:
                return

        self.scope.append(ScopeNode(scope_type, node.name))
        try:
            yield
        finally:
            self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        source_code_hash = self.get_function_source_code_hash(node)
        function_id = uuid4()

        worker_queue.append(
            Declaration.from_function_node(
                function_id,
                node,
                source_code_hash,
                self.path,
                is_async=False,
                scope=self.scope[:],
            )
        )

        with self.scope_manager(node):
            node.args = self.visit(node.args)
            stmts = ast.parse(
                'with HudContextManager("{}"):\n    pass'.format(function_id)
            ).body  # type: List[ast.stmt]

            docstring = self.get_and_remove_docstring(node)

            with_stmt = cast(ast.With, stmts[-1])
            with_stmt.body = [self.visit(stmt) for stmt in node.body]

            node.body = [*stmts]

            if docstring is not None:
                node.body.insert(0, docstring)

            node.decorator_list = [
                self.visit(decorator) for decorator in node.decorator_list
            ]

        return node

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        source_code_hash = self.get_function_source_code_hash(node)
        function_id = uuid4()
        worker_queue.append(
            Declaration.from_function_node(
                function_id,
                node,
                source_code_hash,
                self.path,
                is_async=True,
                scope=self.scope[:],
            )
        )

        with self.scope_manager(node):
            node.args = self.visit(node.args)
            with_stmt = cast(
                ast.With,
                ast.parse(
                    'with HudContextManager("{}"):\n    pass'.format(function_id)
                ).body[0],
            )  # type: ast.With

            docstring = self.get_and_remove_docstring(node)

            with_stmt.body = [self.visit(stmt) for stmt in node.body]

            node.body = [with_stmt]

            if docstring is not None:
                node.body.insert(0, docstring)

            node.decorator_list = [
                self.visit(decorator) for decorator in node.decorator_list
            ]
        return node

    def visit_Lambda(self, node: ast.Lambda) -> ast.Lambda:
        node.args = self.visit(node.args)
        node.body = self.visit(node.body)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        source_code_hash = self.get_function_source_code_hash(node)
        class_id = uuid4()
        worker_queue.append(
            Declaration.from_class_node(
                class_id, node, source_code_hash, self.path, scope=self.scope[:]
            )
        )
        with self.scope_manager(node):
            return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        # When passing an AST to the `compile` function, the `__future__` imports are not parsed
        # and the compiler flags are not set. This is a workaround to set the compiler flags,
        # and removing the invalid imports.
        if node.module == "__future__":
            import __future__

            for name in node.names:
                feature = getattr(__future__, name.name)
                self.compiler_flags |= feature.compiler_flag
            return None
        return self.generic_visit(node)


def should_wrap_file(path: str) -> bool:
    return path in paths_to_wrap


def should_wrap_module(fullname: str) -> bool:
    if fullname in config.modules_to_trace:
        return True
    for module in config.modules_to_trace:
        if fullname.startswith("{}.".format(module)):
            return True
    return False


class MyFileFinder(FileFinder):
    def __repr__(self) -> str:
        return "MyFileFinder('{}')".format(self.path)

    def __init__(
        self,
        path: str,
        *loader_details: Tuple[Type[Loader], List[str]],
        override: bool = False
    ) -> None:
        if not should_wrap_file(os.path.abspath(path)) and not override:
            raise ImportError("Not wrapping path: {}".format(path))

        super().__init__(path, *loader_details)

    def find_spec(self, fullname: str, *args: Any) -> Optional[ModuleSpec]:
        spec = super().find_spec(fullname, *args)
        if spec is not None and spec.submodule_search_locations is not None:
            paths_to_wrap.extend(spec.submodule_search_locations)
        return spec


class ModuleFinder(MyFileFinder):

    def __init__(self, path: str, original_finder: PathEntryFinder) -> None:
        self.path = path
        self.original_finder = original_finder

        if hasattr(original_finder, "_loaders"):
            suffixes = [loader[0] for loader in original_finder._loaders]
        else:
            raise ImportError("Original finder unsupported for path {}".format(path))

        if ".py" not in suffixes:
            raise ImportError("Not wrapping loader that doesn't handle .py files")

        loader_details = []

        if set(suffixes) == {".py"}:
            loader_details.append((MySourceLoader, [".py"]))
        else:
            for suffix, loader in original_finder._loaders:
                if suffix == ".py":
                    loader_details.append((MySourceLoader, [suffix]))
                else:
                    loader_details.append((loader, [suffix]))

        super().__init__(path, *loader_details, override=True)

    def __repr__(self) -> str:
        return "ModuleFinder('{}', original_finder={})".format(
            self.path, self.original_finder
        )

    def find_spec(self, fullname: str, *args: Any) -> Optional[ModuleSpec]:
        spec = None
        if should_wrap_module(fullname):
            spec = super().find_spec(fullname, *args)
        if spec is not None:
            if spec.origin is not None and spec.origin not in paths_to_wrap:
                paths_to_wrap.append(os.path.dirname(spec.origin))
            return spec
        if self.original_finder is not None:
            return self.original_finder.find_spec(fullname, *args)


class MySourceLoader(SourceFileLoader):
    def path_stats(self, path: str) -> Mapping[str, Any]:
        if not path.endswith(".py"):
            return super().path_stats(path)
        stats = super().path_stats(path)
        stats["mtime"] -= randint(  # type: ignore[index]
            1, 500
        )  # This manipulation allows bytecode caching to work for the edited module, without conflicting with the original module
        return stats

    def source_to_code(  # type: ignore[override]
        self, data: bytes, path: str, *, _optimize: int = -1
    ) -> CodeType:
        try:
            internal_logger.debug("Monitoring file: {}".format(path))
            tree = cast(
                ast.Module,
                compile(
                    data,
                    path,
                    "exec",
                    flags=ast.PyCF_ONLY_AST,
                    dont_inherit=True,
                    optimize=_optimize,
                ),
            )  # type: ast.Module
            transformer = ASTTransformer(path, data.splitlines())
            tree = transformer.visit(tree)
            tree.body = [
                *ast.parse("from pyhud.native import HudContextManager\n").body,
                *tree.body,
            ]
            return cast(
                CodeType,
                compile(
                    tree,
                    path,
                    "exec",
                    flags=transformer.compiler_flags,
                    dont_inherit=True,
                    optimize=_optimize,
                ),
            )
        except Exception as e:
            internal_logger.error(
                "Error while transforming AST on file: {}, error: {}".format(path, e)
            )
            return super().source_to_code(data, path)


def module_hook(path: str) -> ModuleFinder:
    original_finder = None
    for hook in sys.path_hooks:
        if hook is not module_hook:
            try:
                original_finder = hook(path)
            except ImportError:
                continue
            return ModuleFinder(path, original_finder=original_finder)  # type: ignore[arg-type,unused-ignore]

    raise ImportError("No module finder found for path: {}".format(path))


def register_to_fork() -> None:
    if hasattr(os, "register_at_fork"):

        def _disable_hud() -> None:
            internal_logger.info(
                "Disabling HUD in child process"
            )  # It will print to the console if HUD_DEBUG is set
            set_hud_running_mode(False)
            # We don't clear the memory of main thread like the queue, aggs and logger, because of COW.
            # If we don't touch the memory, that's still "shared", but if we clear it, it copied and actually consomes more memory

        os.register_at_fork(after_in_child=_disable_hud)


hook_set = False


def set_hook() -> None:
    global hook_set
    if hook_set:
        return
    if should_run_hud():
        hook_set = True

        if not config.disable_exception_handler:
            install_exception_handler()

        for path in paths_to_wrap:
            if path in sys.path_importer_cache:
                del sys.path_importer_cache[path]
        for path in sys.path:
            if path in sys.path_importer_cache:
                del sys.path_importer_cache[path]

        loader_details = []
        if hasattr(sys.path_hooks[-1]("."), "_loaders"):
            for suffix, loader in sys.path_hooks[-1](".")._loaders:  # type: ignore[attr-defined]
                if suffix == ".py":
                    loader_details.append((MySourceLoader, [suffix]))
                else:
                    loader_details.append((loader, [suffix]))

        sys.path_hooks.insert(0, MyFileFinder.path_hook(*loader_details))
        sys.path_hooks.insert(0, module_hook)
        register_to_fork()
