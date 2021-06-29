from core.models import *
from core.manager import *
from typing import Optional
from json import dumps, loads
from hashlib import sha256

db_manager = ExtraDataBaseManager()


class User(BaseModel):
    """
    Signing up Cashier Users for Access to Dashboard Panel
    """

    name = "users"
    number: int
    first_name: str
    last_name: str
    phone_number: str  # phone number is a string with length 9 char without 09 in first
    email: Optional[str]  # check validation of params in core.utility class Validators
    password: str  # password must be hashed by sha256 algorithm and save into database
    extra_information: dict  # extra information is a dict and convert to json for save

    def __init__(self, first_name, last_name, phone_number, password, email=None, **extra_information):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.extra_information = extra_information
        # Create method in DataBaseManager
