from core.models import *
from core.manager import *

db_manager = ExtraDataBaseManager()


class Table(BaseModel):
    """
    Information About Tables of in the Cafe for Example Cafe Position Space and ...
    """

    number: int
    capacity: int
    position_space: str
    status: int

    def __init__(self, capacity, position_space, status="empty"):
        self.capacity = capacity
        self.position_space = position_space
        self.status = db_manager.get_id("statuses", title=status)
        self.number = db_manager.create("tables", self)
