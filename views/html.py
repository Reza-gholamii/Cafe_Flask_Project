from flask import render_template, request, redirect, make_response, Response
from flask.helpers import url_for
from core.manager import ExtraDataBaseManager , DataBaseManager
from core.models import TextMessage
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)-10s - %(message)s')

db_manager = ExtraDataBaseManager()


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


def order_list():
    if request.method == "GET":
        # need call a function to get access to last orders based on tables
        return render_template("order_list.html", orders=orders)
    else:
        json_data = request.get_json()
        # print(json_data['status'])
        # data must be updated in database
        return render_template('order_list.html', orders=orders)


# this is for test

items = [("پیتزا", "۶۰۰۰۰"), ("پاستا", "۵۰۰۰۰"), ("هات داگ", "۴۰۰۰۰"), ("همبرگر", "۳۰۰۰۰"), ("پیش غذا", "۱۰۰۰۰")]


def menu_items():
    if request.method == "GET":
        # need call a function to get access last menu items in database
        return render_template("menu_items.html", items=items)
    else:
        _vars = request.form
        if "delete" in _vars.keys():
            # call function to delete the item from database
            pass
        elif "name" in _vars.keys():
            # call function to edit existing menu item in database
            pass
        elif "new_name" in _vars.keys():
            # call function to add a new menu item to database
            pass
        return render_template("menu_items.html", items=items)


# this is for test

served_orders = [("۳۲۵", "۱", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۲", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۶", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۴", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۴", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۶", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
                 ("۳۲۵", "۷", "۰۶/۲۰/۲۰۲۱", "جدید", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲")]


def served_order_list():
    if request.method == "GET":
        return render_template("served_orders_list.html", orders=served_orders)
    else:
        return render_template("served_orders_list.html", orders=served_orders)


# this is test for tables status
empty_table = [1, 3, 4, 7]


def dashboard():
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
            user = DataBaseManager().check_record("users", phone_number= resp["username"])[0]
        except:
            return render_template("cashier/login_cachier.html", condition="warning")

        # TODO: where is bug?? just update
        # TODO: hash

        if user[-3] == resp["password"]:
            pass
        else:
            return render_template("cashier/login_cachier.html", condition="warning")
        return redirect(f"/cashier/{user[-1]}/dashboard")

def tables():
    return 'table page'


def charts():
    return 'charts page'

