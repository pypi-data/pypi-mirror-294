from multi_db_query_builder.database_object_handler import DatabaseObjectHandler


def check_if_table_exists(data_store, db_session, schema_name, table_name):
    """
    Check if a table exists in a specified schema within a given database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    table_name (str): The name of the table to check for existence.

    Returns:
    bool: True if the table exists, False otherwise.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.check_if_table_exists(db_session, schema_name, table_name)
    return res


def check_if_column_exists(
    data_store, db_session, schema_name, table_name, column_name
):
    """
    Check if a specified column exists in a given table within a specified schema of a database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    table_name (str): The name of the table to check for the existence of the column.
    column_name (str): The name of the column to check for existence.

    Returns:
    bool: True if the column exists in the table, False otherwise.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.check_if_column_exists(
        db_session, schema_name, table_name, column_name
    )
    return res


def get_schemas_like_pattern(
    data_store, db_session, schema_name=None, source_database=None
):
    """
    Retrieve schemas from a database that match a given pattern.

    This function uses the DatabaseObjectHandler to interact with the specified data store.
    It then calls the get_schemas_like_pattern method of the appropriate data store object
    to retrieve schemas that match the provided pattern.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str, optional): The pattern to match against schema names.
        If not provided, all schemas will be returned.

    Returns:
    list: A list of schema names that match the provided pattern.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.get_schemas_like_pattern(
        db_session, schema_name, source_database
    )
    return res


def fetch_column_name(data_store, db_session, schema_name, table_name):
    """
    Fetches the names of columns from a specified table within a given schema of a database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    table_name (str): The name of the table from which to fetch column names.

    Returns:
    list: A list of column names from the specified table within the given schema.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.fetch_column_name(db_session, schema_name, table_name)
    return res


def fetch_column_name_datatype(
    data_store, db_session, schema_name, table_name, filter_val="fivetran"
):
    """
    Fetches the names and data types of columns from a specified table within a given schema of a database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    table_name (str): The name of the table from which to fetch column names and data types.
    filter_val (str, optional): A filter value to apply to the column names.

    Returns:
    list: A list of dictionaries, where each dictionary contains keys 'column_name' and 'data_type', with their corresponding values.
    [
        {
            "column_name": column_name,
            "data_type": data_type,
        }
    ]
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.fetch_column_name_datatype(
        db_session, schema_name, table_name, filter_val
    )
    return res


def fetch_single_column_name_datatype(
    data_store, db_session, schema_name, table_name, column_name
):
    """
    Fetches the name and data type of a specified column from a given table within a specified schema of a database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    table_name (str): The name of the table from which to fetch the column's name and data type.
    column_name (str): The name of the column to fetch the name and data type for.

    Returns:
    dict: A dictionary containing keys 'column_name' and 'data_type', with their corresponding values.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.fetch_single_column_name_datatype(
        db_session, schema_name, table_name, column_name
    )
    return res


def fetch_all_tables_in_schema(
    data_store, db_session, schema_name, pattern=None, source_database=None
):
    """
    Fetches all table names within a specified schema of a database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    pattern (str, optional): The pattern to match against table names.
        If not provided, all tables within the schema will be returned.

    Returns:
    list: A list of table names that match the provided pattern within the specified schema.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.fetch_all_tables_in_schema(
        db_session, schema_name, pattern, source_database
    )
    return res


def fetch_all_views_in_schema(data_store, db_session, schema_name, pattern=None):
    """
    Fetches all views within a specified schema of a database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    pattern (str, optional): The pattern to match against table names.
        If not provided, all tables within the schema will be returned.

    Returns:
    list: A list of names of views that match the provided pattern within the specified schema.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.fetch_all_views_in_schema(db_session, schema_name, pattern)
    return res


def fetch_table_type_in_schema(data_store, db_session, schema_name, table_name):
    """
    Fetches the type (table or view) of a specified table within a given schema of a database.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema_name (str): The name of the schema within the database.
    table_name (str): The name of the table to fetch the type for.

    Returns:
    str: The type of the table (either 'table' or 'view').
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.fetch_table_type_in_schema(
        db_session, schema_name, table_name
    )
    return res


def enclose_reserved_keywords(data_store, query):
    """
    Encloses reserved keywords in a given SQL query with appropriate escape characters.

    Parameters:
    data_store (str): The name of the data store or database.
    query (str): The SQL query to be processed.

    Returns:
    str: The SQL query with reserved keywords enclosed with appropriate escape characters.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.enclose_reserved_keywords(query)
    return res


