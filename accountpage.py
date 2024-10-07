from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from database import get_db_connection
from TABLES import Customer, Session

account_pointer = Blueprint('account', __name__)

@account_pointer.route('/account', methods=['GET', 'POST'])
def account():
    username = session.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    session_db = Session()
    if request.method == 'POST':
        new_address = request.form['address']
        customer = session_db.query(Customer).filter_by(username=username).first()
        if customer:
            customer.address = new_address
            session_db.commit()
            flash('Address updated successfully.')
        else:
            flash('Customer not found.')
        return redirect(url_for('account.account'))
    customer = session_db.query(Customer).filter_by(username=username).first()
    session_db.close()
    if customer:
        customer_info = {
            'name': customer.name,
            'username': customer.username,
            'phone_number': customer.phone_number,
            'address': customer.address,
            'birthdate': customer.birthdate,
            'total_pizzas_ordered': customer.total_pizzas_ordered
        }
        return render_template('account.html', customer=customer_info)
    else:
        flash('Customer not found.')
        return redirect(url_for('login.login'))


