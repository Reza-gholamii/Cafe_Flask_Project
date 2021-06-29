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
    phone_number: str  # phone number is string with length 9 char without 09 in first
    email: Optional[str]  # check validation of params in core.utility class Validators
    password: str  # password must be hashed by sha256 algorithm and save into database
    extra_information: dict  # extra information is a dict and convert to json for save

    def __init__(self, first_name, last_name, phone_number, password, email=None, **extra_information):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number[2:]
        self.email = email
        self.password = sha256(password.encode()).hexdigest()
        self.extra_information = dumps(extra_information)
        self.number = db_manager.create(self.name, self)

    def check_user(self) -> bool:
        pass

    def __repr__(self) -> str:
        return f"""
ID: {self.number}
First Name: {self.first_name}
Last Name: {self.last_name}
Phone Number: 09{self.phone_number}
Email Address: {self.email if self.email else '-'}
Extra Informations: {self.extra_information if self.extra_information else '-'}
"""
