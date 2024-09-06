import re
from multi_db_query_builder.constants import BIGQUERY_RESERVED_KEYWORDS
from multi_db_query_builder.protocol_class import CommonProtocols


class BigqueryQueryBuilder(CommonProtocols):
    def __init__(self, data_store):
        super().__init__()
        self.data_store = data_store

    def check_if_table_exists(self, db_session, schema_name, table_name):
        try:
            query = f"SELECT 1 FROM {schema_name}.INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table_name}'"
            result = db_session.execute(query).fetchone()
            if not result:
                return False
            return True
        except Exception as e:
            return None

    def check_if_column_exists(self, db_session, schema_name, table_name, column_name):
        # TODO:
        return None

    def get_schemas_like_pattern(self, db_session, schema_name, source_database=None):
        try:
            schema_query = (
                f"SELECT lower(schema_name) FROM INFORMATION_SCHEMA.SCHEMATA "
            )
            condition = (
                f"WHERE schema_name LIKE lower('%{schema_name}%')"
                if schema_name
                else ""
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
        try:
            query = (
                f"SELECT column_name, data_type FROM `{schema_name}.INFORMATION_SCHEMA.COLUMNS` "
                f"WHERE table_name = '{table_name}' AND table_schema = '{schema_name}' ORDER BY ordinal_position"
            )
            result = db_session.execute(query).fetchall()
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
            query = (
                f"SELECT column_name, data_type FROM `{schema_name}.INFORMATION_SCHEMA.COLUMNS` "
                f"WHERE table_name = '{table_name}' AND table_schema = '{schema_name}' ORDER BY ordinal_position"
            )
            result = db_session.execute(query).fetchall()
            fields = []
            if result and len(result) > 0:
                for column in result:
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
        try:
            query = (
                f"SELECT column_name, data_type FROM `{schema_name}.INFORMATION_SCHEMA.COLUMNS` "
                f"WHERE table_name = '{table_name}' AND table_schema = '{schema_name}' AND column_name = '{column_name}'"
            )
            result = db_session.execute(query).fetchone()
            fields = dict()
            if result and len(result) > 0:
                fields = {
                    "column_name": result[0],
                    "data_type": result[1].split("_")[0],
                }
                return fields
            return fields
        except Exception as e:
            return None

    def fetch_all_tables_in_schema(
        self, db_session, schema_name, pattern=None, source_database=None
    ):
        try:
            query = f"SELECT table_name from INFORMATION_SCHEMA.TABLES "
            condition = f"and table_name like '%{pattern}'" if pattern else ""
            query = query + condition
            result = db_session.execute(query).fetchall()
            tables_list = []
            if result and len(result) > 0:
                tables_list.append(result[0])
            return tables_list
        except Exception as e:
            return None

    def fetch_all_views_in_schema(self, db_session, schema_name, pattern):
        # TODO
        return None

    def fetch_table_type_in_schema(self, db_session, schema_name, table_name):
        return None

    def enclose_reserved_keywords(self, query):
        try:
            # Regular expression pattern to identify reserved keywords used as column names
            pattern = r"(?i)SELECT\s+(?P<columns>.+?)\s+FROM"

            # Define a function to replace reserved keywords with double-quoted versions
            def replace_keywords(match):
                columns = match.group("columns")
                for keyword in BIGQUERY_RESERVED_KEYWORDS:
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
                '"{}"'.format(col) if col in BIGQUERY_RESERVED_KEYWORDS else col
                for col in columns
            ]
            return ", ".join(enclosed_columns)
        except Exception as e:
            return columns_string

    def handle_reserved_keywords(self, query_string):
        return ""

    def get_tables_under_schema(self, db_session, schema):
        try:
            query = (
                f"SELECT distinct table_name FROM `{schema}.INFORMATION_SCHEMA.TABLES` "
                f"table_schema = '{schema}' and table_type = 'BASE TABLE';"
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
        return ""

    def median_function(self, column, alias):
        return ""

    def concat_function(self, column, alias, separator):
        return ""

    def pivot_function(self, fields, column_list, schema, table_name):
        return ""

    def trim_function(self, column, value, condition, alias):
        return ""

    def split_function(self, column, delimeter, part, alias):
        return ""

    def timestamp_to_date_function(self, column, alias):
        return ""

    def substring_function(self, column, start, end):
        return ""

    def table_rename_query(self, schema_name, old_table_name, new_table_name):
        return f"ALTER TABLE {schema_name}.{old_table_name} RENAME TO {new_table_name}"

    def date_diff_in_hours(self, start_date, end_date, table_name, alias):
        query = f"""SELECT *, 
        EXTRACT(EPOCH FROM CAST({end_date} AS TIMESTAMP) - CAST({start_date} AS TIMESTAMP)) / 3600 AS {alias}
        FROM {table_name}"""
        return query

    def date_substraction(self, date_part, start_date, end_date, alias=None):
        query = f"DATEDIFF(HOUR, {start_date}, {end_date})"
        if alias:
            query += f" as {alias}"
        return query
