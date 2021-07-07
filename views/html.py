from pprint import pprint

from flask import render_template, request, redirect, make_response, Response
from flask.helpers import url_for
from datetime import timedelta, date
from core.utility import *
import model.users
from core.manager import ExtraDataBaseManager, DataBaseManager
from core.models import TextMessage, BaseModel
from model.categories import Category
from model.menu_items import MenuItem
from hashlib import sha256
from model import users
import logging

from model.orders import Order
from model.tables import Table
from model.recepites import Recepite

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')

db_manager = ExtraDataBaseManager()

# status_dict = {'new': 'جدید', 'cooking': 'در حال پخت', 'serving': 'سرو شده', 'canceled': 'کنسل شده'}

from core.manager import *


def viewer():
    # with open("views.log", "r+") as file:
    #     _v = int(file.readline(0))+1
    #     file.write(str(_v))
    print("viwed from user this page!")


def home():
    viewer()
    return render_template("home.html", page_name="home")


def recipe(_id):
    if db_manager.read("recepites", _id):
        return render_template("recpie.html", ID=_id)
    else:
        return render_template("404.html")


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
        db_manager.create(table="messages", model=message)
        logging.info(f"{__name__}: Message has Written into the DataBase")
        return {"Data Received": 200, "msg": "پیام شما با موفقیت ارسال گردید\nاز نظردهی شما بسیار سپاسگزاریم"}


def menu():
    if request.method == "GET":
        two_person_table_number = [table.number for table in Table.TABLES.values() if
                                   table.status == 12 and table.capacity == 2]
        four_person_table_number = [table.number for table in Table.TABLES.values() if
                                    table.status == 12 and table.capacity == 4]
        eight_person_table_number = [table.number for table in Table.TABLES.values() if
                                     table.status == 12 and table.capacity == 8]
        two_person_table_number.sort()
        four_person_table_number.sort()
        eight_person_table_number.sort()

        table_number = [two_person_table_number, four_person_table_number, eight_person_table_number]
        items = db_manager.read_all('menu_items')
        categories = db_manager.category_list()
        items = list(map(lambda item: list(item), items))
        items.sort(key=lambda x: x[8])
        image_names = [(item[4] if item[4] else "") for item in items]
        categories_dict = {}
        categories = list(map(lambda item: categories_dict.update({item[0]: item[1]}), categories))
        for item in items:
            item[2] = categories_dict[item[2]]
            item[3] = int(item[1] * (1 - (item[3] / 100)))

        # print(list(categories_dict.values()))

        print(items, table_number, list(categories_dict.values()), image_names, sep="\n\n")

        return render_template("menu.html", items=items, table_number=table_number,
                               cat=list(categories_dict.values()), images=image_names
                               )
    else:
        json_data = request.get_json()
        print(json_data)
        table_num = int(json_data['table_number'])
        recepite = Recepite(table_num)

        # orders = []
        for i in range(len(json_data['item_list'])):
            # orders.append(Order(recepite.number, json_data['item_list'][i], count=json_data['count_list'][i]))
            recepite.add_order(json_data['item_list'][i], count=json_data['count_list'][i])
        # return redirect(f"/recipe/{recepite.number}")
        return f"/recipe/{recepite.number}"


# fro here all are for cashier side

def menu_items():
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''
    if request.method == "GET":
        items = db_manager.read_all('menu_items')
        categories = db_manager.category_list()
        items = list(map(lambda item: list(item), items))
        categories_dict = {}
        categories = list(map(lambda item: categories_dict.update({item[0]: item[1]}), categories))
        for item in items:
            item[2] = categories_dict[item[2]]
        items.sort(key=lambda x: x[8])
        return render_template("cashier/menu_items.html", items=items, user=user_data, page_name="menu items")
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


