from hashlib import sha256
from getpass import getpass

import string
import secrets
import argparse


def password_generator() -> str:
    """
    Generate Password for Admin in First time Login
    """

    alphanumeric = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphanumeric) for i in range(8))
    return password


if __name__ == '__main__':

    if True:  # must be check user table in database admin exist
        print("Admin Password:", password_generator())
        # TODO: save admin information in database with user id = 0

    parser = argparse.ArgumentParser(description="<Admin Panel>")
    parser.add_argument('-c', '--cashier', action='store_true', dest="user", help="Create User")
    parser.add_argument('-s', '--setting', action='store_true', dest="pass", help="Change Password")
    
    args = parser.parse_args()

    password = sha256(getpass("Password: ").encode()).hexdigest()
