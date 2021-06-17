from core.models import BaseModel


class Table(BaseModel):
    """
    Information About Tables of in the Cafe for Example Cafe Position Space and ...
    """

    ID: int
    number: int
    position_space: str

    def __init__(self):
        pass
