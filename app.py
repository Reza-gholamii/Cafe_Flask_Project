from flask import Flask
from views import html

app = Flask(__name__)

app.add_url_rule("/", 'home', html.home)
app.add_url_rule("/menu", 'menu', html.menu)
app.add_url_rule("/contact_us", 'contact_us', html.contact_us, methods=['GET', 'POST'])
app.add_url_rule("/about_us", 'about_us', html.about_us)

app.add_url_rule("/cashier/<_id>", 'dashboard', html.dashboard, methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/orders", 'order_list', html.order_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/tables", 'tables', html.tables, methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/charts", 'charts', html.charts, methods=['GET', 'POST'])
app.add_url_rule("/cashier/menu", 'menu_items', html.menu_items, methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/orders/served", 'served_order_list', html.served_order_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/login", 'login', html.login, methods=['GET', 'POST'])
if __name__ == '__main__':
    app.run(port=12345)
