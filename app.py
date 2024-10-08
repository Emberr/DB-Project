from flask import Flask, session

from cartpage import cart_pointer
from login import login_pointer
from dashboard import dashboard_pointer
from accountpage import account_pointer
from itemspage import items_pointer
from checkoutpage import checkout_pointer
from orderpage import order_pointer
from report import report_pointer

app = Flask(__name__)
app.secret_key = 'idk_what_this_does'
app.config['SESSION_PERMANENT'] = False

app.register_blueprint(login_pointer)
app.register_blueprint(dashboard_pointer)
app.register_blueprint(account_pointer)
app.register_blueprint(cart_pointer)
app.register_blueprint(items_pointer)
app.register_blueprint(checkout_pointer)
app.register_blueprint(order_pointer)
app.register_blueprint(report_pointer)

if __name__ == '__main__':
    app.run(debug=False)
