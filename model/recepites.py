from core.models import *
from core.manager import *


db_manager = ExtraDataBaseManager()


class Recepite(BaseModel):
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
            self.number = db_manager.get_id(self.name, **self.to_dict())
            logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")

    def change_status(self, status="paid"):
        """
        Method for Change Status of Model for Example Paid, Unpaid or Canceled
        """

        self.status = db_manager.get_id("statuses", title=status)
        db_manager.update(self.name, id=self.number, status=self.status)
        logging.debug(f"{__name__}: Change Status Column Successfully in DataBase.")
