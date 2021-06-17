from typing import Optional
from core.models import BaseModel


class User(BaseModel):
    """
    Signing up Cashier Users for Access to Dashboard Panel
    """

    ID: int
    first_name: str
    last_name: str
    phone_number: str
    emial: Optional[str]
    password: str
    extra_information: dict

    def __init__(self, first_name, last_name, phone_number, password, email = None, **extra_information):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.extra_information = extra_information
