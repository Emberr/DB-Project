from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from database import get_db_connection
from TABLES import Customer, Session

items_pointer = Blueprint('items', __name__)

@items_pointer.route('/items')
def items():
    username = request.args.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    return f"Item page for {username} - Coming soon!"