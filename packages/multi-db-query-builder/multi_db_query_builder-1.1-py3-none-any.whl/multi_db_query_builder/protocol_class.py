from abc import ABC, abstractmethod


class CommonProtocols(ABC):
    @abstractmethod
    def check_if_table_exists(self, db_session, schema_name, table_name):
        pass

    @abstractmethod
    def check_if_column_exists(self, db_session, schema_name, table_name, column_name):
        pass

    @abstractmethod
    def get_schemas_like_pattern(
        self, db_session, schema_name=None, source_database=None
    ):
        pass

    @abstractmethod
    def fetch_column_name(self, db_session, schema_name, table_name):
        pass

    @abstractmethod
    def fetch_column_name_datatype(
        self, db_session, schema_name, table_name, filter_val
    ):
        pass

    @abstractmethod
    def fetch_single_column_name_datatype(
        self, db_session, schema_name, table_name, column_name
    ):
        pass

    @abstractmethod
    def fetch_all_tables_in_schema(
        self, db_session, schema_name, pattern=None, source_database=None
    ):
        pass

    @abstractmethod
    def fetch_all_views_in_schema(self, db_session, schema_name, pattern=None):
        pass

    @abstractmethod
    def fetch_table_type_in_schema(self, db_session, schema_name, table_name):
        pass

    @abstractmethod
    def enclose_reserved_keywords(self, query):
        pass

    @abstractmethod
    def enclose_reserved_keywords_v2(self, columns_string):
        pass

    @abstractmethod
    def handle_reserved_keywords(self, query_string):
        pass

    @abstractmethod
    def get_tables_under_schema(self, db_session, schema):
        pass

    #  OPERATIONS
    @abstractmethod
    def mode_function(self, column, alias):
        pass

    @abstractmethod
    def median_function(self, column, alias):
        pass

    @abstractmethod
    def concat_function(self, column, alias, separator):
        pass

    @abstractmethod
    def pivot_function(self, fields, column_list, schema, table_name):
        pass

    @abstractmethod
    def trim_function(self, column, value, condition, alias):
        pass

    @abstractmethod
    def split_function(self, column, delimiter, part, alias):
        pass

    @abstractmethod
    def timestamp_to_date_function(self, column, alias):
        pass

    @abstractmethod
    def substring_function(self, column, start, end):
        pass

    @abstractmethod
    def table_rename_query(self, schema_name, old_table_name, new_table_name):
        pass

    @abstractmethod
    def date_diff_in_hours(self, start_date, end_date, table_name):
        pass

    @abstractmethod
    def date_substraction(self, date_part, start_date, end_date, alias):
        pass
