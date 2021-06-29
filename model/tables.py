from core.models import *
from core.manager import *

db_manager = ExtraDataBaseManager()


class Table(BaseModel):
    """
    Information About Tables of in the Cafe for Example Cafe Position Space and ...
    """

    name = "tables"
    number: int
    capacity: int
    position_space: str
    status: int

    def __init__(self, capacity, position_space, status="empty"):
        self.capacity = capacity
        self.position_space = position_space
        self.status = db_manager.get_id("statuses", title=status)
        self.number = db_manager.create(self.name, self)

    def change_status(self, status="full"):
        """
        Method for Change Status of Model from empty to full or Upside Down
        """

        code = db_manager.get_id("statuses", title=status)
        db_manager.update(self.name, id=self.number, status=code)
