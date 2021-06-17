from db_syncer import *

from psycopg2 import connect
from psycopg2._psycopg import connection, cursor

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')


class DataBaseContext:
    def __init__(self):
        try:
            conn: connection = connect(database="postgres",
                user=dbconfig.get("user", "postgres"), password=dbconfig.get("password"),
                host=dbconfig.get("host", "localhost"), port=dbconfig.get("port", "5432"))

            conn.autocommit = True
            curs: cursor = conn.cursor()

            SQL = f"CREATE DATABASE {dbconfig.get('dbname')};"
            curs.execute(SQL)

            conn.close()
            logging.info(f"{__name__}: Database Created Successfully.")
        except:
            logging.warning(f"{__name__}: Database Already Existed.")

    def __enter__(self):
        pass

    def __exit__(self):
        pass
