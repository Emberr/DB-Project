import datetime
from flask import Blueprint, render_template, session, redirect, url_for
from sqlalchemy.orm import sessionmaker
from TABLES import Customer, Session, Order, OrderDrink, OrderDessert, OrderPizza, Drink, Dessert, Pizza

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

    new_order = Order(
        customer_id=customer.customer_id,
        total_price=total_price,
        order_datetime=order_datetime,
        delivery_address=delivery_address,
        status='Pending'
    )
    db_session.add(new_order)
    db_session.commit()
    db_session.refresh(new_order)

    for item in cart:
        item_type = item['type']
        item_id = item['id']
        quantity = item.get('quantity', 1)  # Automatically set to 1 if not no quantity is specified

        if item_type == 'pizza':
            pizza = db_session.query(Pizza).filter_by(name=item_id).first()
            if pizza:
                existing_order_pizza = db_session.query(OrderPizza).filter_by(order_id=new_order.order_id, pizza_id=pizza.pizza_id).first()
                if existing_order_pizza:
                    existing_order_pizza.quantity += quantity
                else:
                    order_pizza = OrderPizza(order_id=new_order.order_id, pizza_id=pizza.pizza_id, quantity=quantity)
                    db_session.add(order_pizza)
        elif item_type == 'dessert':
            dessert = db_session.query(Dessert).filter_by(dessert_id=item_id).first()
            if dessert:
                existing_order_dessert = db_session.query(OrderDessert).filter_by(order_id=new_order.order_id, dessert_id=dessert.dessert_id).first()
                if existing_order_dessert:
                    existing_order_dessert.quantity += quantity
                else:
                    order_dessert = OrderDessert(order_id=new_order.order_id, dessert_id=dessert.dessert_id, quantity=quantity)
                    db_session.add(order_dessert)
        elif item_type == 'drink':
            drink = db_session.query(Drink).filter_by(drink_id=item_id).first()
            if drink:
                existing_order_drink = db_session.query(OrderDrink).filter_by(order_id=new_order.order_id, drink_id=drink.drink_id).first()
                if existing_order_drink:
                    existing_order_drink.quantity += quantity
                else:
                    order_drink = OrderDrink(order_id=new_order.order_id, drink_id=drink.drink_id, quantity=quantity)
                    db_session.add(order_drink)

    db_session.commit()
    session['customer_id'] = customer.customer_id
    session.pop('cart', None)

    return redirect(url_for('order.orders'))