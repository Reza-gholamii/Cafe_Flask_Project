from pprint import pprint

# from flask import render_template, request, redirect, make_response, Response
# from flask.helpers import url_for
from core.manager import *

db_manager = ExtraDataBaseManager()

#
# def home():
#     return render_template("home.html", page_name="home")
#
#
# def about_us():
#     return render_template("about_us.html", page_name="about_us")
#
#
# def contact_us():
#     return render_template("contact_us.html", page_name="contact_us")
#
#
# def menu():
#     return render_template("menu.html", page_name="menu")


def order_list():
    res = db_manager.order_lists(1)
    pprint(res)


if __name__ == "__main__":
    order_list()
