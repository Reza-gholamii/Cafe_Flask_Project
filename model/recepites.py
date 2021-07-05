from core.models import *
from core.manager import *
from datetime import datetime
from model.tables import Table
from model.orders import Order

db_manager = ExtraDataBaseManager()
Table.all_tables()


class Recepite(BaseModel):
    """
    Information About Recepites for Example Price or Payment Status and ...
    """

    name = "recepites"
    number: int
    total_price: int  # without discount
    final_price: int  # with discount
    status: int  # paid or unpaid or canceled
    table_number: int

    def __init__(self, table_number, total_price=0, final_price=0, status="پرداخت نشده", num=None):
        if not num:
            if Table.TABLES[table_number].status == STATUSES["tables"]["خالی"]:
                self.total_price = total_price
                self.final_price = final_price
                self.status = STATUSES[self.name][status]
                self.table_number = table_number

                # todo: put create here is wrong, when you want retrive object
                #  from database, it add recepit again into table
                self.number = db_manager.create(self.name, self)
                logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")

                Table.TABLES[self.table_number].change_status()
                logging.debug(f"{__name__}: Change Status of Table Number Successfully.")

                self.orders = {}  # after write into database create empty list orders
            else:
                logging.error(f"{__name__}: This Table is Occupied & Recepite it's not Possible.")
        else:
            self.total_price = total_price
            self.final_price = final_price
            self.status = STATUSES[self.name][status]
            self.table_number = table_number
            self.number = num
            self.orders = {}

            temp_list = db_manager.order_list(self.number)
            for order in temp_list:
                self.add_order(order[1], order[2], order[5].strftime("%Y-%m-%d %H:%M:%S"), order[0])

    def change_status(self, status="پرداخت شده"):
        """
        Method for Change Status of Model for Example Paid, Unpaid or Canceled
        """

        self.status = STATUSES[self.name][status]
        db_manager.update(self.name, id=self.number, status=self.status)
        logging.info(f"{__name__}: Change Status Column(Recepite) Successfully.")
        Table.TABLES[self.table_number].change_status("خالی")
        logging.debug(f"{__name__}: Change Status Column(Table) Successfully.")

    def sum_price(self):
        """
        Method for Calculate Recepite Price by Sum Order Price and Write in Attributes
        """

        details = db_manager.calculate_price(self.table_number)
        self.total_price, self.final_price = details[2], details[3]
        db_manager.update(self.name, id=self.number,
                          total_price=self.total_price, final_price=self.final_price)
        logging.info(f"{__name__}: Calculated Price has Written in DataBase.")

    def add_order(self, menu_item, count=1,
                  time_stamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status="جدید"):
        """
        Add Order for this Recepite Number by a Method for Self Recepite
        """

        order = Order(self.number, menu_item, count, time_stamp, status)
        self.orders[order.number] = order
        self.sum_price()
