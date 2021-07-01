from abc import ABC, abstractmethod
from core.models import BaseModel
from typing import List, Tuple
from psycopg2 import connect
from psycopg2._psycopg import connection, cursor
from contextlib import contextmanager
from db_syncer import config


class BaseManager(ABC):
    """
    A Base Model for Inheritanced All Managers for Example DataBase or File...
    """

    @abstractmethod
    def create(self, table: str, model: BaseModel):
        """
        Create New Row in DataBase Table By Model and to_dict Method
        """

    @abstractmethod
    def read(self, table: str, row_id):
        """
        Read Data from DataBase and Return All of the Columns
        """

    @abstractmethod
    def update(self, table: str, **kwargs):
        """
        Update Information of a Model in the DataBase with Row ID
        """

    @abstractmethod
    def delete(self, table: str, row_id):
        """
        Delete a Model by Row ID from the DataBase Table
        """


class DataBaseManager(BaseManager):
    """
    Managed DataBase Tables to CRUD Data of Models
    """

    def create(self, table: str, model: BaseModel) -> int:
        attrs: dict = model.to_dict()
        dict_values = tuple(attrs.values())
        value_num = '%s, ' * len(dict_values)
        query = f"INSERT INTO {table} VALUES ({value_num[:-2]});"
        self.send_query(query, dict_values)
        return self.get_id(table, **attrs)  # for get id after insert value into table

    def read(self, table, row_id):
        query = f"SELECT * FROM {table} where id={row_id}"
        with self.access_database() as db_cursor:
            db_cursor.execute(query)
            return db_cursor.fetchall()

    # '''''''''''''''''''
    def read_condition(self, table, condition_row_name, condition):
        query = f"SELECT * FROM {table} where {condition_row_name}='{condition}'"
        with self.access_database() as db_cursor:
            db_cursor.execute(query)
            return db_cursor.fetchall()

    # '''''''''''''''''''''

    def update(self, table, **kwargs):
        set_string = ""
        condition_string_key = list(kwargs.keys())[0]
        condition_string_value = kwargs[condition_string_key]
        condition_string = f"{condition_string_key}='{condition_string_value}'"
        kwargs.pop(condition_string_key)
        for key, value in kwargs.items():
            set_string += f"{key}='{value}', "
        query = f"UPDATE {table} SET {set_string[:-2]} where {condition_string}"
        self.send_query(query)

    def delete(self, table, row_id):
        query = f"DELETE FROM {table} where id={row_id}"
        self.send_query(query)

    def get_id(self, table, **kwargs):
        condition = ""
        for column, value in kwargs.items():
            if column != "time_stamp":
                if value is not None:
                    condition += f"{table}.{column}='{value}' and "
                else:
                    condition += f"{table}.{column} IS NULL and "
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

    # Read All Data Methods ...

    def send_query(self, query, data=None):
        with self.access_database() as db_cursor:
            db_cursor.execute(query, data)

    @contextmanager
    def access_database(self):
        conn: connection = connect(config)
        curs: cursor = conn.cursor()
        yield curs
        curs.close()
        conn.commit()
        conn.close()


