from flask import render_template, request, redirect, make_response, Response
from flask.helpers import url_for
from core.manager import ExtraDataBaseManager
from core.models import TextMessage


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
        _vars = request.form
        message = TextMessage()
        # TODO: use try and except for exceptions handeling after check validate        


def menu():
    return render_template("menu.html", page_name="menu")


# this is for test

orders = [("۱", "۳۲۵", "جدید", "رضا غلامی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۲", "۳۲۵", "جدید", "رضا یزدانی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۳", "۳۲۵", "جدید", "علی غلامی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۴", "۳۲۵", "جدید", "رسول احدی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۵", "۳۲۵", "جدید", "س‍پهر بازیار", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۶", "۳۲۵", "جدید", "علی احدی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲"),
          ("۷", "۳۲۵", "جدید", "ممد نادیجی", "قهوه", "۲", "نسکافه", "۱", "کاپوچینو", "۲")]


def order_list():
    return render_template("order_list.html", orders=orders)
