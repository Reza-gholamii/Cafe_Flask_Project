from abc import ABC, abstractclassmethod


class BaseModels(ABC):

    def to_dict(self):
        return vars(self)
