from flask import Flask, session

from cartpage import cart_pointer
from login import login_pointer
from dashboard import dashboard_pointer
from accountpage import account_pointer
from itemspage import items_pointer
import atexit

app = Flask(__name__)
app.secret_key = 'idk_what_this_does'
app.config['SESSION_PERMANENT'] = False

app.register_blueprint(login_pointer)
app.register_blueprint(dashboard_pointer)
app.register_blueprint(account_pointer)
app.register_blueprint(cart_pointer)
app.register_blueprint(items_pointer)

def cleanup_sessions():
    with app.app_context():
        session.clear()

atexit.register(cleanup_sessions)

if __name__ == '__main__':
    app.run(debug=False)
