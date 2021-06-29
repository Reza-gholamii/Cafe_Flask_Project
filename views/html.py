from flask import render_template, request, redirect, make_response, Response
from flask.helpers import url_for
from datetime import timedelta

import model.users
from core.manager import ExtraDataBaseManager, DataBaseManager
from core.models import TextMessage, BaseModel
from model.menu_items import MenuItem

from model import users
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')

db_manager = ExtraDataBaseManager()

status_dict = {'new': 'جدید', 'cooking': 'در حال پخت', 'serving': 'سرو شده', 'canceled': 'کنسل شده'}


def home():
    return render_template("home.html", page_name="home")


def about_us():
    return render_template("about_us.html", page_name="about_us")


def contact_us():
    """
    Manage The Request to Contact US Page for Example Just See or Send Message
    """

    if request.method == 'GET':
        return render_template("contact_us.html")

    else:
        _vars = dict(request.form)
        message = TextMessage(**_vars)
        # TODO: use try and except for exceptions handeling after check validate
        db_manager.create(table="messages", model=message)
        logging.info(f"{__name__}: Message has Written into the DataBase")
        # TODO: show alert for send message successfully and next ...?
        return redirect(url_for('home'))


def menu():
    return render_template("menu.html", page_name="menu")


# fro here all are for cashier side


# this is for test

