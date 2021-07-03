import re as regex


def inputer(text, type=str, validator: callable = None, retry=False, retry_print=""):
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


def change_status_lang(parameter):
    status_dict = {'new': 'جدید',
                   'cooking': 'در حال پخت',
                   'serving': 'سرو شده',
                   'canceled': 'کنسل شده',
                   'paid': 'پرداخت شده',
                   'unpaid': 'پرداخت نشده',
                   'empty': 'خالی',
                   'full': 'پر'
                   }
    status_dict_reverse = {value: key for key, value in status_dict.items()}

    if parameter in status_dict.keys():
        parameter = status_dict[parameter]
    elif parameter in status_dict.values():
        parameter = status_dict_reverse[parameter]

    return parameter


def change_status_lang_by_number(parameter):
    status_dict = {'5': 'جدید',
                   '6': 'در حال پخت',
                   '7': 'سرو شده',
                   '8': 'کنسل شده',
                   '9': 'پرداخت شده',
                   '10': 'پرداخت نشده',
                   '11': 'کنسل شده',
                   '12': 'خالی',
                   '13': 'پر'
                   }
    status_dict_reverse = {value: key for key, value in status_dict.items()}

    if parameter in status_dict.keys():
        parameter = status_dict[parameter]
    elif parameter in status_dict.values():
        parameter = status_dict_reverse[parameter]

    return parameter
