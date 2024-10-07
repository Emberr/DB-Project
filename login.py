from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, session
from database import get_db_connection
from TABLES import Customer, Session
import bcrypt

login_pointer = Blueprint('login', __name__)

@login_pointer.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']
        address = request.form['address']
        birthdate = request.form['birthdate']
        gender = request.form['gender']

        session_db = Session()
        existing_user = session_db.query(Customer).filter_by(username=username).first()

        if existing_user:
            session_db.close()
            return jsonify(success=False, message='Username already exists. Please choose a different one.')
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_customer = Customer(
                name=name,
                username=username,
                password=hashed_password.decode('utf-8'),
                phone_number=phone_number,
                address=address,
                birthdate=birthdate,
                total_pizzas_ordered=0,
                gender=gender
            )
            session_db.add(new_customer)
            session_db.commit()
            session_db.close()
            return jsonify(success=True, message='Registration successful! You can now log in.')
    else:
        return render_template('register.html')

@login_pointer.route('/login', methods=['GET', 'POST'])
@login_pointer.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        session_db = Session()
        user = session_db.query(Customer).filter_by(username=username).first()

        if user:
            stored_password = user.password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                session['username'] = username
                session_db.close()
                return jsonify(success=True)
            else:
                session_db.close()
                return jsonify(success=False, message='Invalid password. Please try again.')
        else:
            session_db.close()
            return jsonify(success=False, message='Username not found. Please register first.')
    else:
        return render_template('login.html')