def order_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        Table.all_tables()
        tables_id = list(Table.TABLES.keys())
        recepits, orders = [], []
        for table_id in tables_id:
            recepit = list(db_manager.calculate_price(table_id))
            # todo: it's better to change the condition to unpaid or other thing
            if recepit[0]:
                recepit.insert(0, table_id)
                order = db_manager.order_list(recepit[1])
                # recepit[2] = change_status_lang(recepit[2])
                order_l = []
                for item in order:
                    item = list(item)
                    # item[0] = change_status_lang(item[0])
                    order_l.append(item)
                recepits.append(recepit)
                orders.append(order_l)
        return render_template('cashier/order_list.html', recepits=recepits, orders=orders, user=user_data,
                               page_name="orders")
    else:
        json_data = request.get_json()
        # updating recepit status
        if 'new_recepit_status' in json_data.keys() and json_data['new_recepit_status']:
            # json_data['new_recepit_status'] = change_status_lang(json_data['new_recepit_status'])
            status_record = db_manager.check_record('statuses', title=json_data['new_recepit_status'])[0]
            db_manager.update('recepites', id=json_data['recepit_id'], status=status_record[2])

            tabl_id = db_manager.read("recepites", json_data['recepit_id'])[0][3]
            db_manager.update("tables", id=tabl_id, status=12)

        # updating order status
        elif 'new_order_status' in json_data.keys() and json_data['new_order_status']:
            # json_data['new_order_status'] = change_status_lang(json_data['new_order_status'])
            status_record = db_manager.check_record('statuses', title=json_data['new_order_status'])[0]
            menu_item_record = db_manager.check_record('menu_items', title=json_data['order_name'])[0]
            order_record = \
                db_manager.check_record('orders', recepite=json_data['recepit_id'], menu_item=menu_item_record[8])[0]
            db_manager.update('orders', id=order_record[5], status=status_record[2])

            recp_id = db_manager.read("orders", order_record[5])[0][3]
            tab_id = db_manager.read("recepites", recp_id)[0][3]
            prices = db_manager.calculate_price(tab_id)[2:]
            db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        # updating order count
        elif json_data['count']:
            menu_item_record = db_manager.check_record('menu_items', title=json_data['item'])[0]
            order_record = \
                db_manager.check_record('orders', recepite=json_data['recepit_id'], menu_item=menu_item_record[8])[0]
            db_manager.update('orders', id=order_record[5], count=json_data['count'])

            recp_id = db_manager.read("orders", order_record[5])[0][3]
            tab_id = db_manager.read("recepites", recp_id)[0][3]
            prices = db_manager.calculate_price(tab_id)[2:]
            db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        return {"Data Received": 200}


def archive_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        all_orders = [list(order) for order in all_orders]
        # for order in all_orders:
        # order[5] = change_status_lang(order[5])
        all_orders.sort(key=lambda x: x[0], reverse=True)
        return render_template("cashier/archive_list.html", orders=all_orders, user=user_data,
                               page_name="archive orlders")
    else:
        json_data = request.get_json()
        # json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])

        recp_id = db_manager.read("orders", json_data['order_id'])[0][3]
        tab_id = db_manager.read("recepites", recp_id)[0][3]
        prices = db_manager.calculate_price(tab_id)[2:]
        db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        return {"Data Received": 200}


def new_order_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        new_orders = [list(order) for order in all_orders if order[5] == 'جدید']
        # for order in new_orders:
        #     order[5] = change_status_lang(order[5])

        new_orders.sort(key=lambda x: x[0], reverse=True)
        return render_template("cashier/new_orders_list.html", orders=new_orders, user=user_data,
                               page_name="new orders")
    else:
        json_data = request.get_json()
        # json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])

        recp_id = db_manager.read("orders", json_data['order_id'])[0][3]
        tab_id = db_manager.read("recepites", recp_id)[0][3]
        prices = db_manager.calculate_price(tab_id)[2:]
        db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        return {"Data Received": 200}


def cooking_order_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        cooking_orders = [list(order) for order in all_orders if order[5] == 'در حال پخت']
        # for order in cooking_orders:
        #     order[5] = change_status_lang(order[5])
        cooking_orders.sort(key=lambda x: x[0], reverse=True)
        return render_template("cashier/cooking_orders_list.html", orders=cooking_orders, user=user_data,
                               page_name="cooking orders")
    else:
        json_data = request.get_json()
        # json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])

        recp_id = db_manager.read("orders", json_data['order_id'])[0][3]
        tab_id = db_manager.read("recepites", recp_id)[0][3]
        prices = db_manager.calculate_price(tab_id)[2:]
        db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        return {"Data Received": 200}


