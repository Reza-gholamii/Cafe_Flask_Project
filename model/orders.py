from datetime import datetime
from core.models import BaseModel


class Order(BaseModel):
    """
    List of Orders Contains Food Item Menu for Customers on Table
    """

    ID: int
    status: bool # present or not
    timestamp: datetime # object of datetime class
    # Forigen Key Reference to Recepites ID
    # Forigen Key Reference to Menu Items ID

    def __init__(self):
        pass
