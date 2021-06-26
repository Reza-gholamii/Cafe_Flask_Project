from flask import Flask, render_template, request
from views import html

app = Flask(__name__)

app.add_url_rule("/", 'home', html.home)
app.add_url_rule("/menu", 'menu', html.menu)
app.add_url_rule("/contact_us", 'contact_us', html.contact_us)
app.add_url_rule("/about_us", 'about_us', html.about_us)

app.add_url_rule("/cashier/orders", 'order_list', html.order_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/menu", 'menu_items', html.menu_items, methods=['GET', 'POST'])
app.add_url_rule("/cashier/orders/served", 'served_order_list', html.served_order_list, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(port=12345)
