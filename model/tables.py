from typing_extensions import ParamSpec
from core.models import BaseModel


class Table(BaseModel):
    """
    Information About Tables of in the Cafe for Example Cafe Position Space and ...
    """

    ID: int
    capacity: int
    position_space: str
    empty: bool

    def __init__(self, capacity, position_space, empty=True):
        self.capacity = capacity
        self.position_space = position_space
        self.empty = empty
