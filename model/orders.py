from datetime import datetime
from core.models import BaseModel


class Order(BaseModel):
    """
    List of Orders Contains Food Item Menu for Customers on Table
    """

    ID: int
    time_stamp: datetime # object of datetime class
    status: bool # present or not
    # Forigen Key Reference to Recepites ID
    # Forigen Key Reference to Menu Items ID

    def __init__(self, time_stamp, status=False):
        self.time_stamp = time_stamp
        self.status = status