def enclose_reserved_keywords_v2(data_store, columns_string):
    """
    Encloses reserved keywords in a given string of column names with appropriate escape characters.

    This function is used to handle reserved keywords in SQL queries. It takes a string of column names
    as input and returns the same string with reserved keywords enclosed with appropriate escape characters.
    The escape characters depend on the specific database system being used.

    Parameters:
    data_store (str): The name of the data store or database.
    columns_string (str): The string of column names to be processed. This string may contain comma-separated
                          column names.

    Returns:
    str: The input string with reserved keywords enclosed with appropriate escape characters.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.enclose_reserved_keywords_v2(columns_string)
    return res


def handle_reserved_keywords(data_store, query_string):
    """
    This function handles reserved keywords in a given SQL query by enclosing them with appropriate escape characters.

    Parameters:
    data_store (str): The name of the data store or database.
    query_string (str): The SQL query to be processed.

    Returns:
    str: The SQL query with reserved keywords enclosed with appropriate escape characters.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.handle_reserved_keywords(query_string)
    return res


def get_tables_under_schema(data_store, db_session, schema):
    """
    Retrieves a list of table names under a specified schema from a given data store.

    Parameters:
    data_store (str): The name of the data store or database.
    db_session (object): The database session object for executing queries.
    schema (str): The name of the schema within the database.

    Returns:
    list: A list of table names under the specified schema.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.get_tables_under_schema(db_session, schema)
    return res


#  OPERATIONS


def mode_function(data_store, column, alias=None):
    """
    This function generates a SQL query to calculate the mode of a specified column in a database.

    Parameters:
    data_store (str): The name of the data store or database.
    column (str): The name of the column for which to calculate the mode.
    alias (str, optional): The alias to be used for the calculated mode value. If not provided, no alias will be used.

    Returns:
    str: A SQL query string that calculates the mode of the specified column.

    Example Output for snowflake datastore:
    ' mode("column_name") AS "alias_name"'
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.mode_function(column, alias)
    return res


def median_function(data_store, column, alias=None):
    """
    Calculates the median value of a specified column in a database.

    This function generates a SQL query to calculate the median of a given column.

    Parameters:
    data_store (str): The name of the data store or database.
    column (str): The name of the column for which to calculate the median.
    alias (str, optional): The alias to be used for the calculated median value. If not provided, no alias will be used.

    Returns:
    str: A SQL query string that calculates the median of the specified column.

    Example Output for snowflake datastore:
    ' median("column_name") AS "alias_name"'
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.median_function(column, alias)
    return res


def concat_function(data_store, column, alias, separator):
    """
    This function generates a SQL query to concatenate a specified column with a given separator.

    Parameters:
    data_store (str): The name of the data store or database.
    column (str): The list of strings to be concatenated.
    alias (str): The alias to be used for the concatenated column.
    separator (str): The separator to be used between the values of the column.

    Returns:
    str: A SQL query string that concatenates the specified column with the given separator.

    Example Output for snowflake datastore when separator is comma (,):
    ' CONCAT_WS(',', 'ONE', 'TWO', 'THREE') AS "alias_name" '
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.concat_function(column, alias, separator)
    return res


def pivot_function(data_store, fields, column_list, schema, table_name):
    """
    This function generates a SQL query for pivoting data based on the given fields.

    Parameters:
    - data_store (str): The name of the data store or database.
    - fields (dict): A dictionary containing the pivoting fields such as column, data_type, value_column, and mappings.
    - column_list (list): A list of column names to be included in the SELECT clause of the query.
    - schema (str): The name of the schema where the table resides.
    - table_name (str): The name of the table to be pivoted.

    Returns:
    - str: A SQL query string for pivoting the data based on the given fields.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.pivot_function(fields, column_list, schema, table_name)
    return res


def trim_function(data_store, column, value, condition, alias=None):
    """
    This function generates a SQL TRIM statement based on the provided condition.

    Parameters:
    - data_store (str): The name of the data store or database.
    - column (str): The name of the column to apply the TRIM function on.
    - value (str): The value to trim from the specified column.
    - condition (str): The condition for trimming. It can be one of the following:
        - "leading": Trims leading characters.
        - "trailing": Trims trailing characters.
        - "both": Trims both leading and trailing characters.
    - alias (str, optional): The alias for the result column. If not provided, no alias will be used.

    Returns:
    str: A SQL statement with the TRIM function applied to the specified column based on the given condition.
    If an alias is provided, the result column will be aliased accordingly.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.trim_function(column, value, condition, alias)
    return res


