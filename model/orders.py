from core.models import *
from core.manager import *
from datetime import datetime
from menu_items import MenuItem


db_manager = ExtraDataBaseManager()
MenuItem.all_menu_items()


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
        flag = False
        code = db_manager.get_id("menu_items", title=menu_item)
        for category in MenuItem.MENU_ITEMS:
            for subcategory in MenuItem.MENU_ITEMS[category]:
                if code in MenuItem.MENU_ITEMS[category][subcategory]:
                    items = MenuItem.MENU_ITEMS[category][subcategory]
                    if items[code].status == STATUSES["menu_items"]["active"]:
                        flag = True

        if flag:
            self.count = count
            self.status = STATUSES[self.name][status]
            self.time_stamp = time_stamp
            self.recepite = recepite
            self.menu_item = code

            try:
                self.number = db_manager.get_id(self.name, **self.to_dict())
                logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")
            except:
                self.number = db_manager.create(self.name, self)
                logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
        else:
            logging.error(f"{__name__}: This Item isn't in the Active List.")

    def change_status(self, status):
        """
        Method for Change Status of Model for Example New, Cooking, Serving or Canceled
        """

        self.status = STATUSES[self.name][status]
        db_manager.update(self.name, id=self.number, status=self.status)
        logging.debug(f"{__name__}: Change Status Column Successfully in DataBase.")

    def change_count(self, count):
        """
        Method for Change Count of Order Menu Item from 1 to Any Number Greater than One
        """

        self.count = count
        db_manager.update(self.name, id=self.number, count=self.count)
        logging.debug(f"{__name__}: Change Count Number Column Successfully in DataBase.")
