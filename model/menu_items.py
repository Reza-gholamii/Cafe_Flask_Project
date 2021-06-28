from datetime import time
from typing import Optional
from core.models import BaseModel


class MenuItem(BaseModel):
    """
    Instances of this Class is Food in Order and has Many Attribute
    """

    ID: int
    name: str
    price: int
    category: str
    image_name: Optional[str]
    discount: Optional[int]
    serving_time: Optional[time]  # Serving time period
    cooking_time: Optional[time]  # Estimated cooking time

    def __init__(self, name, price, category, image_name="", discount=0, status=14, serving_time=time(0), cooking_time=time(0)):
        self.name = name
        self.price = price
        self.category = category
        self.image_name = image_name
        self.discount = discount
        self.status = status
        self.serving_time = serving_time
        self.cooking_time = cooking_time
