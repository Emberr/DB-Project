from flask import Blueprint, render_template, session, redirect, url_for
from sqlalchemy.orm import sessionmaker
from TABLES import Customer, Session

checkout_pointer = Blueprint('checkout', __name__)

db_session = Session()

@checkout_pointer.route('/checkout')
def checkout():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    username = session['username']
    customer = db_session.query(Customer).filter_by(username=username).first()
    if not customer:
        return redirect(url_for('dashboard.dashboard'))

    cart = session.get('cart', {}).get(username, [])
    total_price = "{:.2f}".format(sum(float(item['price']) for item in cart))
    address = session.get('address', customer.address)  # Fetch the address from the session

    return render_template('checkout.html', cart=cart, total_price=total_price, address=address)