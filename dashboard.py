from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from database import get_db_connection

dashboard_pointer = Blueprint('dashboard', __name__)

@dashboard_pointer.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    if username == 'admin':
        return render_template('admin_dashboard.html', username=username)

    return render_template('dashboard.html', username=username)

@dashboard_pointer.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login.login'))