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
        if db_manager.read("tables", id=table_number)[0][3] == STATUSES["tables"]["empty"]:
            self.total_price = total_price
            self.final_price = final_price
            self.status = STATUSES[self.name][status]
            self.table_number = table_number
            try:
                self.number = db_manager.create(self.name, self)
                logging.info(f"{__name__}: Model Created Successfully in {self.number} Row ID.")
            except:
                self.number = db_manager.get_id(self.name, **self.to_dict())
                logging.warning(f"{__name__}: Model Already Existed in {self.number} Row ID.")
            db_manager.update("tables", id=self.table_number, status=STATUSES["tables"]["full"])
            logging.debug(f"{__name__}: Change Status of Table Number Successfully.")
        else:
            logging.error(f"{__name__}: This Table is Occupied & Recepite it's not Possible.")

    def change_status(self, status="paid"):
        """
        Method for Change Status of Model for Example Paid, Unpaid or Canceled
        """

        self.status = STATUSES[self.name][status]
        db_manager.update(self.name, id=self.number, status=self.status)
        db_manager.update("tables", id=self.table_number, status=STATUSES["tables"]["empty"])
        logging.debug(f"{__name__}: Change Status Column(Recepite & Table) Successfully.")

    def sum_price(self):
        """
        Method for Calculate Recepite Price by Sum Order Price and Write in Attributes
        """

        details = db_manager.calculate_price(self.table_number)
        self.total_price, self.final_price = details[2], details[3]
        db_manager.update(self.name, id=self.number,
                          total_price=self.total_price, final_price=self.final_price)
        logging.info(f"{__name__}: Calculated Price has Written in DataBase.")
