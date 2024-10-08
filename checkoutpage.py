# checkoutpage.py
import datetime
from flask import Blueprint, render_template, session, redirect, url_for
from sqlalchemy.orm import sessionmaker
from TABLES import Customer, Session, Order

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
    address = session.get('address', customer.address)

    return render_template('checkout.html', cart=cart, total_price=total_price, address=address)

@checkout_pointer.route('/place_order')
def place_order():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    username = session['username']
    customer = db_session.query(Customer).filter_by(username=username).first()
    if not customer:
        return redirect(url_for('dashboard.dashboard'))

    cart = session.get('cart', {}).get(username, [])
    total_price = "{:.2f}".format(sum(float(item['price']) for item in cart))
    order_datetime = datetime.datetime.now()
    delivery_address = session.get('address', customer.address)

    # Insert order into the database
    new_order = Order(
        customer_id=customer.customer_id,
        total_price=total_price,
        order_datetime=order_datetime,
        delivery_address=delivery_address
    )
    db_session.add(new_order)
    db_session.commit()

    # Store customer_id in session
    session['customer_id'] = customer.customer_id

    # Refresh the session to ensure the new order is fetched
    db_session.refresh(new_order)
    session.pop('cart', None)

    return redirect(url_for('order.orders'))