orders = [("۱", "۳۲۵", "جدید", "رضا غلامی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۲", "۳۲۵", "جدید", "رضا یزدانی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۳", "۳۲۵", "جدید", "علی غلامی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۴", "۳۲۵", "جدید", "رسول احدی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۵", "۳۲۵", "جدید", "س‍پهر بازیار", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۶", "۳۲۵", "جدید", "علی احدی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۷", "۳۲۵", "جدید", "ممد نادیجی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲")]


def order_list(_id):
    if request.method == "GET":
        # tables_info = db_manager.read_all('tables')
        # tables_numbers = [i[3] for i in tables_info]
        # orders = []
        # for tables_number in tables_numbers:
        #     print(tables_number)
        #     # I think this query does not work correctly, since recepites.status = 8 while 8 is for orders
        #     receipts_number = db_manager.calculate_price(tables_number)
        #     print(receipts_number)
        #     orders += db_manager.order_list(receipts_number[0])
        # print(orders)
        # # need call a function to get access to last orders based on tables
        return render_template("cashier/order_list.html", orders=orders)
    else:
        json_data = request.get_json()
        # print(json_data['status'])
        # data must be updated in database
        return render_template('cashier/order_list.html', orders=orders)


# this is for test


def menu_items(_id):
    if request.method == "GET":
        items = db_manager.read_all('menu_items')
        items.sort(key=lambda x: x[8])
        return render_template("cashier/menu_items.html", items=items, id=_id)
    else:
        json_data = request.get_json()
        if json_data['action'] == "delete":
            item_id = db_manager.get_id('menu_items', title=json_data['name'])
            db_manager.delete('menu_items', item_id)
        elif json_data['action'] == "update":
            item_id = db_manager.get_id('menu_items', title=json_data['name'])
            db_manager.update('menu_items', id=item_id, title=json_data['name'], price=json_data['price'])
        elif json_data['action'] == "add":
            new_item = MenuItem(name=json_data['name'], price=json_data['price'], category=2)
            db_manager.create('menu_items', new_item)
        items = db_manager.read_all('menu_items')
        items.sort(key=lambda x: x[8])
        return render_template("cashier/menu_items.html", items=items, id=_id)


# this is for test
#
served_orders = [("۳۲۵", "۱", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۲", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۶", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۴", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۴", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۶", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۷", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲")]


#
# all_orders = orders.copy()


def archive_list(_id):
    all_orders_l = []
    all_orders = db_manager.read_all('orders')
    for order in all_orders:
        menu_item = db_manager.read('menu_items', row_id=order[4])
        item_name = menu_item[0][0]
        item_category_id = menu_item[0][2]
        item_category = db_manager.read('categories', row_id=item_category_id)
        status = db_manager.read('statuses', row_id=order[1])
        status_name = status[0][0]
        order_l = list(order)
        order_l[4], order_l[1] = item_name, status_name
        order_l.append(item_category[0][0])
        all_orders_l.append(order_l)
    if request.method == "GET":
        return render_template("cashier/archive_list.html", orders=all_orders_l, id=_id)
    else:
        json_data = request.get_json()
        status_dict_reverse = {}
        for key, value in status_dict.items(): status_dict_reverse.update({value: key})
        status_id = db_manager.get_id('statuses', title=status_dict_reverse[json_data['status']])
        db_manager.update('orders', id=json_data['index'], status=status_id)
        return render_template("cashier/archive_list.html", orders=all_orders_l, id=_id)


def new_order_list(_id):
    if request.method == "GET":
        # served_orders = db_manager.statusfilter('orders', status='serving')
        # print(served_orders)
        return render_template("cashier/new_orders_list.html", orders=served_orders)
    else:
        return render_template("cashier/new_orders_list.html", orders=served_orders)


def cooking_order_list(_id):
    if request.method == "GET":
        # served_orders = db_manager.statusfilter('orders', status='serving')
        # print(served_orders)
        return render_template("cashier/cooking_orders_list.html", orders=served_orders)
    else:
        return render_template("cashier/cooking_orders_list.html", orders=served_orders)


def served_order_list(_id):
    if request.method == "GET":
        # served_orders = db_manager.statusfilter('orders', status='serving')
        # print(served_orders)
        return render_template("cashier/served_orders_list.html", orders=served_orders)
    else:
        return render_template("cashier/served_orders_list.html", orders=served_orders)


def paid_order_list(_id):
    if request.method == "GET":
        # served_orders = db_manager.statusfilter('orders', status='serving')
        # print(served_orders)
        return render_template("cashier/paid_orders_list.html", orders=served_orders)
    else:
        return render_template("cashier/paid_orders_list.html", orders=served_orders)


def cancelled_order_list(_id):
    if request.method == "GET":
        # served_orders = db_manager.statusfilter('orders', status='serving')
        # print(served_orders)
        return render_template("cashier/cancelled_orders_list.html", orders=served_orders)
    else:
        return render_template("cashier/cancelled_orders_list.html", orders=served_orders)


# this is test for tables status
empty_table = [1, 3, 4, 7]


def dashboard(_id):
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)
        user = model.users.User(user_data[0], user_data[1], user_data[2], user_data[4], user_data[3])
    else:
        return user_seter()
    # ''''''''''''''''''''
    data = {
        'count_new_orders': len(orders),
        'count_orders': len(orders) + len(served_orders),
        'count_empty_tables': len(empty_table),
        'count_view': 15
    }
    return render_template('cashier/dashboard.html', user={'name': 'حسابدار'}, data=data)


def login():
    if request.method == "GET":
        return render_template("cashier/login_cachier.html")
    elif request.method == "POST":
        resp = request.form
        print(resp)
        try:
            user = DataBaseManager().check_record("users", phone_number=resp["username"])[0]
        except:
            return render_template("cashier/login_cachier.html", condition="warning")

        # TODO: hash

        if user[-3] == resp["password"]:
            html_str = redirect(f"/cashier/{user[-1]}")
            response = make_response(html_str)
            response.set_cookie(
                '_ID', user[-1], max_age=timedelta(weeks=1))
            return response
        else:
            return render_template("cashier/login_cachier.html", condition="warning")


def tables(_id):
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)
        user = model.users.User(user_data[0], user_data[1], user_data[2], user_data[4], user_data[3])
    else:
        return user_seter()
    # ''''''''''''''''''''
    tables = ExtraDataBaseManager().read_all("tables")
    # TODO: where is order number?
    print("where are here")
    print(tables)
    #
    return render_template("cashier/tables.html", tables=tables, user=user)


def charts():
    return 'charts page'


def user_seter():
    """
    this is not flask function .
    this function just check cookie and return user if it exists
    """
    cookies = request.cookies
    if cookies.get("_id"):
        id = cookies.get("_id")
        u = DataBaseManager().read("users", id)
        print(u)
        return int(id)
    else:
        return redirect("login")
