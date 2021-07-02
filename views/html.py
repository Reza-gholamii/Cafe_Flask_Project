from flask import render_template, request, redirect, make_response, Response
from flask.helpers import url_for
from datetime import timedelta
from core.utility import *
import model.users
from core.manager import ExtraDataBaseManager, DataBaseManager
from core.models import TextMessage, BaseModel
from model.menu_items import MenuItem

from model import users
import logging

from model.tables import Table
from model.recepites import Recepite

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')

db_manager = ExtraDataBaseManager()

status_dict = {'new': 'جدید', 'cooking': 'در حال پخت', 'serving': 'سرو شده', 'canceled': 'کنسل شده'}

from core.manager import *


def viewer():
    with open("views.log", "a+") as file:
        _v = int(file.readline())+1
        file.write(str(_v))


def home():
    viewer()
    return render_template("home.html", page_name="home")


def about_us():
    viewer()
    return render_template("about_us.html", page_name="about_us")


def contact_us():
    """
    Manage The Request to Contact US Page for Example Just See or Send Message
    """

    viewer()
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


def order_list(_id):
    if request.method == "GET":
        Table.all_tables()
        tables_id = list(Table.TABLES.keys())
        recepits, orders = [], []
        for table_id in tables_id:
            recepit = list(db_manager.calculate_price(table_id))
            if recepit[0]:
                recepit.insert(0, table_id)
                order = db_manager.order_list(recepit[1])
                recepit[2] = change_status_lang(recepit[2])
                order_l = []
                for item in order:
                    item = list(item)
                    item[0] = change_status_lang(item[0])
                    order_l.append(item)

            else:
                recepit = ["" for i in recepit]
                recepit.insert(0, table_id)
                recepit.insert(4, "0")
                order_l = []
            recepits.append(recepit)
            orders.append(order_l)
        return render_template('cashier/order_list.html', recepits=recepits, orders=orders, id=_id)
    else:
        json_data = request.get_json()
        # updating recepit status
        if 'new_recepit_status' in json_data.keys() and json_data['new_recepit_status']:
            json_data['new_recepit_status'] = change_status_lang(json_data['new_recepit_status'])
            status_record = db_manager.check_record('statuses', title=json_data['new_recepit_status'])[0]
            db_manager.update('recepites', id=json_data['recepit_id'], status=status_record[2])
        # updating order status
        elif 'new_order_status' in json_data.keys() and json_data['new_order_status']:
            json_data['new_order_status'] = change_status_lang(json_data['new_order_status'])
            status_record = db_manager.check_record('statuses', title=json_data['new_order_status'])[0]
            menu_item_record = db_manager.check_record('menu_items', title=json_data['order_name'])[0]
            order_record = \
                db_manager.check_record('orders', recepite=json_data['recepit_id'], menu_item=menu_item_record[8])[0]
            db_manager.update('orders', id=order_record[5], status=status_record[2])
        # updating order count
        elif json_data['count']:
            menu_item_record = db_manager.check_record('menu_items', title=json_data['item'])[0]
            order_record = \
                db_manager.check_record('orders', recepite=json_data['recepit_id'], menu_item=menu_item_record[8])[0]
            db_manager.update('orders', id=order_record[5], count=json_data['count'])

        return {"Data Received": 200}


# this is for test


def menu_items(_id):
    if request.method == "GET":
        items = db_manager.read_all('menu_items')
        categories = db_manager.category_list()
        items = list(map(lambda item: list(item), items))
        categories_dict = {}
        categories = list(map(lambda item: categories_dict.update({item[0]: item[1]}), categories))
        for item in items:
            item[2] = categories_dict[item[2]]
        # items.sort(key=lambda x: x[8])
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
            new_item = MenuItem(title=json_data['name'], price=json_data['price'], category=json_data['category'],
                                discount=json_data['discount'])
        items = db_manager.read_all('menu_items')
        items.sort(key=lambda x: x[8])
        return {"Data Received": 200}


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
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        all_orders = [list(order) for order in all_orders]
        for order in all_orders:
            order[5] = change_status_lang(order[5])
        return render_template("cashier/new_orders_list.html", orders=all_orders, id=_id)
    else:
        json_data = request.get_json()
        json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])
        return {"Data Received": 200}

def new_order_list(_id):
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        new_orders = [list(order) for order in all_orders if order[5] == 'new']
        for order in new_orders:
            order[5] = change_status_lang(order[5])
        return render_template("cashier/new_orders_list.html", orders=new_orders, id=_id)
    else:
        json_data = request.get_json()
        json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])
        return {"Data Received": 200}


def cooking_order_list(_id):
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        cooking_orders = [list(order) for order in all_orders if order[5] == 'cooking']
        for order in cooking_orders:
            order[5] = change_status_lang(order[5])
        return render_template("cashier/cooking_orders_list.html", orders=cooking_orders, id=_id)
    else:
        json_data = request.get_json()
        json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])
        return {"Data Received": 200}


def served_order_list(_id):
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        serving_orders = [list(order) for order in all_orders if order[5] == 'serving']
        for order in serving_orders:
            order[5] = change_status_lang(order[5])
        return render_template("cashier/served_orders_list.html", orders=serving_orders, id=_id)
    else:
        json_data = request.get_json()
        json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])
        return {"Data Received": 200}


def paid_order_list(_id):
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        paid_orders = [list(order) for order in all_orders if order[5] == 'paid']
        for order in paid_orders:
            order[5] = change_status_lang(order[5])
        return render_template("cashier/paid_orders_list.html", orders=paid_orders, id=_id)
    else:
        json_data = request.get_json()
        json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])
        return {"Data Received": 200}


def cancelled_order_list(_id):
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        canceled_orders = [list(order) for order in all_orders if order[5] == 'canceled']
        for order in canceled_orders:
            order[5] = change_status_lang(order[5])
        return render_template("cashier/cancelled_orders_list.html", orders=canceled_orders, id=_id)
    else:
        json_data = request.get_json()
        json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])
        return {"Data Received": 200}


def recepit_list(_id):
    if request.method == "GET":
        # print(recepits)
        return render_template("cashier/receipt.html", recepits=recepits_list, orders=orders, id=_id)
    else:
        json_data = request.get_json()
        # call function for updating recepit status
        return render_template("cashier/receipt.html", recepits=recepits_list, orders=orders, id=_id)


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
