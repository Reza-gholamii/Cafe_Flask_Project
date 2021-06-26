from abc import ABC
from typing import Optional


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
