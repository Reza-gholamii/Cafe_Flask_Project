import re as regex


def inputer(text, type=str, validator: callable = None, retry=False,retry_print=""):
    try:
        res = type(input(text))
        if validator:
            if validator(res):
                return res
    except:
        if retry:
            print(retry_print)
            inputer(text, type, validator, retry)

    return res


class Validators:
    """
    Check Validation of the All the Input Values
    """

    phone_pattern = r"^(09)([0-9]{9})$"
    email_pattern = r"^([\w\.\_\-]+)[@]([\w\.\_\-]*\w)[.]([A-Za-z]{2,3})$"
    password_pattern = r"^([^ ]{8,})$"

    @classmethod
    def check_phone(cls, phone_number: str) -> bool:
        """
        Check Validation of Phone Number and Return Boolean Value
        Example Valid Number: 09123456789(Start with 09 length 11)
        """

        return bool(regex.search(cls.phone_pattern, phone_number))

    @classmethod
    def check_email(cls, email_address: str) -> bool:
        """
        Check Validation of Email Address and Return Boolean Value
        Example Valid Address: Username@domain.com
        """

        return bool(regex.search(cls.email_pattern, email_address))

    @classmethod
    def check_password(cls, password: str) -> bool:
        """
        Check Validation of Password and Return Boolean Value
        Example Password: abcd1234...(minimum length 8 without space)
        """

        return bool(regex.search(cls.password_pattern, password))