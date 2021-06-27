import re as regex


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
        Check Validetion of Phone Number and Return Boolean Value
        Example Valid Number: 09123456789(Start with 09 lenght 11)
        """

        return bool(regex.search(cls.phone_pattern, phone_number))


    @classmethod
    def check_email(cls, email_address: str) -> bool:
        """
        Check Validetion of Email Address and Return Boolean Value
        Example Valid Address: Username@domain.com
        """

        return bool(regex.search(cls.email_pattern, email_address))

    @classmethod
    def check_password(cls, password: str) -> bool:
        """
        Check Validetion of Password and Return Boolean Value
        Example Password: abcd1234...(minimum lenght 8 without space)
        """

        return bool(regex.search(cls.password_pattern, password))
