from .exceptions import MenuGenerateError
from .models import *


def generate_menu(menu_dict: dict, parent=None) -> Menu:
    if 'children' in menu_dict:
        menu = MenuList(menu_dict['name'], parent, description=menu_dict.get('description'))
        for c in menu_dict['children']:
            generate_menu(c, menu)
    elif 'children_with_authorization' in menu_dict:
        menu = MenuList_with_authorization(menu_dict['authorization_function'], menu_dict.get('name', None),
                                           parent=parent, description=menu_dict.get('description'),
                                           access_dict=menu_dict.get('access_dict'))
        for c in menu_dict['children_with_authorization']:
            generate_menu(c, menu)

    elif 'function' in menu_dict:
        menu = MenuView(menu_dict['function'], menu_dict.get('name', None), parent=parent,
                        description=menu_dict.get('description'))
    else:
        raise MenuGenerateError()

    return menu
