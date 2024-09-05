import random
import re
import string
import typing as T
from enum import Enum

import sqlparse
from pydantic import BaseModel, Field


class PostgresDriver(str, Enum):
    SQLALCHEMY = "SQLALCHEMY"
    PSYCOPG3 = "PSYCOPG3"
    ASYNCPG = "ASYNCPG"


ListT = T.TypeVar("ListT")


def random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def chunk_list(lst: list[ListT], chunk_size: int) -> list[list[ListT]]:
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def split_text_around_where(text: str) -> tuple[str, str | None]:
    # Regex pattern to split the string around 'where' (case-insensitive)
    pattern = r"(?i)\bwhere\b"

    # Splitting the string
    parts = re.split(pattern, text, maxsplit=1)

    # Stripping whitespace from both parts
    before_where = parts[0].strip()
    after_where = parts[1].strip() if len(parts) > 1 else None

    return before_where, after_where


class FilterConnector(str, Enum):
    AND = "AND"
    OR = "OR"


class QueryBuilderError(Exception):
    pass


class Cardinality(str, Enum):
    ONE = "ONE"
    MANY = "MANY"


class Selection(BaseModel):
    name: str

    @property
    def is_simple_column(self) -> bool:
        if not isinstance(self, SelectionField):
            return False
        return (
            self.name == self.path
            or self.path == f"$current.{self.name}"
            or self.path == f'"{self.path}"'
            or self.path == f'$current."{self.name}"'
        )


class SelectionField(Selection):
    path: str
    variables: dict[str, T.Any] | None = None


class SelectionSub(Selection):
    qb: "QueryBuilder"


class CTE(BaseModel):
    cte_str: str
    join_str: str
    is_top_level: bool = True


