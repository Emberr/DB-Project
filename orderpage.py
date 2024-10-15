from flask import Blueprint, render_template, session, flash, redirect, url_for, request, jsonify
from TABLES import Customer, Session, Order, OrderPizza, OrderDessert, OrderDrink, DeliveryOrder, Delivery, DeliveryPerson
import time
from datetime import datetime, timedelta
import threading
from deliverylogic import assign_delivery

order_pointer = Blueprint('order', __name__)

db_session1 = Session()

cancel_time_seconds = 300


def can_cancel_order(order_datetime):
    cancel_time_limit = order_datetime + timedelta(seconds=cancel_time_seconds)
    return datetime.now() < cancel_time_limit

def update_order_status_after_cancel(order_id):
    print(f'Waiting for {cancel_time_seconds} seconds before cancelling order {order_id}')
    time.sleep(cancel_time_seconds)
    db_session2 = Session()
    order = db_session2.query(Order).filter_by(order_id=order_id).first()
    if order and order.status == 'Pending':
        order.status = 'Preparing'
        db_session2.commit()
        print(f'Order {order_id} status updated to Preparing')
        assign_delivery()
        db_session2.close()

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

    print(f'Customer ID: {customer_id}')  # Debug print

    db_session = Session()

    orders = db_session.query(Order).filter_by(customer_id=customer_id).order_by(Order.order_datetime.desc()).all()
    print(f'Found {len(orders)} orders for customer ID {customer_id}')  # Debug print

    current_time = datetime.now()
    for order in orders:
        order_placement_time = order.order_datetime
        order.time_left = max(0, (order_placement_time + timedelta(seconds=cancel_time_seconds) - current_time).total_seconds())
        order.time_left_str = "{:.2f}".format(order.time_left)
        if order.status == 'Pending':
            threading.Thread(target=update_order_status_after_cancel, args=(order.order_id,)).start()


    return render_template('orders.html', orders=orders) if orders else render_template('no_orders.html')
@order_pointer.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    order = db_session1.query(Order).filter_by(order_id=order_id).first()
    if not order:
        flash('Order not found.')
        return redirect(url_for('order.orders'))

    customer = db_session1.query(Customer).filter_by(customer_id=order.customer_id).first()
    if not customer:
        flash('Customer not found.')
        return redirect(url_for('order.orders'))

    total_pizzas_in_order = db_session1.query(OrderPizza).filter_by(order_id=order_id).count()

    delivery_order = db_session1.query(DeliveryOrder).filter_by(order_id=order_id).first()
    if delivery_order:
        delivery = db_session1.query(Delivery).filter_by(delivery_id=delivery_order.delivery_id).first()
        if delivery:
            delivery_person = db_session1.query(DeliveryPerson).filter_by(deliverer_id=delivery.deliverer_id).first()

            delivery_orders_count = db_session1.query(DeliveryOrder).filter_by(delivery_id=delivery.delivery_id).count()

            db_session1.delete(delivery_order)
            db_session1.commit()

            if delivery_orders_count == 1:
                db_session1.delete(delivery)
                db_session1.commit()

            other_deliveries = db_session1.query(Delivery).filter(
                Delivery.deliverer_id == delivery_person.deliverer_id,
                Delivery.status == 'In Oven',
                Delivery.status == 'Preparing'
            ).all()

            if not other_deliveries:
                delivery_person.is_available = True
                db_session1.commit()

    db_session1.query(OrderPizza).filter_by(order_id=order_id).delete()
    db_session1.query(OrderDessert).filter_by(order_id=order_id).delete()
    db_session1.query(OrderDrink).filter_by(order_id=order_id).delete()
    customer.total_pizzas_ordered -= total_pizzas_in_order
    db_session1.delete(order)
    db_session1.commit()

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
    orders = new_session.query(Order).order_by(Order.order_datetime.desc()).all()
    new_session.commit()
    return render_template('all_orders.html', orders=orders)

@order_pointer.route('/update_order_status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if session.get('username') == 'admin':
        new_status = request.form.get('status')
        order = db_session1.query(Order).filter_by(order_id=order_id).first()

        if order:
            order.status = new_status
            db_session1.commit()
            flash(f"Order {order_id} status updated to {new_status}")
        else:

            flash('Order not found.')
        return redirect(url_for('order.all_orders'))

def update_status_preparing(order_id):
    order = db_session1.query(Order).filter_by(order_id=order_id).first()
    if order:
        order.status = 'Preparing'
        db_session1.commit()
        flash(f"Order {order_id} status updated to Preparing")
    else:
        flash('Order not found.')
    return redirect(url_for('order.orders'))
