from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="qazWSX123!@#",
        database="PizzaDeliverySystem"
    )
# # Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        phone_number = request.form['phone_number']
        address = request.form['address']
        birthdate = request.form['birthdate']

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to MySQL and insert the new user
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM Customer WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify(success=False, message='Username already exists. Please choose a different one.')
        else:
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert the new customer into the Customer table
            cursor.execute('''INSERT INTO Customer (name, username, password, phone_number, address, birthdate, total_pizzas_ordered)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (name, username, hashed_password.decode('utf-8'), phone_number, address, birthdate, 0))
            conn.commit()
            return jsonify(success=True, message='Registration successful! You can now log in.')

        cursor.close()
        conn.close()

    return render_template('register.html')
# Dashboard route
@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login'))

    # Render the dashboard, passing the username to the template
    return render_template('dashboard.html', username=username)

# Account route
@app.route('/account')
def account():
    username = request.args.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login'))

    # Here, you can add logic to retrieve the account details for the logged-in user.
    return f"Account page for {username} - Coming soon!"

# Cart route
@app.route('/cart')
def cart():
    username = request.args.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login'))

    return f"Cart page for {username} - Coming soon!"

# Orders route
@app.route('/orders')
def orders():
    username = request.args.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login'))

    return f"Orders page for {username} - Coming soon!"

# Logout route
@app.route('/logout')
def logout():
    flash('You have been logged out.')
    return redirect(url_for('login'))


# Login route
@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']

        # Connect to MySQL and retrieve the user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Customer WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            stored_password = user[6]  # Assuming password is the 7th column (index 6)
            # Check the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return jsonify(success=True)
            else:
                return jsonify(success=False, message='Invalid password. Please try again.')
        else:
            return jsonify(success=False, message='Username not found. Please register first.')

        cursor.close()
        conn.close()

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False)