class ExtraDataBaseManager(DataBaseManager):
    """
    Extra Methods for DataBase Manager Executed the Other Queries
    """

    def bestsellers(self, size: int = 3) -> List[tuple]:
        """
        Query to Find the Best Selling Products
        """

        query = """
SELECT menu_items.id, title, SUM(orders.count) AS Sellers
FROM orders INNER JOIN menu_items
ON orders.menu_item = menu_items.id
GROUP BY menu_items.id
ORDER BY Sellers DESC;
"""

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query)
            result = cafe_cursor.fetchmany(size)

        return result

    def statusfilter(self, table: str, status: str) -> List[int]:
        """
        Query to Get Empty Table or Payment Recepites or Present Order...
        """

        query = f"""
SELECT {table}.id FROM {table}
INNER JOIN statuses ON {table}.status = statuses.id
WHERE statuses.title = '{status}';
"""

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query)
            result = cafe_cursor.fetchall()  # list contains single member tuple (id,)

        return [item[0] for item in result]

    def read_all(self, table: str, limit: int = None, offset: int = None, status: bool = True) -> List[tuple]:
        """
        Query to SELECT All Row & Columns from a Table with Limit Opional
        """

        query = f"SELECT * FROM {table}"

        if status:
            query += f" ORDER BY {table}.status"

        if limit:
            query += f" LIMIT {limit}"

            if offset:
                query += f" OFFSET {(offset - 1) * limit}"

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query + ';')
            result = cafe_cursor.fetchall()

        return result

    def category_list(self, sub: bool = True, root: str = None, table: str = "categories") -> List[Tuple[int, str]]:
        """
        List of Category or Sub Categories And Show All or Filter by Root
        """

        query = f"""
SELECT id, title FROM {table}
WHERE root IS {'NOT NULL' if sub else 'NULL'}
"""

        if root:
            with self.access_database() as cafe_cursor:
                cafe_cursor.execute(f"SELECT id FROM {table} WHERE title = '{root}';")
                index = cafe_cursor.fetchone()

            query += f" AND root = {index[0]}"

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query + ';')
            result = cafe_cursor.fetchall()

        return result

    def order_list(self, recepite_number: int) -> List[tuple]:
        """
        Get List of Orders by One Recepite Number
        """

        query = f"""
SELECT statuses.title, menu_items.title, orders.count, menu_items.price, menu_items.discount
FROM recepites INNER JOIN orders ON orders.recepite = recepites.id
INNER JOIN menu_items ON orders.menu_item = menu_items.id
INNER JOIN statuses ON orders.status = statuses.id
WHERE recepites.id = {recepite_number};
"""
        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query)
            result = cafe_cursor.fetchall()

        return result

    def calculate_price(self, table_number: int) -> Tuple[int, str, int, int]:
        """
        Calculate Total Price and Final Price for One Table & Recepite Number
        """

        query = f"""
SELECT MAX(recepites.id) AS Recepite, MAX(statuses.title) AS Status,
SUM(orders.count * menu_items.price) AS Total,
SUM(orders.count * (menu_items.price * (1 - (menu_items.discount / 100)))) AS Final
FROM recepites INNER JOIN orders ON orders.recepite = recepites.id
INNER JOIN menu_items ON orders.menu_item = menu_items.id
INNER JOIN statuses ON recepites.status = statuses.id
WHERE recepites.table_number = {table_number} AND recepites.status = 10 AND orders.status <> 8;
"""

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query)
            result = cafe_cursor.fetchone()

        return result

    def incoming(self, day: str = None) -> int:
        """
        Calculate Incoming of Orders in One Day or All Days
        """

        query = f"""
SELECT SUM(count * price * (1 - (discount / 100)))
FROM orders INNER JOIN menu_items
ON orders.menu_item = menu_items.id
WHERE orders.status <> 6"""

        if day:
            query += f" AND time_stamp::DATE = '{day}'"

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query + ';')
            result = cafe_cursor.fetchone()

        return result[0]

    def archive_orders_list(self, ordered: str = "status") -> List[Tuple[int, int, str, str, int, str, str]]:
        """
        Return Full Archive of All Orders with All Field & Order by Status or Recepite Number
        """

        query = f"""
SELECT orders.id, orders.recepite, menu_items.title, category.title, orders.count,
statuses.title, orders.time_stamp FROM orders ORDER BY orders.{ordered}
INNER JOIN statuses ON orders.status = statuses.id
INNER JOIN menu_items ON orders.menu_item = menu_items.id
INNER JOIN categories ON menu_items.category = categories.id
"""

        with self.access_database() as cafe_cursor:
            cafe_cursor.execute(query)
            result = cafe_cursor.fetchall()

        return result


db_manager = ExtraDataBaseManager()
STATUSES = {key[1]: {} for key in db_manager.category_list(False, table="statuses")}
for root in STATUSES:
    STATUSES[root] = {key[1]: key[0] for key in db_manager.category_list(True, root, "statuses")}