def served_order_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        serving_orders = [list(order) for order in all_orders if order[5] == 'سرو شده']
        # for order in serving_orders:
        #     order[5] = change_status_lang(order[5])
        serving_orders.sort(key=lambda x: x[0], reverse=True)
        return render_template("cashier/served_orders_list.html", orders=serving_orders, user=user_data,
                               page_name="served order")
    else:
        json_data = request.get_json()
        # json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])

        recp_id = db_manager.read("orders", json_data['order_id'])[0][3]
        tab_id = db_manager.read("recepites", recp_id)[0][3]
        prices = db_manager.calculate_price(tab_id)[2:]
        db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        return {"Data Received": 200}


def paid_order_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        paid_orders = [list(order) for order in all_orders if order[5] == 'پرداخت شده']
        # for order in paid_orders:
        #     order[5] = change_status_lang(order[5])
        paid_orders.sort(key=lambda x: x[0], reverse=True)
        return render_template("cashier/paid_orders_list.html", orders=paid_orders, user=user_data,
                               page_name="paid orders")
    else:
        json_data = request.get_json()
        # json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])

        recp_id = db_manager.read("orders", json_data['order_id'])[0][3]
        tab_id = db_manager.read("recepites", recp_id)[0][3]
        prices = db_manager.calculate_price(tab_id)[2:]
        db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        return {"Data Received": 200}


def cancelled_order_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        all_orders = db_manager.archive_orders_list('status')
        canceled_orders = [list(order) for order in all_orders if order[5] == 'کنسل شده']
        # for order in canceled_orders:
        #     order[5] = change_status_lang(order[5])
        canceled_orders.sort(key=lambda x: x[0], reverse=True)
        return render_template("cashier/cancelled_orders_list.html", orders=canceled_orders, user=user_data,
                               page_name="canceled orders")
    else:
        json_data = request.get_json()
        # json_data['status'] = change_status_lang(json_data['status'])
        status_record = db_manager.check_record('statuses', title=json_data['status'])[0]
        db_manager.update('orders', id=json_data['order_id'], status=status_record[2])

        recp_id = db_manager.read("orders", json_data['order_id'])[0][3]
        tab_id = db_manager.read("recepites", recp_id)[0][3]
        prices = db_manager.calculate_price(tab_id)[2:]
        db_manager.update("recepites", id=recp_id, total_price=prices[0], final_price=prices[1])

        return {"Data Received": 200}


def recepit_list():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    if request.method == "GET":
        orders = []
        recepits_list = db_manager.read_all('recepites')
        recepits_list.sort(key=lambda x: x[4], reverse=True)
        recepits_list = list(map(lambda recepit: list(recepit), recepits_list))
        for recepit in recepits_list:
            recepit.append(recepit[0] - recepit[1])
            order = db_manager.order_list(recepit[4])
            recepit[2] = change_status_lang_by_number(str(recepit[2]))
            orders.append(order)
            recepit.append(order[0][5].strftime('%m.%d.%Y'))
        return render_template("cashier/receipt.html", recepits=recepits_list, orders=orders, page_name="recepits"
                               , user=user_data)

    else:
        json_data = request.get_json()
        # recepit_status = change_status_lang(json_data['status'])
        # print(recepit_status)
        # print("###############")
        # print(json_data)
        # print("##############")
        print(db_manager.check_record('statuses', title=json_data['status']))
        recepit_status_id = db_manager.check_record('statuses', title=json_data['status'])[0][2]
        db_manager.update('recepites', id=json_data['recepit_id'], status=recepit_status_id)

        tabl_id = db_manager.read("recepites", json_data['recepit_id'])[0][3]
        db_manager.update("tables", id=tabl_id, status=12)

    return {"Data Received": 200}


# this is test for tables status
# empty_table = [1, 3, 4, 7]

# this is for test
#
# served_orders = [("۳۲۵", "۱", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
#                  ("۳۲۵", "۲", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
#                  ("۳۲۵", "۶", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
#                  ("۳۲۵", "۴", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
#                  ("۳۲۵", "۴", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
#                  ("۳۲۵", "۶", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
#                  ("۳۲۵", "۷", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲")]


