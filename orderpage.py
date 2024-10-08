from flask import Blueprint, render_template, session, flash, redirect, url_for, request, jsonify
from TABLES import Session, Order, OrderPizza, OrderDessert, OrderDrink
import time
from datetime import datetime, timedelta

order_pointer = Blueprint('order', __name__)

db_session = Session()

cancel_time_seconds = 60

def can_cancel_order(order_datetime):
    cancel_time_limit = order_datetime + timedelta(seconds=cancel_time_seconds)
    return datetime.now() < cancel_time_limit

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

    db_session.close()
    new_session = Session()

    orders = new_session.query(Order).filter_by(customer_id=customer_id).all()
    current_time = time.time()
    for order in orders:
        order_placement_time = order.order_datetime.timestamp()
        order.time_left = max(0, cancel_time_seconds - int(current_time - order_placement_time))
        if not can_cancel_order(order.order_datetime):
            order.status = 'Preparing'
    new_session.commit()

    if orders:
        return render_template('orders.html', orders=orders)
    else:
        return render_template('no_orders.html')

@order_pointer.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = db_session.query(Order).filter_by(order_id=order_id).first()
    if not order:
        flash('Order not found.')
        return redirect(url_for('order.orders'))

    db_session.query(OrderPizza).filter_by(order_id=order_id).delete()
    db_session.query(OrderDessert).filter_by(order_id=order_id).delete()
    db_session.query(OrderDrink).filter_by(order_id=order_id).delete()

    db_session.delete(order)
    db_session.commit()

    flash('Order cancelled successfully.')
    if session.get('username') == 'admin':
        return redirect(url_for('order.all_orders'))
    return redirect(url_for('order.orders'))

@order_pointer.route('/all_orders')
def all_orders():
    if session.get('username') != 'admin':
        flash('You are not authorized to view this page.')
        return redirect(url_for('dashboard.dashboard'))
    new_session = Session()
    orders = db_session.query(Order).all()
    for order in orders:
        if not can_cancel_order(order.order_datetime):
            order.status = 'Preparing'
    new_session.commit()
    return render_template('all_orders.html', orders=orders)

@order_pointer.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if session.get('username') == 'admin':
        new_status = request.form.get('status')
        order = db_session.query(Order).filter_by(order_id=order_id).first()

        if order:
            order.status = new_status
            db_session.commit()
            flash(f"Order {order_id} status updated to {new_status}")
        else:
            flash('Order not found.')
        return redirect(url_for('order.all_orders'))
