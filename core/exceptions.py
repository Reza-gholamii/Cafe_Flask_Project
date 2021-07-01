class BaseExceptions(Exception):
    """
    A Base Model for Inheritance All Exceptions Class
    """


class UserExistError(BaseExceptions):
    """
    User Already Exist in the Database.
    """


class ValidationError(BaseExceptions):
    """
    Params isn't Validation Check by Validators Class
    """
