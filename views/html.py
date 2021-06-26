from flask import render_template, request, redirect, make_response, Response
from flask.helpers import url_for


def home():
    return render_template("home.html", page_name="home")


def about_us():
    return render_template("about_us.html", page_name="about_us")


def contact_us():
    return render_template("contact_us.html", page_name="contact_us")


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
    # need call a function to get access to last orders based on tables
    return render_template("order_list.html", orders=orders)


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
