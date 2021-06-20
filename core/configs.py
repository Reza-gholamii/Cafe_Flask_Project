from db_syncer import *

from psycopg2 import connect
from psycopg2._psycopg import connection, cursor

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')


class DataBaseContext:
    """
    Context Manager for Accessing DataBase
    """

    def __init__(self):
        try:
            # establishing the connection
            conn: connection = connect(database="postgres",
                user=dbconfig.get("user", "postgres"), password=dbconfig.get("password"),
                host=dbconfig.get("host", "localhost"), port=dbconfig.get("port", "5432"))

            conn.autocommit = True
            # creating a cursor object using the cursor() method
            curs: cursor = conn.cursor()

            # preparing query to create a database
            SQL = f"CREATE DATABASE {dbconfig.get('dbname')} WITH OWNER = postgres;"
            # creating a database
            curs.execute(SQL)

            # closing the connection
            conn.close()
            logging.info(f"{__name__}: Database Created Successfully.")
        except:
            logging.warning(f"{__name__}: Database Already Existed.")

    def __enter__(self):
        self.conn: connection = connect(config)
        self.curs: cursor = self.conn.cursor()
        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.conn.commit()
            self.curs.close()
            self.conn.close()
            logging.info(f"{__name__}: Execute Query Successfully.")
        return True  # For ignore raising exceptions!


sql_queries = [
    """
CREATE TABLE users (
first_name CHAR(50) NOT NULL,
last_name CHAR(50) NOT NULL,
phone_number CHAR(11) NOT NULL,
email CHAR(100),
password CHAR(100) NOT NULL,
extra_information JSON NOT NULL,
id SERIAL PRIMARY KEY);
""",
    """
CREATE TABLE tables (
table_number INT NOT NULL,
position_space CHAR(20) NOT NULL,
id SERIAL PRIMARY KEY);
""",
    """
CREATE TABLE menu_items (
name CHAR(50) NOT NULL,
price INT NOT NULL,
category CHAR(20) NOT NULL,
image_name CHAR(100),
discount INT,
serving_time TIME,
cooking_time TIME,
id SERIAL PRIMARY KEY);
""",
    """
CREATE TABLE recepites (
total_price INT NOT NULL,
final_price INT NOT NULL,
status BOOLEAN NOT NULL,
table_num INT NOT NULL,
id SERIAL PRIMARY KEY,
CONSTRAINT fk_num
    FOREIGN KEY(table_num)
    REFERENCES tables(table_number)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);
""",
    """

"""
]