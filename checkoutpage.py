from flask import Flask, request, jsonify, session, redirect, url_for, render_template, Blueprint
from datetime import datetime, date
from TABLES import Session, DiscountCode, Order, Customer, DeliveryPerson, OrderPizza, OrderDessert, OrderDrink, Pizza, Dessert, Drink

checkout_pointer = Blueprint('checkout', __name__)

def validate_discount_code(code):
    db_session = Session()
    discount_code = db_session.query(DiscountCode).filter_by(code=code).first()
    db_session.close()
    if discount_code and discount_code.valid_to > date.today():
        return discount_code.discount_percent
    return None

@checkout_pointer.route('/apply_discount', methods=['POST'])
def apply_discount():
    discount_code = request.form.get('discount_code')
    discount_percent = validate_discount_code(discount_code)
    if discount_percent:
        username = session.get('username')
        cart = session.get('cart', {}).get(username, [])
        total_price = sum(float(item['price']) for item in cart)
        discount_percent = float(discount_percent)
        discount_amount = total_price * (discount_percent)
        total_price -= discount_amount
        total_price = "{:.2f}".format(total_price)
        session['discount_percentage'] = discount_percent
        return jsonify({'success': True, 'discount_percentage': discount_percent, 'total_price': total_price, 'discount_amount': "{:.2f}".format(discount_amount)})
    else:
        return jsonify({'error': 'Invalid or expired discount code.'})

@checkout_pointer.route('/place_order', methods=['POST'])
def place_order():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    db_session = Session()
    customer = db_session.query(Customer).filter_by(username=username).first()
    if not customer:
        return redirect(url_for('dashboard'))

    cart = session.get('cart', {}).get(username, [])
    total_price = sum(float(item['price']) for item in cart)
    discount_applied = False
    discount_applied_pizza = False

    today = date.today()
    if customer.birthdate and customer.birthdate.month == today.month and customer.birthdate.day == today.day:
        cheapest_pizza = min((item for item in cart if item['type'] == 'pizza'), key=lambda x: float(x['price']), default=None)
        cheapest_drink = min((item for item in cart if item['type'] == 'drink'), key=lambda x: float(x['price']), default=None)
        if cheapest_pizza:
            total_price -= float(cheapest_pizza['price'])
            cheapest_pizza['price'] = 0
            discount_applied_pizza = True
            discount_applied = True
        if cheapest_drink:
            total_price -= float(cheapest_drink['price'])
            cheapest_drink['price'] = 0
            discount_applied_pizza = True
            discount_applied = True

    if not discount_applied and customer.total_pizzas_ordered >= 10:
        total_price *= 0.9
        discount_applied = True

    discount_percentage = float(session.get('discount_percentage', 0))
    if not discount_applied and discount_percentage:
        total_price *= (1 - discount_percentage)
        session.pop('discount_percentage', None)
        discount_applied = True

    total_price = "{:.2f}".format(total_price)
    order_datetime = datetime.now()
    delivery_address = session.get('address', customer.address)

    postal_code = delivery_address[:4]
    delivery_person = db_session.query(DeliveryPerson).filter_by(postal_code=postal_code).first()
    if not delivery_person:
        return jsonify({'error': 'We do not deliver to this address. Please choose a valid delivery address.'})

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

    total_pizzas_in_order = 0
    for item in cart:
        item_type = item['type']
        item_id = item['id']
        quantity = item.get('quantity', 1)

        if item_type == 'pizza':
            total_pizzas_in_order += quantity
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

    if customer.total_pizzas_ordered >= 10 and discount_applied_pizza:
        customer.total_pizzas_ordered = 0
    else:
        customer.total_pizzas_ordered += total_pizzas_in_order
    db_session.commit()

    session['customer_id'] = customer.customer_id
    session.pop('cart', None)

    return jsonify({'success': True})

@checkout_pointer.route('/checkout')
def checkout():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    db_session = Session()
    customer = db_session.query(Customer).filter_by(username=username).first()
    if not customer:
        return redirect(url_for('dashboard'))

    cart = session.get('cart', {}).get(username, [])
    total_price = sum(float(item['price']) for item in cart)
    discount_amount = 0
    discount_applied = False

    today = date.today()
    if customer.birthdate and customer.birthdate.month == today.month and customer.birthdate.day == today.day:
        cheapest_pizza = min((item for item in cart if item['type'] == 'pizza'), key=lambda x: float(x['price']), default=None)
        cheapest_drink = min((item for item in cart if item['type'] == 'drink'), key=lambda x: float(x['price']), default=None)
        if cheapest_pizza:
            discount_amount += float(cheapest_pizza['price'])
            discount_applied = True
        if cheapest_drink:
            discount_amount += float(cheapest_drink['price'])
            discount_applied = True

    if not discount_applied and customer.total_pizzas_ordered >= 10:
        discount_amount += total_price * 0.1
        discount_applied = True

    discount_percentage = float(session.get('discount_percentage', 0))
    if not discount_applied and discount_percentage:
        discount_amount += total_price * (discount_percentage / 100)
        session.pop('discount_percentage', None)
        discount_applied = True

    total_price -= discount_amount
    total_price = "{:.2f}".format(total_price)
    discount_amount = "{:.2f}".format(discount_amount)
    address = session.get('address', customer.address)
    delivery_postal_codes = [dp.postal_code for dp in db_session.query(DeliveryPerson).all()]

    return render_template('checkout.html', cart=cart, total_price=total_price, discount_amount=discount_amount, address=address, delivery_postal_codes=delivery_postal_codes)
@checkout_pointer.route('/check_birthday_discount', methods=['GET'])
def check_birthday_discount():
    if 'username' not in session:
        return jsonify({'error': 'User not logged in'})

    username = session['username']
    db_session = Session()
    customer = db_session.query(Customer).filter_by(username=username).first()
    if not customer:
        return jsonify({'error': 'Customer not found'})

    today = date.today()
    if customer.birthdate and customer.birthdate.month == today.month and customer.birthdate.day == today.day:
        return jsonify({'birthday': True})
    return jsonify({'birthday': False})