from flask import Blueprint, render_template, session, redirect, url_for, request

cart_pointer = Blueprint('cart', __name__)

@cart_pointer.route('/cart')
def view_cart():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    if 'cart' not in session or not isinstance(session['cart'], dict):
        session['cart'] = {}

    username = session['username']
    cart = session.get('cart', {}).get(username, [])
    total_price = "{:.2f}".format(sum(float(item['price']) for item in cart))
    return render_template('cart.html', cart=cart, total_price=total_price)

@cart_pointer.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    username = session['username']
    item_id = request.form.get('item_id')
    item_type = request.form.get('item_type')
    item_name = request.form.get('item_name')
    item_price = request.form.get('item_price')

    if 'cart' not in session or not isinstance(session['cart'], dict):
        session['cart'] = {}

    if username not in session['cart']:
        session['cart'][username] = []

    session['cart'][username].append({
        'id': item_id,
        'type': item_type,
        'name': item_name,
        'price': item_price
    })
    session.modified = True
    return redirect(url_for('items.items'))

@cart_pointer.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if 'username' not in session:
        return redirect(url_for('login.login'))

    username = session['username']
    item_id = request.form.get('item_id')
    if 'cart' in session and username in session['cart']:
        for item in session['cart'][username]:
            if item['id'] == item_id:
                session['cart'][username].remove(item)
                session.modified = True
                break
    return redirect(url_for('cart.view_cart'))