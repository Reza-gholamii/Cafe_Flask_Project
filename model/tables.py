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
    status: int  # empty or full
    TABLES: dict = {}  # collection of all tables model in cafe from database

    def __init__(self, capacity, position_space, status="empty"):
        self.capacity = capacity
        self.position_space = position_space
        self.status = db_manager.get_id("statuses", title=status)
        try:
            self.number = db_manager.create(self.name, self)
            logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
        except:
            self.number = db_manager.get_id(self.name, **self.to_dict())
            logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")

    def change_status(self, status="full"):
        """
        Method for Change Status of Model from empty to full or Upside Down
        """

        self.status = db_manager.get_id("statuses", title=status)
        db_manager.update(self.name, id=self.number, status=self.status)
        logging.debug(f"{__name__}: Change Status Column Successfully in DataBase.")

    @classmethod
    def all_tables(cls):
        """
        Create & Save Tables Model from DataBase Information into the Class Attribue
        """

        for table in db_manager.read_all(cls.name):
            status = db_manager.read("statuses", table[2])[0]
            t = cls(table[0], table[1], status)
            cls.TABLES[t.number] = t
