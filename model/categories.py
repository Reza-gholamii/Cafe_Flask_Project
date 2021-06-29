from abc import ABC, abstractmethod
from core.models import *
from core.manager import *


db_manager = ExtraDataBaseManager()


class Node(ABC):
    def __init__(self, parent=None):
        self.parent = parent
        self.child = []
        if self.parent:
            self.parent.child.append(self)


class Category(BaseModel, Node):
    """
    Model of Category and SubCategories in DataBase
    """

    title: str

    def __init__(self, title, root=None):
        super().__init__(root)
        self.title = title
        if root:
            self.root = root.title
        db_manager.create("categories", self)
