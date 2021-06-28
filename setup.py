import menu
import views.menu_views  as menu_views
menu_dict = {
    "name": "main menu",
    "children": [{
        "name": "register cashier",
        "function": menu_views.register_cashier,
        "description": "creat new cashier"
    }
    ]
}

menu = menu.utility.generate_menu(menu_dict)
menu()