class QueryBuilder(BaseModel):
    table_name: str
    table_alias: str | None = None

    cardinality: Cardinality
    selections: list[SelectionField | SelectionSub] = Field(default_factory=list)
    variables: dict[str, T.Any] = Field(default_factory=dict)

    ctes: list[CTE] = Field(default_factory=list)

    from_: str | None = None
    where: str | None = None

    order_by: str | None = None
    offset: str | None = None
    limit: str | None = None

    full_query_str: str | None = None
    pattern_to_replace: str | None = None

    is_count: bool = False

    @staticmethod
    def build_child_var_name(
        child_name: str, var_name: str, variables_to_use: dict[str, T.Any]
    ) -> str:
        child_name = re.sub(r"[^a-zA-Z0-9]+", "_", child_name)
        count = 0
        while var_name in variables_to_use:
            count_str = "" if not count else f"_{count}"
            var_name = f"_{child_name}{count_str}_{var_name}"
        return var_name

    def add_variable(
        self, key: str, val: T.Any, replace: bool = False
    ) -> "QueryBuilder":
        if key in self.variables:
            if not replace and self.variables[key] != val:
                raise QueryBuilderError(
                    f"Key {key} already exists in variables so you cannot add it. "
                    f"If you'd like to replace it, pass replace."
                )
        self.variables[key] = val
        return self

    def add_variables(
        self, variables: dict[str, T.Any], replace: bool = False
    ) -> "QueryBuilder":
        """if there is an error, it does not save to the builder"""
        if not variables:
            return self
        if not replace:
            for k, v in variables.items():
                if k in self.variables and v != self.variables[k]:
                    raise QueryBuilderError(
                        f"Key '{k}' already exists in variables so you cannot add it. "
                        f"If you'd like to replace it, pass replace."
                    )
        self.variables.update(variables)
        return self

    def set_offset(self, offset: int | None, replace: bool = False) -> "QueryBuilder":
        if offset is None:
            return self
        if self.offset is not None:
            if not replace:
                raise QueryBuilderError(
                    "An offset already exists. If you would like to replace it, pass in replace."
                )
        self.offset = "OFFSET $offset"
        self.add_variable("offset", offset, replace=replace)
        return self

    def set_limit(self, limit: int | None, replace: bool = False) -> "QueryBuilder":
        if limit is None:
            return self
        if self.limit is not None:
            if not replace:
                raise QueryBuilderError(
                    "A limit already exists. If you would like to replace it, pass in replace."
                )
        self.limit = "LIMIT $limit"
        self.add_variable("limit", limit, replace=replace)
        return self

    def add_cte(
        self, cte_str: str, join_str: str, variables: dict[str, T.Any] | None = None
    ) -> "QueryBuilder":
        self.add_variables(variables)
        self.ctes.append(CTE(cte_str=cte_str, join_str=join_str))
        return self

    def set_from(
        self,
        from_: str,
        variables: dict[str, T.Any] | None = None,
        replace_from: bool = False,
        replace_variables: bool = False,
    ) -> "QueryBuilder":
        if self.from_ and not replace_from:
            raise QueryBuilderError("from_ already exists.")
        self.add_variables(variables=variables, replace=replace_variables)
        pre_where, post_where = split_text_around_where(from_)
        self.from_ = pre_where
        if post_where:
            self.and_where(post_where)
        return self

    def and_where(
        self,
        where: str,
        variables: dict[str, T.Any] | None = None,
        replace_variables: bool = False,
    ) -> "QueryBuilder":
        self.add_variables(variables=variables, replace=replace_variables)
        if not self.where:
            self.where = where
        else:
            self.where = f"{self.where} AND {where}"
        return self

    def set_where(
        self,
        where: str,
        variables: dict[str, T.Any] | None = None,
        replace_where: bool = False,
        replace_variables: bool = False,
    ) -> "QueryBuilder":
        if self.where and not replace_where:
            raise QueryBuilderError("Where by already exists.")
        self.add_variables(variables=variables, replace=replace_variables)
        self.where = where
        return self

    def set_order_by(
        self,
        order_by: str,
        variables: dict[str, T.Any] | None = None,
        replace_order_by: bool = False,
        replace_variables: bool = False,
    ) -> "QueryBuilder":
        if self.order_by and not replace_order_by:
            raise QueryBuilderError("Order by already exists.")
        self.add_variables(variables=variables, replace=replace_variables)
        self.order_by = order_by
        return self

    def set_full_query_str(
        self,
        full_query_str: str,
        replace: bool = False,
        variables: dict[str, T.Any] | None = None,
        replace_variables: bool = False,
    ) -> "QueryBuilder":
        if self.full_query_str and not replace:
            raise QueryBuilderError("full_query_str already exists.")
        self.add_variables(variables=variables, replace=replace_variables)
        pattern_to_replace = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(10)
        )
        self.full_query_str = full_query_str.replace("$$", pattern_to_replace)
        self.pattern_to_replace = pattern_to_replace
        return self

    def build_subquery(
        self,
        name: str,
        qb: "QueryBuilder",
        path: tuple[str, ...],
        parent_table_alias: str,
        variables: dict,
        order_fields_alphabetically: bool,
    ) -> str:
        s, v = qb.build(
            parent_table_alias=parent_table_alias,
            path=path,
            order_fields_alphabetically=order_fields_alphabetically,
        )
        for var_name, var_val in v.items():
            if var_name in variables:
                if var_val is variables[var_name]:
                    continue
                # must change the name for the child
                new_var_name = self.build_child_var_name(
                    child_name=name,
                    var_name=var_name,
                    variables_to_use=variables,
                )
                variables[new_var_name] = var_val
                # now, must regex the str to find this and replace it
                regex = re.compile(rf"\${var_name}(?!\w)")
                s = regex.sub(f"${new_var_name}", s)
            else:
                variables[var_name] = var_val

        s = f"'{name}', ({s})"
        return s

    def build_fields_s(
        self,
        new_path: tuple[str, ...],
        table_alias: str,
        order_fields_alphabetically: bool,
    ) -> tuple[list[str], dict[str, T.Any]]:
        variables = self.variables.copy()
        subquery_strs: list[str] = [
            self.build_subquery(
                name=sel_sub.name,
                qb=sel_sub.qb,
                path=new_path,
                variables=variables,
                parent_table_alias=table_alias,
                order_fields_alphabetically=order_fields_alphabetically,
            )
            for sel_sub in self.selections
            if isinstance(sel_sub, SelectionSub)
        ]
        selection_strs: list[str] = [
            f"'{sel.name}', {sel.path}"
            for sel in self.selections
            if isinstance(sel, SelectionField)
        ]
        all_fields_strs = [*selection_strs, *subquery_strs]
        if order_fields_alphabetically:
            all_fields_strs.sort()
        if not all_fields_strs:
            raise QueryBuilderError(f"Query Builder {self=} has no fields.")

        return all_fields_strs, variables

    def build_filter_parts_s(self) -> str:
        filter_parts: list[str] = []
        if self.where:
            filter_parts.append(f"WHERE {self.where}")
        if self.order_by:
            filter_parts.append(f"ORDER BY {self.order_by}")
        if self.offset:
            filter_parts.append(self.offset)
        if self.limit:
            filter_parts.append(self.limit)
        filter_parts_s = "\n".join(filter_parts)
        return filter_parts_s

    @staticmethod
    def replace_current_and_parent(
        s: str, table_alias: str, parent_table_alias: str | None
    ) -> str:
        s = s.replace("$current", table_alias)
        if parent_table_alias:
            s = s.replace("$parent", parent_table_alias)
        return s

    def get_top_level_ctes(self) -> list[CTE]:
        ctes = [cte for cte in self.ctes if cte.is_top_level]
        for sel_sub in self.selections:
            if isinstance(sel_sub, SelectionSub):
                ctes.extend(sel_sub.qb.get_top_level_ctes())
        return ctes

    def build(
        self,
        parent_table_alias: str | None,
        path: tuple[str, ...] | None,
        order_fields_alphabetically: bool = True,
        is_count: bool | None = None,
        use_top_level_ctes: bool = True,
    ) -> tuple[str, dict[str, T.Any]]:
        is_count = is_count if is_count is not None else self.is_count
        if is_count:
            if self.limit is not None:
                raise QueryBuilderError("Cannot be is_count and have a limit.")
            if self.offset is not None:
                raise QueryBuilderError("Cannot be is_count and have an offset.")
        if path:
            new_path = (*path, self.table_name)
        else:
            new_path = (self.table_name,)
        if self.table_alias:
            table_alias = self.table_alias
        else:
            table_alias = "__".join(new_path).replace('"', "").replace(".", "__")
            if len(table_alias) > 55:
                table_alias = (
                    f"{table_alias[0:10]}{random_string(10)}{table_alias[-10:]}"
                )
        if not path:
            if table_alias.lower() == self.table_name.lower().replace('"', ""):
                table_alias = f"_{table_alias}"
        strs_list, variables = self.build_fields_s(
            new_path=new_path,
            table_alias=table_alias,
            order_fields_alphabetically=order_fields_alphabetically,
        )
        filter_parts_s = self.build_filter_parts_s()
        # now do from_
        if not self.from_:
            self.from_ = "*FROM*"
        self.from_ = self.from_.replace(
            "*FROM*", f"FROM {self.table_name} {table_alias}"
        )
        if not self.from_ or not self.from_.lower().startswith("from "):
            self.from_ = f"FROM {self.table_name} {table_alias} {self.from_}"

        # if this is the top level, use top level CTES. Otherwise, ignore them
        if use_top_level_ctes:
            ctes_to_use = self.get_top_level_ctes()
        else:
            ctes_to_use = [cte for cte in self.ctes if not cte.is_top_level]

        cte_str = ",\n".join([cte.cte_str for cte in ctes_to_use])
        cte_join_str = "\n".join([cte.join_str for cte in ctes_to_use])

        # now build the json objects by chunking the keys + vals at 50
        chunks = chunk_list(lst=strs_list, chunk_size=50)
        if len(chunks) == 1:
            json_obj_str = f'json_build_object({", ".join(chunks[0])})'
        else:
            json_obj_strs: list[str] = []
            for chunk in chunks:
                json_obj_strs.append(f'jsonb_build_object({", ".join(chunk)})')
            json_obj_str = " || ".join(json_obj_strs)
        if is_count:
            json_obj_str = f"COUNT({json_obj_str})"
        s = f"""
{cte_str}
SELECT {json_obj_str} AS {table_alias}_json
{self.from_}
{cte_join_str}
{filter_parts_s}
""".strip()
        if self.cardinality == Cardinality.MANY:
            if is_count is not True:
                s = f"""
    SELECT COALESCE(json_agg({table_alias}_json), '[]'::json) AS {table_alias}_json_agg
    FROM (
        {s}
    ) as {table_alias}_json_sub
                """.strip()
        if self.full_query_str:
            s = self.full_query_str.replace(self.pattern_to_replace, s)
        # now replace the values
        s = self.replace_current_and_parent(
            s=s, table_alias=table_alias, parent_table_alias=parent_table_alias
        )
        return s, variables

    def build_root(
        self,
        format_sql: bool = False,
        order_fields_alphabetically: bool = False,
        parent_table_alias: str = None,
        path: tuple[str, ...] = None,
        driver: PostgresDriver = PostgresDriver.SQLALCHEMY,
        is_count: bool | None = None,
    ) -> tuple[str, dict[T.Any]]:
        rr = self.build(
            order_fields_alphabetically=order_fields_alphabetically,
            parent_table_alias=parent_table_alias,
            path=path,
            is_count=is_count,
        )
        s, v = rr
        if v:
            if driver == PostgresDriver.SQLALCHEMY:
                s, variables = self.prepare_query_sqlalchemy(sql=s, params=v)
            elif driver == PostgresDriver.PSYCOPG3:
                s, variables = self.prepare_query_psycopg(sql=s, params=v)
            elif driver == PostgresDriver.ASYNCPG:
                s, variables = self.prepare_query_asyncpg(sql=s, params=v)
            else:
                raise QueryBuilderError(f"Unknown driver: {driver=}.")
        else:
            variables = {}
        if format_sql:
            s = sqlparse.format(s, reindent=True, keyword_case="upper")
        return s, variables

    @staticmethod
    def prepare_query_asyncpg(
        sql: str, params: dict[str, T.Any]
    ) -> tuple[str, list[T.Any]]:
        """
        Generated by GPT4
        Converts a SQL string with named parameters (e.g., $variable) to a format
        compatible with asyncpg (using $1, $2, etc.), and returns the new SQL string
        and the list of values in the correct order.

        :param sql: Original SQL string with named parameters
        :param params: Dictionary of parameters
        :return: Tuple of (new_sql_string, list_of_values)
        """

        # Extract the named parameters from the SQL string
        named_params = re.findall(r"\$(\w+)", sql)
        # Ensure that each parameter is unique
        unique_params = list(dict.fromkeys(named_params))

        # Replace named parameters with positional parameters ($1, $2, etc.)
        for i, param in enumerate(unique_params, start=1):
            sql = sql.replace(f"${param}", f"${i}")

        # Create the list of values in the order they appear in the query
        values = [params[param] for param in unique_params]

        return sql, values

    @staticmethod
    def prepare_query_psycopg(
        sql: str, params: dict[str, T.Any]
    ) -> tuple[str, dict[str, T.Any]]:
        """
        Converts a SQL string with named parameters (e.g., $variable) to a format
        compatible with psycopg (using %(variable)s), and returns the new SQL string
        and the dictionary of parameters.

        :param sql: Original SQL string with named parameters
        :param params: Dictionary of parameters
        :return: Tuple of (new_sql_string, dict_of_parameters)
        """

        # Extract the named parameters from the SQL string
        named_params = re.findall(r"[\$:]([\w]+)", sql)

        # Replace named parameters with %(param)s
        for param in named_params:
            sql = sql.replace(f"${param}", f"%({param})s")
            # TODO be careful with this lower one
            sql = sql.replace(f":{param}", f"%({param})s")
        return sql, {**params}

    @staticmethod
    def prepare_query_sqlalchemy(
        sql: str, params: dict[str, T.Any]
    ) -> tuple[str, dict[str, T.Any]]:
        """
        Converts a SQL string with named parameters (e.g., $variable) to a format
        compatible with sqlalchemy (using :variable), and returns the new SQL string
        and the dictionary of parameters.

        :param sql: Original SQL string with named parameters
        :param params: Dictionary of parameters
        :return: Tuple of (new_sql_string, dict_of_parameters)
        """

        # Extract the named parameters from the SQL string
        named_params = re.findall(r"\$(\w+)", sql)

        # Replace named parameters with %(param)s
        for param in named_params:
            sql = sql.replace(f"${param}", f":{param}")

        # Create the dictionary of parameters to be used in the query
        return sql, {**params}

    def existing_sel(self, name: str) -> SelectionField | SelectionSub | None:
        for sel in self.selections:
            if name == sel.name:
                return sel
        return None

    def sel(
        self, name: str, path: str = None, variables: dict[str, T.Any] | None = None
    ) -> "QueryBuilder":
        if not path:
            path = f'$current."{name}"'
        self.add_variables(variables)
        self.selections.append(
            SelectionField(name=name, path=path, variables=variables)
        )
        return self

    def sel_sub(self, name: str, qb: "QueryBuilder") -> "QueryBuilder":
        self.selections.append(SelectionSub(name=name, qb=qb))
        return self

    def add_sel(self, sel: SelectionField | SelectionSub) -> "QueryBuilder":
        if isinstance(sel, SelectionField):
            return self.sel(name=sel.name, path=sel.path, variables=sel.variables)
        elif isinstance(sel, SelectionSub):
            return self.sel_sub(name=sel.name, qb=sel.qb)
        else:
            raise QueryBuilderError(
                f"Can only add selections for SelectionField or SelectionSub, not {type(sel)}"
            )
