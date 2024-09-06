from multi_db_query_builder.bigquery_query_builder import BigqueryQueryBuilder
from multi_db_query_builder.constants import (
    BIGQUERY,
    POSTGRESQL,
    REDSHIFT,
    SNOWFLAKE,
)
from multi_db_query_builder.postgresql_query_builder import PostgresqlQueryBuilder
from multi_db_query_builder.snowflake_query_builder import SnowflakeQueryBuilder


class DatabaseObjectHandler:
    @staticmethod
    def get_data_object(data_store):
        try:
            if data_store == SNOWFLAKE:
                snowflake_object = SnowflakeQueryBuilder(data_store)
                return snowflake_object
            elif data_store == BIGQUERY:
                bigquery_object = BigqueryQueryBuilder(data_store)
                return bigquery_object
            elif data_store == POSTGRESQL or data_store == REDSHIFT:
                postgresql_object = PostgresqlQueryBuilder(data_store)
                return postgresql_object
            else:
                return False
        except Exception as e:
            return None
