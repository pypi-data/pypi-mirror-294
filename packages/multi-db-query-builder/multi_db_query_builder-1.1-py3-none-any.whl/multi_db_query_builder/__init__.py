import logging
from .multi_database_query_builder import *


for logger_name in ("snowflake.snowpark", "snowflake.connector"):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(threadName)s %(filename)s:%(lineno)d - %(funcName)s() - %(levelname)s - %(message)s"
        )
    )
    logger.addHandler(ch)
