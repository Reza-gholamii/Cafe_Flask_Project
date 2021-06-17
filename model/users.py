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

    def __init__(self):
        pass
