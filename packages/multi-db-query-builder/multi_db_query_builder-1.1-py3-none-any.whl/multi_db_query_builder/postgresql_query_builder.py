import re
import time

from multi_db_query_builder.constants import (
    NUMERICAL_DATA_TYPES,
    REDSHIFT_RESERVED_KEYWORDS,
)
from multi_db_query_builder.protocol_class import CommonProtocols


class PostgresqlQueryBuilder(CommonProtocols):
    def __init__(self, data_store):
        super().__init__()
        self.data_store = data_store

    def check_if_table_exists(self, db_session, schema_name, table_name):
        try:
            query = (
                f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE table_name = '{table_name}' "
                f"AND table_schema = '{schema_name}'"
            )
            result = db_session.execute(query).fetchone()
            if not result:
                return False
            return True
        except Exception as e:
            return None

    def check_if_column_exists(self, db_session, schema_name, table_name, column_name):
        try:
            result = db_session.execute(
                f"SELECT a.attname as column_name FROM "
                f"pg_attribute a JOIN pg_class t on a.attrelid = t.oid JOIN pg_namespace s on t.relnamespace = s.oid "
                f"WHERE a.attname = '{column_name}' and a.attnum > 0 AND NOT a.attisdropped AND t.relname = '{table_name}' AND s.nspname = '{schema_name}' "
                f"ORDER BY a.attnum;"
            ).fetchone()
            if result:
                return True
            return False
        except Exception as e:
            print("Something went wrong: check_if_column_exists:postgres/redhift")
            print(e)
            return False

    def get_schemas_like_pattern(self, db_session, schema_name, source_database=None):
        try:
            schema_query = f"SELECT nspname FROM pg_namespace "
            condition = f"WHERE nspname ILIKE '%{schema_name}%'" if schema_name else ""
            schema_query = schema_query + condition
            result = db_session.execute(schema_query).fetchall()
            schemas = []
            for schema in result:
                schemas.append(schema[0])
            return schemas
        except Exception as e:
            return None

    def fetch_column_name(self, db_session, schema_name, table_name):
        try:
            result = db_session.execute(
                f"SELECT a.attname as column_name FROM "
                f"pg_attribute a JOIN pg_class t on a.attrelid = t.oid JOIN pg_namespace s on t.relnamespace = s.oid "
                f"WHERE a.attnum > 0 AND NOT a.attisdropped AND t.relname = '{table_name}' AND s.nspname = '{schema_name}' "
                f"ORDER BY a.attnum;"
            ).fetchall()
            fields = []
            if result and len(result) > 0:
                for column in result:
                    fields.append(column[0])
                return fields
            else:
                return None
        except Exception as e:
            return None

    def fetch_column_name_datatype(
        self, db_session, schema_name, table_name, filter_val="fivetran"
    ):
        try:
            result = db_session.execute(
                f"SELECT a.attname as column_name, pg_catalog.format_type(a.atttypid, a.atttypmod) as data_type FROM "
                f"pg_attribute a JOIN pg_class t on a.attrelid = t.oid JOIN pg_namespace s on t.relnamespace = s.oid "
                f"WHERE a.attnum > 0 AND NOT a.attisdropped AND t.relname = '{table_name}' AND s.nspname = '{schema_name}' "
                f"ORDER BY a.attnum;"
            ).fetchall()
            fields = []
            if result and len(result) > 0:
                for column in result:
                    if filter_val in column[0].lower():
                        print("\n\nsggasgsg\n\n")
                        continue
                    else:
                        temp = {
                            "column_name": column[0],
                            "data_type": column[1].split("_")[0].split("(")[0],
                        }
                    fields.append(temp)
                return fields
            else:
                return None
        except Exception as e:
            return None

    def fetch_single_column_name_datatype(
        self, db_session, schema_name, table_name, column_name
    ):
        try:
            result = db_session.execute(
                f"SELECT a.attname as column_name, pg_catalog.format_type(a.atttypid, a.atttypmod) as data_type FROM "
                f"pg_attribute a JOIN pg_class t on a.attrelid = t.oid JOIN pg_namespace s on t.relnamespace = s.oid "
                f"WHERE a.attnum > 0 AND NOT a.attisdropped AND t.relname = '{table_name}' AND s.nspname = '{schema_name}' "
                f"AND a.attname = '{column_name}' ORDER BY a.attnum;"
            ).fetchone()
            fields = dict()
            if result and len(result) > 0:
                fields = {
                    "column_name": result[0],
                    "data_type": result[1].split("_")[0].split("(")[0],
                }
            return fields
        except Exception as e:
            return None

    def fetch_all_tables_in_schema(
        self, db_session, schema_name, pattern=None, source_database=None
    ):
        try:
            query = f"SELECT table_name from INFORMATION_SCHEMA.TABLES WHERE table_schema='{schema_name}' "
            condition = f"and table_name like '%{pattern}'" if pattern else ""
            query = query + condition
            result = db_session.execute(query).fetchall()
            tables_list = []
            if result and len(result) > 0:
                for res in result:
                    tables_list.append(res[0])
            return tables_list
        except Exception as e:
            return None

    def fetch_all_views_in_schema(self, db_session, schema_name, pattern):
        try:
            query = f"""
                SELECT table_schema, table_name
                FROM information_schema.views
                WHERE table_schema = '{schema_name}' 
                AND table_name  ILIKE '%{pattern}%'
            """
            print(query)
            temp1 = time.time()
            result = db_session.execute(query).fetchall()
            temp2 = time.time()
            print("----------------------------------------------------------------")
            print(temp2 - temp1)
            print("----------------------------------------------------------------")
            tables_list = []
            if result and len(result) > 0:
                for item in result:
                    tables_list.append(item[1])
            return tables_list
        except Exception as e:
            return None

    def fetch_table_type_in_schema(self, db_session, schema_name, table_name):
        result = db_session.execute(
            f"select table_type from information_schema.tables where "
            f"table_schema = '{schema_name}' and table_name = '{table_name}'"
        ).fetchall()
        if result:
            return result[0][0]
        return "VIEW"

    def enclose_reserved_keywords(self, query):
        try:
            # Regular expression pattern to identify reserved keywords used as column names
            pattern = r"(?i)SELECT\s+(?P<columns>.+?)\s+FROM"

            # Define a function to replace reserved keywords with double-quoted versions
            def replace_keywords(match):
                columns = match.group("columns")
                for keyword in REDSHIFT_RESERVED_KEYWORDS:
                    columns = re.sub(
                        rf"\b({keyword})\b",
                        rf'"{keyword}"',
                        columns,
                        flags=re.IGNORECASE,
                    )
                return f"SELECT {columns} FROM"

            # Use re.sub() to enclose reserved keywords with double quotes without changing their case
            return re.sub(pattern, replace_keywords, query)

        except Exception as e:
            return query

    def enclose_reserved_keywords_v2(self, columns_string):
        try:
            print("\nindise enclose_reserved_keywords_v2\n")
            columns = [col.strip() for col in columns_string.split(",")]
            enclosed_columns = [
                '"{}"'.format(col) if col in REDSHIFT_RESERVED_KEYWORDS else col
                for col in columns
            ]
            print(enclosed_columns)
            return ", ".join(enclosed_columns)
        except Exception as e:
            return columns_string

    def handle_reserved_keywords(self, query_string):
        # Loop through each reserved keyword and surround them with double quotes in the SQL query
        for keyword in REDSHIFT_RESERVED_KEYWORDS:
            query_string = re.sub(
                rf"\b{keyword}\b", f'"{keyword}"', query_string, flags=re.IGNORECASE
            )
        return query_string

    def get_tables_under_schema(self, db_session, schema):
        try:
            query = (
                f"SELECT distinct table_name FROM information_schema.tables WHERE table_schema = '{schema}' "
                f"AND table_type = 'BASE TABLE';"
            )
            result = db_session.execute(query).fetchall()
            tables = []
            for res in result:
                tables.append(res.table_name)
            return tables
        except Exception as e:
            print(e)
            return None

    def mode_function(self, column, alias):
        query = f' mode() within group (order by "{column}") '
        if alias:
            query += f'as "{alias}" '
        return query

    def median_function(self, column, alias):
        return ""

    def concat_function(self, column, alias, separator):
        return f" || '{separator}' || ".join(column) + f" AS {alias}"

    def pivot_function(self, fields, column_list, schema, table_name):
        column = fields.get("column")
        data_type = fields.get("data_type")
        value_column = fields.get("value_column")
        mappings = fields.get("mappings")
        cases = ""

        for key, value in mappings.items():
            if value.get("status") is True:
                cases += f"""CASE WHEN {column} = {f"'{key}'" if data_type not in NUMERICAL_DATA_TYPES else f"{key}"} THEN {value_column if value_column else "'1'"} ELSE '0' END AS {value.get('value')}, """

        cases = cases[:-2]
        query_string = f"""SELECT {', '.join(column_list)}, {column}, {cases} FROM {schema}.{table_name}"""
        print("query_string --> ", query_string)
        return query_string

    def trim_function(self, column, value, condition, alias):
        if alias:
            return f" TRIM({condition} '{value}' FROM {column}) as {alias} "

        return f" TRIM({condition} '{value}' FROM {column}) "

    def split_function(self, column, delimiter, part, alias):
        if alias:
            return f" split_part({column}, '{delimiter}', {part}) as {alias} "

        return f" split_part({column}, '{delimiter}', {part}) "

    def timestamp_to_date_function(self, column, alias):
        return f" TRUNC({column}) AS {alias} "

    def substring_function(self, column, start, end):
        return f" SUBSTRING({column}::TEXT FROM {start} FOR {end}) "

    def table_rename_query(self, schema_name, old_table_name, new_table_name):
        return f"ALTER TABLE {schema_name}.{old_table_name} RENAME TO {new_table_name}"

    def date_diff_in_hours(self, start_date, end_date, table_name, alias):
        query = f"""SELECT *, 
        EXTRACT(EPOCH FROM CAST({end_date} AS TIMESTAMP) - CAST({start_date} AS TIMESTAMP)) / 3600 as {alias}
        FROM {table_name}"""
        return query

    def date_substraction(self, date_part, start_date, end_date, alias):
        query = f"DATEDIFF({date_part}, {start_date}, {end_date})"
        if alias:
            query += f" as {alias}"
        return query
