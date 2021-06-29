from core.models import *
from core.manager import *
from typing import Optional
from json import dumps, loads
from hashlib import sha256
import logging


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')

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
        self.phone_number = phone_number
        self.email = email
        self.password = password
        self.extra_information = dumps(extra_information)
        try:
            self.number = db_manager.create(self.name, self)
            logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
        except:
            self.number = db_manager.get_id(self.name, **self.to_dict())
            logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")

    @classmethod
    def check_user(cls, phone_number: str, password: str) -> Optional[int]:
        """
        Check Exist User with Correct Password for Cashier Login
        """

        phone_number = phone_number[2:]
        password = sha256(password.encode()).hexdigest()
        try:
            logging.debug(f"{__name__}: Find This Username & Password Successfully in DataBase.")
            return db_manager.get_id(cls.name, phone_number=phone_number, password=password)
        except:
            logging.warning(f"{__name__}: This Username & Password Unavailable in DataBase.")

    def __repr__(self) -> str:
        return f"""
ID: {self.number}
First Name: {self.first_name}
Last Name: {self.last_name}
Phone Number: 09{self.phone_number}
Email Address: {self.email if self.email else '-'}
Extra Information: {self.extra_information if loads(self.extra_information) else '-'}
"""
