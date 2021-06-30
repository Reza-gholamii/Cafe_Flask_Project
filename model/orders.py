from core.models import *
from core.manager import *
from datetime import datetime


db_manager = ExtraDataBaseManager()


class Order(BaseModel):
    """
    List of Orders Contains Food Item Menu for Customers on Table
    """

    name = "orders"
    number: int
    count: int
    time_stamp: str
    status: int  # new or cooking or serving or canceled
    recepite: int
    menu_item: int

    def __init__(self, recepite, menu_item, count=1,
                 time_stamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status="new"):
        self.count = count
        self.status = db_manager.get_id("statuses", title=status)
        self.time_stamp = time_stamp
        self.recepite = recepite
        self.menu_item = menu_item
        try:
            self.number = db_manager.create(self.name, self)
            logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
        except:
            self.number = db_manager.get_id(self.name, **self.to_dict())
            logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")
