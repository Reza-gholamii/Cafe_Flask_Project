from abc import ABC
from psycopg2.errors import *
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
