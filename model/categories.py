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
            self.root = db_manager.get_id(self.name, title=root)
        try:
            db_manager.create(self.name, self)
            logging.info(f"{__name__}: Model Created Successfully in DataBase.")
        except:
            logging.warning(f"{__name__}: Model Already Existed in DataBase.")

    def add_sub(self, title: str) -> int:
        """
        Method to Add New Category in Child this Category Parent
        """

        self.__class__(title, self.title)
        return db_manager.get_id(self.name, title=title)
