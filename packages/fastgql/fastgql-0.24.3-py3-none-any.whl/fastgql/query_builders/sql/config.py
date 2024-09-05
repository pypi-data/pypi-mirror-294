import typing as T
import inspect
from dataclasses import dataclass
from pydantic import TypeAdapter

from fastgql.info import Info
from fastgql.gql_ast import models as M
from fastgql.utils import node_from_path
from .query_builder import QueryBuilder, Cardinality

from fastgql.execute.executor import DISPLAY_TO_PYTHON_MAP


@dataclass
class Property:
    path: str | None
    update_qb: T.Callable[[..., T.Any], None | T.Awaitable] = None


@dataclass
class Link:
    # table_name: str | None
    from_: str | None
    cardinality: Cardinality

    return_cls_qb_config: (
        T.Union["QueryBuilderConfig", dict[str, "QueryBuilderConfig"]] | None
    ) = None
    path_to_return_cls: tuple[str, ...] | None = None
    update_qbs: T.Callable[[..., T.Any], None | T.Awaitable] = None

    # these are for unions
    from_mapping: dict[str, str] | None = None
    update_qbs_mapping: dict[str, T.Callable[[..., T.Any], None | T.Awaitable]] = None


async def execute_update_qb(
    update_qb: T.Callable[[..., T.Any], None | T.Awaitable],
    qb: QueryBuilder,
    node: M.FieldNode,
    child: M.FieldNode,
    info: Info,
) -> None:
    new_kwargs: dict[str, T.Any] = {}
    sig = inspect.signature(update_qb)
    args_by_name: dict[str, M.Argument] = {a.name: a for a in child.arguments}
    for name, param in sig.parameters.items():
        if name in args_by_name:
            arg = args_by_name[name]
            val = arg.value
            if val is not None:
                val = TypeAdapter(param.annotation).validate_python(
                    val, context={"_display_to_python_map": DISPLAY_TO_PYTHON_MAP}
                )
            new_kwargs[name] = val
        elif name == "qb":
            new_kwargs[name] = qb
        elif name == "node":
            new_kwargs[name] = node
        elif name == "child_node":
            new_kwargs[name] = child
        elif name == "info":
            new_kwargs[name] = info

    _ = update_qb(**new_kwargs)
    if inspect.isawaitable(_):
        await _


async def execute_update_qbs(
    update_qbs: T.Callable[[..., T.Any], None | T.Awaitable],
    original_child: M.FieldNode,
    qb: QueryBuilder,
    child_qb: QueryBuilder,
    node: M.FieldNode,
    child: M.FieldNode | M.InlineFragmentNode,
    info: Info,
) -> None:
    new_kwargs: dict[str, T.Any] = {}
    sig = inspect.signature(update_qbs)
    args_by_name: dict[str, M.Argument] = {a.name: a for a in original_child.arguments}
    for name, param in sig.parameters.items():
        if name in args_by_name:
            arg = args_by_name[name]
            val = arg.value
            if val is not None:
                val = TypeAdapter(param.annotation).validate_python(
                    val, context={"_display_to_python_map": DISPLAY_TO_PYTHON_MAP}
                )
            new_kwargs[name] = val
        elif name == "qb":
            new_kwargs[name] = qb
        elif name == "child_qb":
            new_kwargs[name] = child_qb
        elif name == "node":
            new_kwargs[name] = node
        elif name == "child_node":
            new_kwargs[name] = child
        elif name == "info":
            new_kwargs[name] = info
        elif name == "original_child":
            new_kwargs[name] = original_child

    _ = update_qbs(**new_kwargs)
    if inspect.isawaitable(_):
        await _


