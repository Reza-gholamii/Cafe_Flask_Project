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
    discount: int
    image_name: Optional[str]
    cooking_time: Optional[time]  # Estimated cooking time
    serving_time: Optional[time]  # Serving time period
    status: int

    def __init__(self, title, price, category, discount=0, image_name=None, cooking_time=None, serving_time=None, status="active"):
        self.title = title
        self.price = price
        self.category = db_manager.get_id("categories", title=category)
        self.discount = discount
        self.image_name = image_name
        self.serving_time = serving_time
        self.cooking_time = cooking_time
        self.status = db_manager.get_id("statuses", title=status)
        self.number = db_manager.create(self.name, self)

    def apply_discount(self, discount):
        """
        Method for Apply Discount for Menu Item Per Unit of Percentage
        """

        db_manager.update(self.name, id=self.number, discount=discount)
        self.discount = discount

    def change_price(self, price):
        """
        Method for Change Price of Menu Item Because Inflation or ...
        """

        db_manager.update(self.name, id=self.number, price=price)
        self.price = price

    def change_status(self, status="deactive"):
        """
        Method for Change Status of Model from active to deactive or Upside Down
        """

        code = db_manager.get_id("statuses", title=status)
        db_manager.update(self.name, id=self.number, status=code)
        self.status = status
