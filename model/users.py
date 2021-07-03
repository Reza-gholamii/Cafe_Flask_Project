from core.exceptions import UserExistError
from core.models import *
from core.manager import *
from core.utility import *
from core.exceptions import *
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
    USERS: dict = {}  # collection of all users model in cafe from database

    def __init__(self, first_name, last_name, phone_number, password, email=None, **extra_information):
        # for _id in self.__class__.USERS:
        #     user = self.__class__.USERS[_id]
        #     if user.phone_number == phone_number and user.password != password:
        #         raise UserExistError("User Already Exist in the Database.")

        # if not Validators.check_phone("09" + phone_number):
        #     raise ValidationError("Phone Number Must be Length 9.")
        # if not Validators.check_password(password):
        #     raise ValidationError("Password Minimum Length is 8.")
        # if email and not Validators.check_email(email):
        #     raise ValidationError("Email Must be Username@domain.com Form.")

        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number[-9:]
        self.email = email
        self.password = password
        self.extra_information = dumps(extra_information)

        try:
            self.number = db_manager.create(self.name, self)
            logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
        except:
            self.number = db_manager.get_id(self.name, **self.to_dict())
            logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")
        
        self.__class__.USERS[self.number] = self

    @classmethod
    def check_user(cls, phone_number: str, password: str) -> Optional[int]:
        """
        Check Exist User with Correct Password for Cashier Login
        """

        phone_number = phone_number[-9:]
        #  password = sha256(password.encode()).hexdigest()
        try:
            logging.debug(f"{__name__}: Find This Username & Password Successfully in DataBase.")
            return db_manager.get_id(cls.name, phone_number=phone_number, password=password)
        except:
            logging.warning(f"{__name__}: This Username & Password Unavailable in DataBase.")

    @classmethod
    def all_users(cls):
        """
        Create & Save Users Model from DataBase Information into the Class Attribue
        """

        for user in db_manager.read_all(cls.name):
            cls(user[0], user[1], user[2], user[3], user[4], **loads(user[5]))
        logging.debug(f"{__name__}: Read Data from DataBase Successfully.")

    def __repr__(self) -> str:
        return f"""
ID: {self.number}
First Name: {self.first_name}
Last Name: {self.last_name}
Phone Number: 09{self.phone_number}
Email Address: {self.email if self.email else '-'}
Extra Information: {self.extra_information if loads(self.extra_information) else '-'}
"""
