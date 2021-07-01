class BaseExceptions(Exception):
    """
    A Base Model for Inheritance All Exceptions Class
    """

class UserExistError(BaseExceptions):
    """
    User Already Exist in the Database.
    """


class UserNotFoundError(BaseExceptions):
    """
    User Not Found in the Database.
    """

