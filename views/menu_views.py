import core.utility as utility
import core.manager as dbmanager
import core.exceptions as exception
import model.users as user_model


def register_cashier():
    firstname = utility.inputer("enter cashier's firstname :")
    lastname = utility.inputer("enter cashier's lastname :")
    phone_number = ""
    try:
        phone_number = utility.inputer("enter cashier's phone number :",
                                       validator=utility.Validator.phone_number,
                                       retry=True,
                                       retry_print="phone number is not valid. pleas enter a valid number")
        db = dbmanager.DataBaseManager()
        res = db.read_condition("users", "phone_number", phone_number)
        if res:
            exception.UserExistError()

    except:
        print("this user exist!!..try again")
        register_cashier()

    email = utility.inputer("enter cashier's email:(optional)",
                            validator=utility.Validator.email,
                            retry=True,
                            retry_print="email is not valid. pleas enter a valid email"
                            )
    if email == "":
        email = None
    password = utility.inputer("enter cashier's password:",
                               validator=utility.Validator.password,
                               retry=True,
                               retry_print="email is not valid. pleas enter a valid email"
                               )
    u = user_model.User(firstname, lastname, phone_number, password, email)
    print(u.to_dict())

    dbmanager.DataBaseManager().create("users",u)
    print("user added successfully")
