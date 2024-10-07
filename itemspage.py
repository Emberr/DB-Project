from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from TABLES import Pizza, Drink, Ingredient, Dessert

items_pointer = Blueprint('items', __name__)

# Create an engine
engine = create_engine('mysql+pymysql://root:qazWSX123%21%40%23@localhost/PDS')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

@items_pointer.route('/items')
def items():
    username = request.args.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    # Create a session
    session = Session()

    # Fetch items from the database
    pizzas = session.query(Pizza).all()
    drinks = session.query(Drink).all()
    desserts = session.query(Dessert).all()

    # Close the session
    session.close()

    return render_template('items.html', username=username, pizzas=pizzas, drinks=drinks, desserts=desserts)