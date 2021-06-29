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

    def add_sub(self, title: str):
        """
        Method to Add New Category in Child this Category Parent
        """

        self.__class__.__init__(self.__class__, title, self.title)
