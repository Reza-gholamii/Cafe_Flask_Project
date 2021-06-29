from core.models import *
from core.manager import *

db_manager = ExtraDataBaseManager()


class Category(BaseModel):
    """
    Model of Category and SubCategories in DataBase
    """

    name = "categories"
    title: str

    def __init__(self, title, root: str = None):
        self.title = title
        if root:
            self.root = db_manager.get_id(self.name, field=root)
        db_manager.create(self.name, self)
