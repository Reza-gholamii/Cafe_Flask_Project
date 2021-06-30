from core.models import *
from core.manager import *


db_manager = ExtraDataBaseManager()


class Recepites(BaseModel):
    """
    Information About Recepites for Example Price or Payment Status and ...
    """

    name = "recepites"
    number: int
    total_price: int  # without discount
    final_price: int  # with discount
    status: int  # paid or unpaid or canceled
    table_number: int

    def __init__(self, table_number, total_price=0, final_price=0, status="unpaid"):
        self.total_price = total_price
        self.final_price = final_price
        self.status = db_manager.get_id("statuses", title=status)
        self.table_number = table_number
        try:
            self.number = db_manager.create(self.name, self)
            logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
        except:
            print(self.to_dict())
            self.number = db_manager.get_id(self.name, **self.to_dict())
            logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")
Recepites(1)