from core.models import *
from core.manager import *


db_manager = ExtraDataBaseManager()


class Category(BaseModel):
    """
    Model of Category and SubCategories in DataBase
    """

    name = "categories"
    title: str
    CATEGORIES: dict = {}  # collection of all category model in cafe from database

    def __init__(self, title, root: str = None):
        if not self.__class__.CATEGORIES:
            self.__class__.all_categories()

        self.title = title
        if root:
            self.root = db_manager.get_id(self.name, title=root)
            self.__class__.CATEGORIES[root][self.title] = {}
        else:
            self.__class__.CATEGORIES[self.title] = {}

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
    
    @classmethod
    def all_categories(cls):
        """
        Create & Save Categories Model from DataBase Information into the Class Attribue
        """

        parents = [key[1] for key in db_manager.category_list(False)]
        for parent in parents:
            cls(parent)
            for child in db_manager.category_list(True, parent):
                cls(child, parent)

        logging.debug(f"{__name__}: Read Data from DataBase Successfully.")
