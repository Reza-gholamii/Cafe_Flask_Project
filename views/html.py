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


items = [("پیتزا", "۶۰۰۰۰"), ("پاستا", "۵۰۰۰۰"), ("هات داگ", "۴۰۰۰۰"), ("همبرگر", "۳۰۰۰۰"), ("پیش غذا", "۱۰۰۰۰")]


def menu_items():
    # need call a function to get access to last menu items
    return render_template("menu_items.html", items=items)
