from datetime import datetime
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
    serving_time: Optional[datetime] # Serving time period
    cooking_time: Optional[datetime] # Estimated cooking time

    def __init__(self):
        pass
