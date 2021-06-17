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

    def __init__(self):
        pass
