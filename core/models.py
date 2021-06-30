from manager import *
from abc import ABC
from typing import Optional
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')

db_manager = ExtraDataBaseManager()


class BaseModel(ABC):
    """
    A Base Model for Inheritanced All Entities Class Models
    """

    def to_dict(self) -> dict:
        """
        This Method Returned All Attributes of the self instance
        """

        return vars(self)


class TextMessage(BaseModel):
    """
    Create Object From a Text Message to Write into DataBase with DBManager
    """

    def __init__(self, first_name: str, last_name: str, phone_number: int, email: Optional[str], comment: str):
        # TODO: check validation input value with class in core.utility and raise exceptions
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email or None
        self.comment = comment


STATUSES = {key[1]: {} for key in db_manager.category_list(False, table="statuses")}
counter = 1
for root in STATUSES:
    STATUSES[root] = {key[1]: key[0] for key in db_manager.category_list(True, root, "statuses")}
