from flask import Flask
from views import html

app = Flask(__name__)

app.add_url_rule("/", 'home', html.home)
app.add_url_rule("/menu", 'menu', html.menu, methods=['GET', 'POST'])
app.add_url_rule("/contact_us", 'contact_us', html.contact_us, methods=['GET', 'POST'])
app.add_url_rule("/about_us", 'about_us', html.about_us)
app.add_url_rule("/recipe/<_id>", 'resipe', html.recipe)

app.add_url_rule("/api/<page>", 'api', html.api, methods=['GET'])

app.add_url_rule("/cashier/login", 'login', html.login, methods=['GET', 'POST'])
app.add_url_rule("/cashier", 'dashboard', html.dashboard, methods=['GET', 'POST'])
app.add_url_rule("/cashier/tables", 'tables', html.tables, methods=['GET', 'POST'])
app.add_url_rule("/cashier/charts", 'charts', html.charts, methods=['GET', 'POST'])
app.add_url_rule("/cashier/menu", 'menu_items', html.menu_items, methods=['GET', 'POST'])
app.add_url_rule("/cashier/orders", 'order_list', html.order_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/orders/archive", 'archive_list', html.archive_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/orders/new", 'new_order_list', html.new_order_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/orders/cooking", 'cooking_order_list', html.cooking_order_list,
                 methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/orders/served", 'served_order_list', html.served_order_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/orders/paid", 'paid_order_list', html.paid_order_list, methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/orders/cancelled", 'cancelled_order_list', html.cancelled_order_list,
                 methods=['GET', 'POST'])
app.add_url_rule("/cashier/<_id>/recepits", 'recepits', html.recepit_list, methods=['GET', 'POST'])
if __name__ == '__main__':
    app.run(port=12345)
