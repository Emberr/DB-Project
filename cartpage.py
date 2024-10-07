from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from database import get_db_connection
from TABLES import Customer, Session

cart_pointer = Blueprint('cart', __name__)

@cart_pointer.route('/cart')
def cart():
    username = request.args.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    return f"Cart page for {username} - Coming soon!"