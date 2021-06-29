from core.models import *
from core.manager import *

db_manager = ExtraDataBaseManager()


class Category(BaseModel):
    """
    Model of Category and SubCategories in DataBase
    """

    title: str

    def __init__(self, title, root: str = None):
        self.title = title
        if root:
            self.root = db_manager.get_id("categories", field=root)
        db_manager.create("categories", self)
