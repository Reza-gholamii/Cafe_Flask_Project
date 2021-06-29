from psycopg2 import connect
from psycopg2._psycopg import connection, cursor

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')


class DataBaseContext:
    """
    Context Manager for Accessing DataBase
    """

    def __init__(self, dbconfig):
        try:
            # establishing the connection
            conn: connection = connect(database="postgres",
                user=dbconfig.get("user", "postgres"), password=dbconfig.get("password"),
                host=dbconfig.get("host", "localhost"), port=dbconfig.get("port", "5432"))

            conn.autocommit = True
            # creating a cursor object using the cursor() method
            curs: cursor = conn.cursor()

            # preparing query to create a database
            SQL = f" CREATE DATABASE {dbconfig.get('dbname')} WITH OWNER = postgres;"
            # creating a database
            curs.execute(SQL)

            # closing the connection
            conn.close()
            logging.info(f"{__name__}: Database Created Successfully.")
        except:
            logging.warning(f"{__name__}: Database Already Existed.")
        finally:
            self.config = ' '.join([key + '=' + value for key, value in dbconfig.items()])

    def __enter__(self):
        self.conn: connection = connect(self.config)
        self.curs: cursor = self.conn.cursor()

        SQL = "CREATE SCHEMA IF NOT EXISTS public;"
        self.curs.execute(SQL)
        self.conn.commit()

        return self.curs

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.conn.commit()
            self.curs.close()
            self.conn.close()
            logging.info(f"{__name__}: Execute Query Successfully.")
        else:
            logging.error(f"{__name__}: {exc_type} >>> {exc_val}")
        return True  # For ignore raising exceptions!


sql_queries_creates = [
    """
CREATE TABLE IF NOT EXISTS messages (
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
phone_number CHAR(9) NOT NULL,
email VARCHAR(100),
comment TEXT NOT NULL,
id SERIAL PRIMARY KEY);
""",
    """
CREATE TABLE IF NOT EXISTS users (
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
phone_number CHAR(9) NOT NULL UNIQUE,
email VARCHAR(100),
password CHAR(64) NOT NULL,
extra_information VARCHAR,
id SERIAL PRIMARY KEY);
""",
    """
CREATE TABLE IF NOT EXISTS statuses (
title VARCHAR(20) NOT NULL,
subtable INT,
id SERIAL PRIMARY KEY,
CONSTRAINT fk_sub
    FOREIGN KEY(subtable)
    REFERENCES statuses(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);
""",
    """
CREATE TABLE IF NOT EXISTS tables (
capacity INT NOT NULL,
position_space VARCHAR(20) NOT NULL UNIQUE,
status INT DEFAULT 12,
id SERIAL PRIMARY KEY,
CONSTRAINT fk_stat
    FOREIGN KEY(status)
    REFERENCES statuses(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);
""",
    """
CREATE TABLE IF NOT EXISTS categories (
title VARCHAR(50) NOT NULL UNIQUE,
root INT,
id SERIAL PRIMARY KEY,
CONSTRAINT fk_tree
    FOREIGN KEY(root)
    REFERENCES categories(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);
""",
    """
CREATE TABLE IF NOT EXISTS menu_items (
title VARCHAR(50) NOT NULL UNIQUE,
price INT NOT NULL,
category INT NOT NULL,
discount INT DEFAULT 0,
image_name VARCHAR(100),
cooking_time TIME,
serving_time TIME,
status INT DEFAULT 14,
id SERIAL PRIMARY KEY,
CONSTRAINT fk_group
    FOREIGN KEY(category)
    REFERENCES categories(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL,
CONSTRAINT fk_stat
    FOREIGN KEY(status)
    REFERENCES statuses(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);
""",
    """
CREATE TABLE IF NOT EXISTS recepites (
total_price INT DEFAULT 0,
final_price INT DEFAULT 0,
status INT DEFAULT 10,
table_number INT NOT NULL,
id SERIAL PRIMARY KEY,
CONSTRAINT fk_num
    FOREIGN KEY(table_number)
    REFERENCES tables(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL,
CONSTRAINT fk_stat
    FOREIGN KEY(status)
    REFERENCES statuses(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);
""",
    """
CREATE TABLE IF NOT EXISTS orders (
count INT DEFAULT 1,
status INT DEFAULT 5,
time_stamp TIMESTAMP NOT NULL,
recepite INT NOT NULL,
menu_item INT NOT NULL,
id SERIAL PRIMARY KEY,
CONSTRAINT fk_recepite
    FOREIGN KEY(recepite)
    REFERENCES recepites(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL,
CONSTRAINT fk_menu_item
    FOREIGN KEY(menu_item)
    REFERENCES menu_items(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL,
CONSTRAINT fk_stat
    FOREIGN KEY(status)
    REFERENCES statuses(id)
    ON DELETE SET NULL
    ON UPDATE SET NULL
);
"""
]

sql_queries_inserts = [
    """
INSERT INTO statuses (title, id)
VALUES ('orders', 1);
""",
    """
INSERT INTO statuses (title, id)
VALUES ('recepites', 2);
""",
    """
INSERT INTO statuses (title, id)
VALUES ('tables', 3);
""",
    """
INSERT INTO statuses (title, id)
VALUES ('menu_items', 4);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('new', 1, 5);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('cooking', 1, 6);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('serving', 1, 7);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('canceled', 1, 8);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('paid', 2, 9);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('unpaid', 2, 10);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('canceled', 2, 11);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('empty', 3, 12);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('full', 3, 13);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('active', 4, 14);
""",
    """
INSERT INTO statuses (title, subtable, id)
VALUES ('deactive', 4, 15);
"""
]
