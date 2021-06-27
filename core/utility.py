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

class Validator:
    def __init__(self):
        pass

    @staticmethod
    def phone_number(phone_number):
        pass

    @staticmethod
    def email(email):
        pass

    @staticmethod
    def password(email):
        pass