@dataclass
class QueryBuilderConfig:
    table_name: str

    properties: dict[str, Property]
    links: dict[str, Link]

    def is_empty(self) -> bool:
        return not self.properties and not self.links

    async def from_info(
        self,
        info: Info,
        node: M.FieldNode | M.InlineFragmentNode,
        cardinality: Cardinality,
    ) -> QueryBuilder | None:
        if not node:
            return None
        qb = QueryBuilder(table_name=self.table_name, cardinality=cardinality)
        children_q = [*node.children]
        while len(children_q) > 0:
            child = children_q.pop(0)
            if isinstance(child, M.InlineFragmentNode):
                children_q.extend(child.children)
            else:
                if child.name in self.properties:
                    property_config = self.properties[child.name]

                    if path_to_value := property_config.path:
                        qb.sel(name=child.name, path=path_to_value)
                    if update_qb := property_config.update_qb:
                        await execute_update_qb(
                            update_qb=update_qb,
                            qb=qb,
                            node=node,
                            child=child,
                            info=info,
                        )
                if child.name in self.links:
                    method_config = self.links[child.name]
                    if method_config.from_mapping and method_config.from_:
                        raise Exception("Cannot provide both from_mapping and from_.")
                    original_child = child
                    if method_config.path_to_return_cls:
                        child = node_from_path(
                            node=child, path=[*method_config.path_to_return_cls]
                        )
                    if config := method_config.return_cls_qb_config:
                        if isinstance(config, dict):
                            # first, get the dangling children, so we can add them to the fragments
                            dangling_children: list[M.FieldNode] = []
                            _type_condition_children: list[M.InlineFragmentNode] = []
                            for c in child.children:
                                if isinstance(c, M.FieldNode):
                                    dangling_children.append(c)
                                elif isinstance(c, M.InlineFragmentNode):
                                    _type_condition_children.append(c)
                                else:
                                    raise Exception(
                                        f"Invalid node for config as dict: {c=}, {child=}"
                                    )

                            # must combine type condition children for repeats
                            node_by_tc: dict[str, M.InlineFragmentNode] = {}
                            for tc_node in _type_condition_children:
                                type_condition = tc_node.type_condition
                                if seen_node := node_by_tc.get(type_condition):
                                    seen_node.children.extend(tc_node.children)
                                else:
                                    node_by_tc[type_condition] = tc_node

                            for child_child in node_by_tc.values():
                                # now add dangling children to these children
                                child_child.children.extend(dangling_children)
                                child_child_qb: QueryBuilder = await config[
                                    child_child.type_condition
                                ].from_info(
                                    info=info,
                                    node=child_child,
                                    cardinality=method_config.cardinality,
                                )
                                from_where = None
                                if method_config.from_mapping:
                                    from_where = method_config.from_mapping.get(
                                        child_child.type_condition
                                    )
                                if not from_where:
                                    from_where = method_config.from_
                                if from_where:
                                    qb.sel_sub(
                                        name=f"{child.alias or child.name}__{child_child.type_condition}",
                                        qb=child_child_qb.set_from(from_where),
                                    )
                                if update_qbs := method_config.update_qbs:
                                    await execute_update_qbs(
                                        update_qbs=update_qbs,
                                        original_child=original_child,
                                        qb=qb,
                                        child_qb=child_child_qb,
                                        node=node,  # maybe this should be child
                                        child=child_child,
                                        info=info,
                                    )
                                if method_config.update_qbs_mapping:
                                    if (
                                        update_qbs_condition
                                        := method_config.update_qbs_mapping.get(
                                            child_child.type_condition
                                        )
                                    ):
                                        await execute_update_qbs(
                                            update_qbs=update_qbs_condition,
                                            original_child=original_child,
                                            qb=qb,
                                            child_qb=child_child_qb,
                                            node=node,  # maybe this should be child
                                            child=child_child,
                                            info=info,
                                        )

                        else:
                            child_qb = await config.from_info(
                                info=info,
                                node=child,
                                cardinality=method_config.cardinality,
                            )
                            if from_where := method_config.from_:
                                qb.sel_sub(
                                    name=child.alias or child.name,
                                    qb=child_qb.set_from(from_where),
                                )
                            if update_qbs := method_config.update_qbs:
                                await execute_update_qbs(
                                    update_qbs=update_qbs,
                                    original_child=original_child,
                                    qb=qb,
                                    child_qb=child_qb,
                                    node=node,
                                    child=child,
                                    info=info,
                                )
        return qb