#
# all_orders = orders.copy()

def dashboard():
    # this codes should be in all cashier side functions to get user and security reasons
    __ = user_seter()
    if type(__) == int:
        user_data = DataBaseManager().read("users", __)[0]
    else:
        return user_seter()
    # ''''''''''''''''''''
    # data = {
    #     'count_new_orders': len(orders),
    #     'count_orders': len(orders) + len(served_orders),
    #     'count_empty_tables': len(empty_table),
    #     'count_view': 15
    # }

    last_message = db_manager.last_row("messages")
    today = date.today().strftime("%Y-%m-%d")

    data = {
        'last_message': last_message[0] if last_message else (),
        'count_new_orders': len(db_manager.statusfilter("orders", "جدید")),
        'count_orders': len(db_manager.read_all("orders", today=today)),
        'count_empty_tables': len(db_manager.statusfilter("tables", "خالی")),
        'all_incoming': db_manager.incoming(),
        'today_incoming': db_manager.incoming(today)
        # 'count_view': 15
    }

    # Charts :
    day_report = db_manager.report_orders("weekday")
    hour_report = db_manager.report_orders("hour")
    best_sellers = db_manager.bestsellers(3)

    weekdays, hours, bests = [], [], []
    for item in best_sellers:
        bests.append((item[1], item[2]))

    for days in range(6, 13):
        for item in day_report:
            if item[0] == (days % 7 or days % 7 + 1):
                weekdays.append(item[1])
            else:
                weekdays.append(0)

    for hour in range(10, 24, 2):
        count = 0
        for item in hour_report:
            if hour <= item[0] < hour + 2:
                count += item[1]
        hours.append(count)

    bests = {
        'labels': [best[0] for best in bests],
        'values': [best[1] for best in bests]
    }

    return render_template('cashier/dashboard.html', user=user_data, data=data, page_name="dashboard", days=weekdays,
                           hours=hours, bests=bests)


# def tables():
#     # this codes should be in all cashier side functions to get user and security reasons
#     __ = user_seter()
#     if type(__) == int:
#         user_data = DataBaseManager().read("users", __)[0]
#     else:
#         return user_seter()
#     # ''''''''''''''''''''
#     tables = ExtraDataBaseManager().read_all("tables")
#     # TODO: where is order number?
#
#     return render_template("cashier/tables.html", tables=tables, user=user_data, page_name="tables")


def login():
    if request.method == "GET":
        __ = user_seter()
        if type(__) == int:
            return redirect(f"/cashier")

        return render_template("cashier/login_cachier.html")
    elif request.method == "POST":
        resp = request.form
        try:
            user = DataBaseManager().check_record("users", phone_number=resp["username"][-9:])[0]

        except:
            return render_template("cashier/login_cachier.html", condition="warning")
        password_hashed = sha256(resp["password"].encode()).hexdigest()
        if user[-3] == password_hashed:
            html_str = redirect(f"/cashier")
            response = make_response(html_str)
            response.set_cookie(
                '_ID', str(user[-1]), max_age=timedelta(weeks=1))
            return response
        else:
            return render_template("cashier/login_cachier.html", condition="warning")


def user_seter():
    """
    this is not flask function .
    this function just check cookie and return user if it exists
    """
    cookies = request.cookies
    id = cookies.get("_ID")
    if id:
        u = DataBaseManager().read("users", id)
        return int(id)
    else:
        return redirect('/cashier/login')


