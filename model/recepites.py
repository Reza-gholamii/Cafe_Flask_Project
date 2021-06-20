from core.models import BaseModel


class Recepites(BaseModel):
    """
    Information About Recepites for Example Price or Payment Status and ...
    """

    ID: int
    total_price: int
    final_price: int # with discount
    status: bool # payment or not
    # Forigen Key Reference to Table ID

    def __init__(self, total_price, final_price, status=False):
        self.total_price = total_price
        self.final_price = final_price
        self.status = status
