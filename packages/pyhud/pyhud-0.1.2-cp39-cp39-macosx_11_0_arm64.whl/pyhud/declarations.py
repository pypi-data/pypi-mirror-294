import ast
from typing import List, Optional, Union
from uuid import UUID

from .schemas.events import (
    ArgumentType,
    CodeBlockType,
    FunctionArgument,
    FunctionDeclaration,
    ScopeNode,
)


def parse_function_node_arguments(
    node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
) -> List[FunctionArgument]:
    # We use this specific order to match the order of the arguments in the function signature.
    # paramters look like: (positional_only, /, positional_or_keyword, *varargs, keyword_only, **kwargs),
    # while all of them are optional and can be omitted
    arguments = []
    if hasattr(node.args, "posonlyargs"):  # Added in Python 3.8
        for arg in node.args.posonlyargs:
            arguments.append(FunctionArgument(arg.arg, ArgumentType.POSITIONAL_ONLY))
    for arg in node.args.args:
        arguments.append(FunctionArgument(arg.arg, ArgumentType.ARG))
    if node.args.vararg:
        arguments.append(FunctionArgument(node.args.vararg.arg, ArgumentType.VARARG))
    for arg in node.args.kwonlyargs:
        arguments.append(FunctionArgument(arg.arg, ArgumentType.KEYWORD_ONLY))
    if node.args.kwarg:
        arguments.append(FunctionArgument(node.args.kwarg.arg, ArgumentType.KWARG))
    return arguments


class Declaration:
    __match_args__ = (
        "function_id",
        "name",
        "path",
        "start_line",
        "end_line",
        "is_async",
        "source_code_hash",
        "code_block_type",
    )

    def __init__(
        self,
        function_id: UUID,
        name: str,
        path: str,
        start_line: int,
        end_line: Optional[int],
        is_async: bool,
        source_code_hash: str,
        code_block_type: CodeBlockType,
        arguments: Optional[List[FunctionArgument]] = None,
        scope: Optional[List[ScopeNode]] = None,
    ):
        self.function_id = function_id
        self.name = name
        self.path = path
        self.start_line = start_line
        self.end_line = end_line
        self.is_async = is_async
        self.source_code_hash = source_code_hash
        self.code_block_type = code_block_type
        self.arguments = arguments or []
        self.scope = scope or []

    @classmethod
    def from_function_node(
        cls,
        function_id: UUID,
        node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
        source_code_hash: str,
        path: str,
        is_async: bool,
        scope: List[ScopeNode],
    ) -> "Declaration":
        return cls(
            function_id,
            node.name,
            path,
            node.lineno,
            getattr(node, "end_lineno", None),
            is_async,
            source_code_hash,
            CodeBlockType.FUNCTION,
            parse_function_node_arguments(node),
            scope,
        )

    @classmethod
    def from_class_node(
        cls,
        class_id: UUID,
        node: ast.ClassDef,
        source_code_hash: str,
        path: str,
        scope: List[ScopeNode],
    ) -> "Declaration":
        return cls(
            class_id,
            node.name,
            path,
            node.lineno,
            getattr(node, "end_lineno", None),
            False,
            source_code_hash,
            CodeBlockType.CLASS,
            None,
            scope,
        )

    def for_request(self) -> "FunctionDeclaration":
        return FunctionDeclaration(
            self.path,
            str(self.function_id),
            self.is_async,
            self.name,
            self.source_code_hash,
            self.start_line,
            self.end_line,
            self.code_block_type,
            self.arguments,
            self.scope,
        )


class DeclarationsAggregator:
    def __init__(self) -> None:
        self.declarations = []  # type: List[Declaration]

    def add_declaration(self, declaration: Declaration) -> None:
        self.declarations.append(declaration)

    def get_declarations(self) -> List[FunctionDeclaration]:
        return [declaration.for_request() for declaration in self.declarations]

    def clear(self) -> None:
        self.declarations = []