def api(page):
    if page == "menu":
        if request.method == "GET":
            two_person_table_number = [table.number for table in Table.TABLES.values() if
                                       table.status == 12 and table.capacity == 2]
            four_person_table_number = [table.number for table in Table.TABLES.values() if
                                        table.status == 12 and table.capacity == 4]
            eight_person_table_number = [table.number for table in Table.TABLES.values() if
                                         table.status == 12 and table.capacity == 8]
            two_person_table_number.sort()
            four_person_table_number.sort()
            eight_person_table_number.sort()

            table_number = [two_person_table_number, four_person_table_number, eight_person_table_number]
            items = db_manager.read_all('menu_items')
            categories = db_manager.category_list()
            items = list(map(lambda item: list(item), items))
            items.sort(key=lambda x: x[8])
            image_names = [(item[4] if item[4] else "") for item in items]
            categories_dict = {}
            categories = list(map(lambda item: categories_dict.update({item[0]: item[1]}), categories))
            for item in items:
                item[2] = categories_dict[item[2]]
                item[3] = int(item[1] * (1 - (item[3] / 100)))

            # print(list(categories_dict.values()))

            print(items, table_number, list(categories_dict.values()), image_names, sep="\n\n")

            return render_template('spa_api/' + page + '.html', items=items, table_number=table_number,
                                   cat=list(categories_dict.values()), images=image_names
                                   )
        else:
            json_data = request.get_json()
            print(json_data)
            table_num = int(json_data['table_number'])
            recepite = Recepite(table_num)

            # orders = []
            for i in range(len(json_data['item_list'])):
                # orders.append(Order(recepite.number, json_data['item_list'][i], count=json_data['count_list'][i]))
                recepite.add_order(json_data['item_list'][i], count=json_data['count_list'][i])
            # return redirect(f"/recipe/{recepite.number}")
            return f"/recipe/{recepite.number}"

    if page == "about_us":
        return render_template('spa_api/' + page + '.html', page_name="about_us")

    if page == "contact_us":
        return render_template('spa_api/' + page + '.html')

    if page == "tables":
        __ = user_seter()
        if type(__) == int:
            user_data = DataBaseManager().read("users", __)[0]
        else:
            return user_seter()
        # ''''''''''''''''''''
        _tables = db_manager.read_all("tables")
        # TODO: where is order number?

        return render_template('spa_api/' + page + '.html', tables=_tables, user=user_data)

    if page == "dashboard":
        # this codes should be in all cashier side functions to get user and security reasons
        __ = user_seter()
        if type(__) == int:
            user_data = DataBaseManager().read("users", __)[0]
        else:
            return user_seter()
        # ''''''''''''''''''''
        # data = {
        #     'count_new_orders': len(orders),
        #     'count_orders': len(orders) + len(served_orders),
        #     'count_empty_tables': len(empty_table),
        #     'count_view': 15
        # }

        last_message = db_manager.last_row("messages")
        today = date.today().strftime("%Y-%m-%d")

        data = {
            'last_message': last_message[0] if last_message else (),
            'count_new_orders': len(db_manager.statusfilter("orders", "جدید")),
            'count_orders': len(db_manager.read_all("orders", today=today)),
            'count_empty_tables': len(db_manager.statusfilter("tables", "خالی")),
            'all_incoming': db_manager.incoming(),
            'today_incoming': db_manager.incoming(today)
            # 'count_view': 15
        }

        # Charts :
        day_report = db_manager.report_orders("weekday")
        hour_report = db_manager.report_orders("hour")
        best_sellers = db_manager.bestsellers(3)

        weekdays, hours, bests = [], [], []
        for item in best_sellers:
            bests.append((item[1], item[2]))

        for days in range(6, 13):
            for item in day_report:
                if item[0] == (days % 7 or days % 7 + 1):
                    weekdays.append(item[1])
                else:
                    weekdays.append(0)

        for hour in range(10, 24, 2):
            count = 0
            for item in hour_report:
                if hour <= item[0] < hour + 2:
                    count += item[1]
            hours.append(count)

        bests = {
            'labels': [best[0] for best in bests],
            'values': [best[1] for best in bests]
        }

        return render_template('spa_api/' + page + '.html', user=user_data,
                               data=data, page_name="dashboard", days=weekdays, hours=hours, bests=bests)

    if page == "menu_items":
        __ = user_seter()
        if type(__) == int:
            user_data = DataBaseManager().read("users", __)[0]
        else:
            return user_seter()
        items = db_manager.read_all('menu_items')
        categories = db_manager.category_list()
        items = list(map(lambda item: list(item), items))
        categories_dict = {}
        categories = list(map(lambda item: categories_dict.update({item[0]: item[1]}), categories))
        for item in items:
            item[2] = categories_dict[item[2]]
        items.sort(key=lambda x: x[8])
        return render_template('spa_api/' + page + '.html', items=items, user=user_data, page_name="menu items")

    return "API : Data Request Not Valid!"
