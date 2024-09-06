# Multi Database Query Builder

The powerful and flexible query builder for multiple databases.

## Overview

This package simplifies SQL query construction for various databases by offering a unified set of methods and operations. It abstracts database-specific syntax, allowing you to focus on crafting the logic of your queries rather than dealing with different database dialects.

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Conclusion](#conclusion)

---

## Installation

To avoid conflicts with other packages, we recommend installing **multi-db-query-builder** within a virtual environment:

```
pip install multi-db-query-builder
```

## Requirements

1. **`data_store`**: Supported data stores are `snowflake`, `postgresql`, `bigquery`
2. **`db_session`**: Database session object

## Usage

To use the module, import the necessary functions from the module. Then, passing the type of the database you want to interact with and other required parameters, call the desired methods to build SQL queries.

Here are two examples of how to use the module:

### Example 1: To check if a table exists in a given schema

```python
from multi_database_query_builder import check_if_table_exists

# Check if a table exists in a given schema

data_store = "snowflake"  # Replace with your database type (e.g., "snowflake", "postgresql", "redshift".)
db_session = "your_database_session"  # Replace with your database session object

schema_name = "your_schema_name"
table_name = "your_table_name"
exists = check_if_table_exists(data_store, db_session, schema_name, table_name)
print(exists) # True if exists, otherwise False
```

### Example 2: Fetch column names and data types of table

```python
from multi_database_query_builder import check_if_table_exists

# Retrieve column names and data types

data_store = "snowflake"
db_session = "your_database_session"
schema_name = "your_schema_name"
table_name = "your_table_name"
col_dtypes = fetch_column_name_datatype(data_store, db_session, schema_name, table_name)
print(col_dtypes)
"""
[
    {
        "column_name": name,
        "data_type": varchar,
    },
    {
        "column_name": age,
        "data_type": int,
    }

]
"""
```

## Documentation

Below is a comprehensive list of available methods, along with their detailed documentation:
<br>

<details>
<summary><strong>check_if_table_exists</strong> - Check if a table exists in a specified schema.</summary>

```python
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
```

</details>

<details>
<summary><strong>check_if_column_exists</strong> - Check if a specified column exists in a given table.</summary>

```python
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
```

</details>

<details>
<summary><strong>get_schemas_like_pattern</strong> - Retrieve schemas from a database that match a given pattern.</summary>

```python
def get_schemas_like_pattern(data_store, db_session, schema_name=None):
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
```

</details>

<details>
<summary><strong>fetch_column_name</strong> - Fetches the names of columns from a specified table.</summary>

```python
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
```

</details>

<details>
<summary><strong>fetch_column_name_datatype</strong> - Fetches the names and data types of columns from a specified table.</summary>

```python
def fetch_column_name_datatype(
    data_store, db_session, schema_name, table_name, filter_val=""
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
    list: A list of dictionaries, where each dictionary contains keys; column_name and data_type and its corresponding values.
    [
        {
            "column_name": column_name,
            "data_type": data_type,
        }
    ]
    """
```

</details>

<details>
<summary><strong>fetch_single_column_name_datatype</strong> - Fetches the name and data type of a specified column from a given table.</summary>

```python
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
```

</details>

<details>
<summary><strong>fetch_all_tables_in_schema</strong> - Fetches all table names within a specified schema.</summary>

```python
def fetch_all_tables_in_schema(data_store, db_session, schema_name, pattern=None):
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
```

</details>

<details>
<summary><strong>fetch_all_views_in_schema</strong> - Fetches all views within a specified schema of a database.</summary>

```python
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
```

</details>

<details>
<summary><strong>fetch_table_type_in_schema</strong> - Fetches the type (table or view) of a specified table.</summary>

```python
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
```

</details>

<details>
<summary><strong>enclose_reserved_keywords</strong> - Encloses reserved keywords in a given SQL query with appropriate escape characters.</summary>

```python
def enclose_reserved_keywords(data_store, query):
    """
    Encloses reserved keywords in a given SQL query with appropriate escape characters.

    Parameters:
    data_store (str): The name of the data store or database.
    query (str): The SQL query to be processed.

    Returns:
    str: The SQL query with reserved keywords enclosed with appropriate escape characters.
    """
```

</details>

<details>
<summary><strong>enclose_reserved_keywords_v2</strong> - Encloses reserved keywords in a given string of column names with appropriate escape characters.</summary>

```python
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
```

</details>

<details>
<summary><strong>handle_reserved_keywords</strong> - Handles reserved keywords in a given SQL query by enclosing them with appropriate escape characters.</summary>

```python
def handle_reserved_keywords(data_store, query_string):
    """
    This function handles reserved keywords in a given SQL query by enclosing them with appropriate escape characters.

    Parameters:
    data_store (str): The name of the data store or database.
    query_string (str): The SQL query to be processed.

    Returns:
    str: The SQL query with reserved keywords enclosed with appropriate escape characters.
    """
```

</details>

<details>
<summary><strong>get_tables_under_schema</strong> - Retrieves a list of table names under a specified schema.</summary>

```python
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
```

</details>

<details>
<summary><strong>mode_function</strong> - Generates a SQL query to calculate the mode of a specified column.</summary>

```python
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
```

</details>

<details>
<summary><strong>median_function</strong> - Generates a SQL query to calculate the median of a specified column.</summary>

```python
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
```

</details>

<details>
<summary><strong>concat_function</strong> - Generates a SQL query to concatenate a specified list of strings.</summary>

```python
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
```

</details>

<details>
<summary><strong>pivot_function</strong> - Generates a SQL query for pivoting data based on the given fields.</summary>

```python
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
```

</details>

<details>
<summary><strong>trim_function</strong> - Generates a SQL TRIM statement based on the provided condition.</summary>

```python
def trim_function(data_store, column, value, condition, alias=None):
    """
    This function generates a SQL TRIM statement based on the provided condition.

    Parameters:
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
```

</details>

<details>
<summary><strong>split_function</strong> - Splits a string into parts based on a specified delimiter and returns a specific part.</summary>

```python
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
```

</details>

<details>
<summary><strong>timestamp_to_date_function</strong> - Generates a SQL statement to convert a timestamp column to a date column.</summary>

```python
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
```

</details>

<details>
<summary><strong>substring_function</strong> - Generates a SQL query to extract a substring from a given column.</summary>

```python
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
```

</details>

<details>
<summary><strong>table_rename_query</strong> - Generates a SQL query to rename a table in a specified schema.</summary>

```python
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
```

</details>

<details>
<summary><strong>date_diff_in_hours</strong> - Generate a SQL query to calculate the difference in hours between two date/time columns.</summary>

```python
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
```

</details>

<details>
<summary><strong>date_substraction</strong> - Generates a SQL query to calculate the difference between two dates or timestamps based on a specified date part.</summary>

```python
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
```

</details>
<!-- 
<details>
<summary><strong></strong> - .</summary>

```python

```

</details> -->

## Troubleshooting

### Common Issues

- Unsupported Data Source: Check if the `data_store` is among the supported ones (_snowflake_, _redshift_, _postgresql_).

## Conclusion

The **`multi-db-query-builder`** package simplifies the process of building database queries across multiple database systems, making it a valuable tool for developers working in diverse environments. Whether you're managing a single database or multiple databases, this package can streamline your workflow.

We encourage you to install the package and start exploring its capabilities.

Happy coding!
