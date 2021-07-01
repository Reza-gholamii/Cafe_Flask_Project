from abc import ABC
from core.utility import *
from core.exceptions import *
from typing import Optional
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')


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
        if not Validators.check_phone("09" + phone_number):
            raise ValidationError("Phone Number Must be Length 9.")
        if email and not Validators.check_email(email):
            raise ValidationError("Email Must be Username@domain.com Form.")

        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email or None
        self.comment = comment
