class BaseExceptions(Exception):
    """
    A Base Model for Inheritance All Exceptions Class
    """


class UserNotFoundError(BaseException):
    """
    user is not in database
    """


class UserExistError(BaseExceptions):
    """
    User Already Exist in the Database.
    """


class ValidationError(BaseExceptions):
    """
    Params isn't Validation Check by Validators Class
    """


class MenuGenerateError(BaseExceptions):
    """
    menu generator error
    """
