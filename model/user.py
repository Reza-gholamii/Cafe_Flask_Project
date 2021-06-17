from core.models import BaseModels


class User(BaseModels):
    first_name: str
    last_name: str
    phone_number: str
    email: str
    password: str
    email: str = None
    extra_information: dict

    # TODO : username
    def __init__(self, first_name, last_name, phone_number, password, email, **extra_information):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone_number
        self.email = email
        self.password = password
        self.extra_information = extra_information
