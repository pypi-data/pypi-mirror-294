import typing as T
import time

import graphql
from fastapi import Request, Response, BackgroundTasks

from fastgql.gql_ast import models as M
from fastgql.gql_ast.translator import Translator
from fastgql.gql_models import GQL, GQLError
from fastgql.execute.utils import (
    build_is_not_nullable_map,
    CacheDict,
    Result,
    InfoType,
    ContextType,
    gql_errors_to_graphql_errors,
    RESULT_WRAPPERS,
)
from fastgql.execute.resolver import Resolver

DISPLAY_TO_PYTHON_MAP: dict[str, str] = {}


class Executor:
    """this class has the un-changing config"""

    def __init__(
        self,
        python_to_display_map: dict[str, str],
        schema: graphql.GraphQLSchema,
        query_model: GQL | None,
        mutation_model: GQL | None,
        root_nodes_cache_size: int = 100,
        process_errors: T.Optional[T.Callable[[list[GQLError]], list[GQLError]]] = None,
        result_wrappers: RESULT_WRAPPERS = None,
    ):
        self.python_to_display_map = python_to_display_map
        self.display_to_python_map = {
            v: k for k, v in self.python_to_display_map.items()
        }
        self.schema = schema
        self.is_not_nullable_map = build_is_not_nullable_map(schema)
        self.operation_type_to_model: dict[M.OperationType, GQL | None] = {
            M.OperationType.query: query_model,
            M.OperationType.mutation: mutation_model,
        }
        self.root_nodes_cache: dict[str, list[M.OperationNode]] = CacheDict(
            cache_len=root_nodes_cache_size
        )
        self.process_errors = process_errors
        self.result_wrappers = result_wrappers

        DISPLAY_TO_PYTHON_MAP.update(self.display_to_python_map)

    async def execute(
        self,
        *,
        source: str,
        variable_values: dict[str, T.Any] | None,
        operation_name: str | None,
        validate_schema: bool = True,
        validate_query: bool = True,
        validate_variables: bool = True,
        info_cls: T.Type[InfoType],
        context_cls: T.Type[ContextType],
        request: Request,
        response: Response,
        bt: BackgroundTasks,
        use_cache: bool,
        print_timings: bool = False,
    ) -> Result:
        start_for_root_nodes = time.time()
        if use_cache:
            root_nodes = self.root_nodes_cache.get(source)
        else:
            root_nodes = None
        if not root_nodes:
            if validate_schema:
                schema_validation_errors = graphql.validate_schema(self.schema)
                if schema_validation_errors:
                    return Result(
                        data=None, errors=schema_validation_errors, extensions=None
                    )
            try:
                document = graphql.parse(source)
            except graphql.GraphQLError as error:
                return Result(data=None, errors=[error], extensions=None)
            if validate_query:
                validation_errors = graphql.validation.validate(self.schema, document)
                if validation_errors:
                    return Result(data=None, errors=validation_errors, extensions=None)
            if validate_variables:
                from graphql.execution.execute import assert_valid_execution_arguments

                assert_valid_execution_arguments(self.schema, document, variable_values)

            start_translate = time.time()
            root_nodes = Translator(
                document=document,
                schema=self.schema,
                display_to_python_map=self.display_to_python_map,
            ).translate()
            if print_timings:
                print(
                    f"[TRANSLATING] took {(time.time() - start_translate) * 1_000} ms"
                )
            if use_cache:
                self.root_nodes_cache[source] = root_nodes
        if print_timings:
            print(
                f"[ROOT NODES] parsing took {(time.time() - start_for_root_nodes) * 1_000} ms"
            )
        resolver = Resolver(
            operation_name=operation_name,
            display_to_python_map=self.display_to_python_map,
            info_cls=info_cls,
            context_cls=context_cls,
            is_not_nullable_map=self.is_not_nullable_map,
            variables=variable_values,
            request=request,
            response=response,
            bt=bt,
        )
        d = await resolver.resolve_root_nodes(
            root_nodes=root_nodes, operation_type_to_model=self.operation_type_to_model
        )
        # now process errors
        if self.process_errors:
            errors = self.process_errors(resolver.errors)
        else:
            errors = resolver.errors
        return Result(
            data=d, errors=gql_errors_to_graphql_errors(errors), extensions=None
        )
