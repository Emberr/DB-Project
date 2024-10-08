# orderpage.py
from flask import Blueprint, render_template, session, flash, redirect, url_for
from TABLES import Session, Order
import time

order_pointer = Blueprint('order', __name__)

db_session = Session()

# orderpage.py
from flask import Blueprint, render_template, session, flash, redirect, url_for
from TABLES import Session, Order
import time

order_pointer = Blueprint('order', __name__)

db_session = Session()

@order_pointer.route('/orders')
def orders():
    username = session.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    customer_id = session.get('customer_id')
    if not customer_id:
        flash('Customer ID not found in session.')
        return redirect(url_for('login.login'))

    # Close and reopen the session to ensure it is up-to-date
    db_session.close()
    new_session = Session()

    orders = new_session.query(Order).filter_by(customer_id=customer_id).all()
    current_time = time.time()
    for order in orders:
        order_placement_time = order.order_datetime.timestamp()
        order.time_left = max(0, 300 - int(current_time - order_placement_time))
    if orders:
        return render_template('orders.html', orders=orders)
    else:
        return render_template('no_orders.html')

@order_pointer.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = db_session.query(Order).filter_by(order_id=order_id).first()
    if order:
        db_session.delete(order)
        db_session.commit()
        flash('Order has been canceled.')
    return redirect(url_for('order.orders'))