import re
import os

from multi_db_query_builder.constants import (
    NUMERICAL_DATA_TYPES,
    SNOWFLAKE_RESERVED_KEYWORDS,
)
from multi_db_query_builder.protocol_class import CommonProtocols


class SnowflakeQueryBuilder(CommonProtocols):
    def __init__(self, data_store):
        self.data_store = data_store

    @staticmethod
    def convert_to_upper(schema_name, table_name):
        return schema_name.upper(), table_name.upper()

    def check_if_table_exists(self, db_session, schema_name, table_name):
        schema_name, table_name = self.convert_to_upper(schema_name, table_name)
        try:
            query = (
                f"SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}' "
                f"AND TABLE_SCHEMA = '{schema_name}'"
            )
            print(query)
            result = db_session.execute(query).fetchone()
            print(result)
            if not result:
                return False
            return True
        except Exception as e:
            print(e)
            return None

    def check_if_column_exists(self, db_session, schema_name, table_name, column_name):
        schema_name, table_name = self.convert_to_upper(schema_name, table_name)
        try:
            query = (
                f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{schema_name}' "
                f"AND TABLE_NAME = '{table_name}' AND COLUMN_NAME = '{column_name.upper()}'"
            )
            result = db_session.execute(query).fetchone()
            if not result:
                return False
            return True
        except Exception as e:
            return None

    def get_schemas_like_pattern(self, db_session, schema_name, source_database=None):
        if schema_name:
            schema_name = schema_name.upper()
        try:
            if source_database:
                schema_query = f"SELECT schema_name FROM {source_database}.INFORMATION_SCHEMA.SCHEMATA "
            else:
                schema_query = f"SELECT schema_name FROM INFORMATION_SCHEMA.SCHEMATA "
            condition = (
                f"WHERE schema_name LIKE '%{schema_name}%'" if schema_name else ""
            )
            schema_query = schema_query + condition
            result = db_session.execute(schema_query).fetchall()
            schemas = []
            for schema in result:
                schemas.append(schema[0])
            return schemas
        except Exception as e:
            return None

    def fetch_column_name(self, db_session, schema_name, table_name):
        schema_name, table_name = self.convert_to_upper(schema_name, table_name)
        try:
            query = (
                f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}' "
                f"AND table_schema = '{schema_name}' ORDER BY ordinal_position"
            )
            print(f"\n\n\nquery --> {query}\n\n", flush=True)
            result = db_session.execute(query).fetchall()
            print(f"\n\n\nresult --> {result}\n\n", flush=True)
            fields = []
            if result and len(result) > 0:
                for column in result:
                    fields.append(column[0])
                print(f"\n\n\nfields --> {fields}\n\n", flush=True)
                return fields
            else:
                return None
        except Exception as e:
            return None

    def fetch_column_name_datatype(
        self, db_session, schema_name, table_name, filter_val="fivetran"
    ):
        schema_name, table_name = self.convert_to_upper(schema_name, table_name)
        try:
            query = (
                f"SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}' "
                f"AND table_schema = '{schema_name}' ORDER BY ordinal_position"
            )
            print(query)
            result = db_session.execute(query).fetchall()
            fields = []
            if result and len(result) > 0:
                for column in result:
                    if filter_val in column[0].lower():
                        continue
                    else:
                        temp = {
                            "column_name": column[0],
                            "data_type": column[1].split("_")[0],
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
        schema_name, table_name = self.convert_to_upper(schema_name, table_name)
        try:
            query = (
                f"SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{table_name}' "
                f"AND table_schema = '{schema_name}' AND column_name = '{column_name.upper()}'"
            )
            result = db_session.execute(query).fetchone()
            fields = dict()
            if result and len(result) > 0:
                fields["column_name"] = result[0]
                fields["data_type"] = result[1].split("_")[0]
            return fields
        except Exception as e:
            return None

    def fetch_all_tables_in_schema(
        self, db_session, schema_name, pattern=None, source_database=None
    ):
        schema_name, table_name = self.convert_to_upper(schema_name, "")
        try:
            if source_database:
                query = f"SELECT table_name from {source_database}.INFORMATION_SCHEMA.TABLES WHERE table_schema='{schema_name}' "
            else:
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

    def fetch_all_views_in_schema(self, db_session, schema_name, pattern=None):
        schema_name, table_name = self.convert_to_upper(schema_name, "")
        try:
            query = f"SHOW VIEWS LIKE '%{pattern}%' in {schema_name}"
            print(query)
            result = db_session.execute(query).fetchall()
            tables_list = []
            if result:
                for item in result:
                    print("item : ", item)
                    tables_list.append(item["name"])
            print("tables_list : ", tables_list)
            return tables_list
        except Exception as e:
            print("Failed to fetch views in schema :", str(e))
            return None

    def fetch_table_type_in_schema(self, db_session, schema_name, table_name):
        schema_name, table_name = self.convert_to_upper(schema_name, table_name)
        result = db_session.execute(
            f"SHOW OBJECTS LIKE '{table_name}' IN {schema_name.lower()};"
        ).fetchall()
        if result:
            return result[0][4]
        return "VIEW"

    def enclose_reserved_keywords(self, query):
        try:
            # Regular expression pattern to identify reserved keywords used as column names
            pattern = r"(?i)SELECT\s+(?P<columns>.+?)\s+FROM"

            # Define a function to replace reserved keywords with double-quoted versions
            def replace_keywords(match):
                columns = match.group("columns")
                for keyword in SNOWFLAKE_RESERVED_KEYWORDS:
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
            columns = [col.strip() for col in columns_string.split(",")]
            enclosed_columns = [
                '"{}"'.format(col) if col in SNOWFLAKE_RESERVED_KEYWORDS else col
                for col in columns
            ]
            return ", ".join(enclosed_columns)
        except Exception as e:
            return columns_string

    def handle_reserved_keywords(self, query_string):
        # Loop through each reserved keyword and surround them with double quotes in the SQL query
        for keyword in SNOWFLAKE_RESERVED_KEYWORDS:
            query_string = re.sub(
                rf"\b{keyword}\b", f'"{keyword}"', query_string, flags=re.IGNORECASE
            )
        return query_string

    def get_tables_under_schema(self, db_session, schema_name):
        schema_name, table_name = self.convert_to_upper(schema_name, "")
        try:
            query = (
                f"SELECT DISTINCT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema_name}' "
                f"AND TABLE_TYPE = 'BASE TABLE';"
            )
            result = db_session.execute(query).fetchall()
            tables = []
            for res in result:
                tables.append(res.table_name)
            return tables
        except Exception as e:
            print("error:", e)
            return None

    def mode_function(self, column, alias):
        query = f' mode("{column}") '
        if alias:
            query += f'as "{alias}" '
        return query

    def median_function(self, column, alias):
        return f' median("{column}")  as "{alias}" '

    def concat_function(self, column, alias, separator):
        return f" CONCAT_WS('{separator}',{','.join(column)}) AS {alias} "

    def pivot_function(self, fields, column_list, schema, table_name):
        schema, table = self.convert_to_upper(schema, table_name)
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

    def trim_function(self, column, value, condition, alias=None):
        trim = "RTRIM"
        if condition.lower() == "leading":
            trim = "LTRIM"
        if condition.lower() == "both":
            trim = "TRIM"

        if alias:
            return f" {trim}({column},'{value}') as {alias} "

        return f" {trim}({column},'{value}') "

    def split_function(self, column, delimiter, part, alias):
        if alias:
            return f" split_part({column}, '{delimiter}', {part - 1}) as {alias} "

        return f" split_part({column}, '{delimiter}', {part - 2}) "

    def timestamp_to_date_function(self, column, alias):
        return f" TO_DATE({column}) AS {alias} "

    def substring_function(self, column, start, end):
        return f" SUBSTR({column}::TEXT, {start}, {end}) "

    def table_rename_query(self, schema_name, old_table_name, new_table_name):
        return f"ALTER TABLE {schema_name}.{old_table_name} RENAME TO {schema_name}.{new_table_name}"

    def date_diff_in_hours(self, start_date, end_date, table_name, alias):
        query = f"""SELECT *, 
        DATEDIFF(HOUR, {start_date}, {end_date}) as {alias}
        FROM {table_name}"""
        return query

    def date_substraction(self, date_part, start_date, end_date, alias):
        query = f"DATEDIFF({date_part}, {start_date}, {end_date})"
        if alias:
            query += f" as {alias}"
        return query