def split_function(data_store, column, delimiter, part, alias=None):
    """
    This function splits a string into parts based on a specified delimiter and returns a specific part.

    Parameters:
    - data_store (str): The name of the data store or database.
    - column (str): The column or string to be split.
    - delimiter (str): The character used to separate the parts of the string.
    - part (int): The part of the string to be returned. The first part is considered as part 1.
    - alias (str, optional): The alias for the result column. If not provided, the result column will not have an alias.

    Returns:
    str: A SQL expression that splits the given column using the specified delimiter and returns the specified part.
         If an alias is provided, the result column will be aliased with the given alias.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.split_function(column, delimiter, part, alias)
    return res


def timestamp_to_date_function(data_store, column, alias=None):
    """
    This function generates a SQL statement to convert a timestamp column to a date column.

    Parameters:
    - data_store (str): The name of the data store or database.
    - column (str): The name of the timestamp column to be converted.
    - alias (str, optional): The alias for the result column. If not provided, no alias will be used.

    Returns:
    str: A SQL statement with the conversion from timestamp to date applied to the specified column.
         If an alias is provided, the result column will be aliased accordingly.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.timestamp_to_date_function(column, alias)
    return res


def substring_function(data_store, column, start, end):
    """
    This function generates a SQL query to extract a substring from a given column.

    Parameters:
    - data_store (str): The name of the data store or database.
    - column (str): The name of the column from which the substring needs to be extracted.
    - start (int): The starting position of the substring (1-indexed).
    - end (int): The ending position of the substring (inclusive).

    Returns:
    str: A SQL query string that extracts the specified substring from the given column.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.substring_function(column, start, end)
    return res


def table_rename_query(data_store, schema_name, old_table_name, new_table_name):
    """
    This function generates a SQL query to rename a table in a specified schema.

    Parameters:
    - data_store (str): The name of the data store or database.
    - schema_name (str): The name of the schema where the table resides.
    - old_table_name (str): The current name of the table.
    - new_table_name (str): The new name to be assigned to the table.

    Returns:
    str: A SQL query string that can be executed to rename the table.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.table_rename_query(
        schema_name, old_table_name, new_table_name
    )
    return res


def date_diff_in_hours(data_store, start_date, end_date, table_name, alias):
    """
    Generate a SQL query to calculate the difference in hours between two date/time columns in a given table.

    Parameters:
    - data_store (str): The name of the data store or database.
    - start_date (str): The name of the column representing the start date/time.
    - end_date (str): The name of the column representing the end date/time.
    - table_name (str): The name of the table where the date/time columns are located.
    - alias (str): The alias for the result column.

    Returns:
    str: A SQL query string that calculates the difference in hours between the start_date and end_date columns
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.date_diff_in_hours(start_date, end_date, table_name, alias)
    return res


def date_substraction(data_store, date_part, start_date, end_date, alias=None):
    """
    Calculate the difference between two dates or timestamps based on a specified date part.

    Parameters:
    - data_store (str): The name of the data store or database.
    - date_part (str): The date part to calculate the difference. It can be 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', or 'SECOND'.
    - start_date (str): The start date or timestamp.
    - end_date (str): The end date or timestamp.
    - alias (str, optional): The alias for the result column. If not provided, no alias will be used.

    Returns:
    str: A SQL query string that calculates the difference between the start_date and end_date based on the specified date part.
         If an alias is provided, the result column will be named with the alias.
    """
    data_store_object = DatabaseObjectHandler.get_data_object(data_store)
    res = data_store_object.date_substraction(date_part, start_date, end_date, alias)
    return res
