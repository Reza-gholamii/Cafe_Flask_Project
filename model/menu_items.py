from core.models import *
from core.manager import *
from datetime import time
from typing import Optional


db_manager = ExtraDataBaseManager()


class MenuItem(BaseModel):
    """
    Instances of this Class is Food in Order and has Many Attribute
    """

    name = "menu_items"
    number: int
    title: str
    price: int
    category: int
    discount: int  # Percentage
    image_name: Optional[str]  # name of picture for product
    cooking_time: Optional[time]  # Estimated cooking time
    serving_time: Optional[time]  # Serving time period
    status: int  # active or deactive in list

    def __init__(self, title, price, category, discount=0,
                 image_name=None, cooking_time=None, serving_time=None, status="active"):
        self.title = title
        self.price = price
        self.category = db_manager.get_id("categories", title=category)
        self.discount = discount
        self.image_name = image_name
        self.serving_time = serving_time
        self.cooking_time = cooking_time
        self.status = db_manager.get_id("statuses", title=status)
        try:
            self.number = db_manager.create(self.name, self)
            logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
        except:
            self.number = db_manager.get_id(self.name, **self.to_dict())
            logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")

    def apply_discount(self, discount: int):
        """
        Method for Apply Discount for Menu Item Per Unit of Percentage
        """

        db_manager.update(self.name, id=self.number, discount=discount)
        self.discount = discount
        logging.debug(f"{__name__}: Change Discount Column Successfully in DataBase.")

    def change_price(self, price: int):
        """
        Method for Change Price of Menu Item Because Inflation or ...
        """

        db_manager.update(self.name, id=self.number, price=price)
        self.price = price
        logging.debug(f"{__name__}: Change Price Column Successfully in DataBase.")

    def change_status(self, status="deactive"):
        """
        Method for Change Status of Model from active to deactive or Upside Down
        """

        self.status = db_manager.get_id("statuses", title=status)
        db_manager.update(self.name, id=self.number, status=self.status)
        logging.debug(f"{__name__}: Change Status Column Successfully in DataBase.")
