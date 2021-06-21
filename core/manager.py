import json
import logging
from abc import ABC, abstractmethod
from db_syncer import config as dbconfig
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from contextlib import contextmanager
from .exceptions import *


class BaseManager(ABC):
    """
    A Base Model for Inheritanced All Managers for Example DataBase or File...
    """

    @abstractmethod
    def create(self, table, model):
        """
        Create New Row in DataBase Table By Model and to_dict Method
        """

    @abstractmethod
    def read(self, table, row_id):
        """
        Read Data from DataBase and Return All of the Columns
        """

    @abstractmethod
    def update(self, table, **kwargs):
        """
        Update Information of a Model in the DataBase with Row ID
        """

    @abstractmethod
    def delete(self, table, row_id):
        """
        Delete a Model by Row ID from the DataBase Table
        """


class BaseDataBaseManager(BaseManager):
    """
    Managed DataBase Tables to CRUD Data of Models
    """

    def create(self, table, model):
        pass

    def read(self, table, row_id):
        pass

    def update(self, table, **kwargs):
        pass

    def delete(self, table, row_id):
        pass


class DataBaseManager(BaseDataBaseManager):

    def create(self, table, model):
        attrs: dict = model.to_dict()
        dict_values = tuple(attrs.values())
        value_num = '%s, ' * len(dict_values)
        query = f"INSERT INTO {table} VALUES ({value_num[:-2]});"
        self.send_query(query, dict_values)

    def delete(self, table, row_id):
        query = f"DELETE FROM {table} where id={row_id}"
        self.send_query(query)

    def get_id(self, table, **kwargs):
        condition = ""
        for column, value in kwargs.items():
            condition += f"{table}.{column}='{value}' and "
        query = f"SELECT {table}.id from {table} where {condition[:-5]};"
        with self.access_database() as db_cursor:
            db_cursor.execute(query)
            return db_cursor.fetchone()[0]

    def check_record(self, table, **kwargs):
        condition_string = ''
        for key, value in kwargs.items():
            condition_string += f"{key}='{value}' and "
        query = f"SELECT * from {table} where {condition_string[:-5]};"
        with self.access_database() as db_cursor:
            db_cursor.execute(query)
            return db_cursor.fetchall()

    # Read All Data Method ...

    def send_query(self, query, data=None):
        with self.access_database() as db_cursor:
            db_cursor.execute(query, data)

    @contextmanager
    def access_database(self):
        conn: connection = connect(dbconfig.config)
        curs: cursor = conn.cursor()
        yield curs
        curs.close()
        conn.commit()
        conn.close()


class ExtraDataBaseManager(DataBaseManager):
    """
    Extra Methods for DataBase Manager Executed the Other Queries
    """

    def bestsellers(self, size: int = 3):
        """
        Query to Find the Best Selling Products
        """

        query = """
SELECT menu_items.name, COUNT(orders.menu_item) AS Sale
FROM orders INNER JOIN menu_items
ON orders.menu_item = menu_items.id
GROUP BY menu_item
ORDER BY COUNT(orders.menu_item) DESC;
"""

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query)
            return cafe_cursor.fetchmany(size)
