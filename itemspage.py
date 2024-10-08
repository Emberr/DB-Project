from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from TABLES import Pizza, Drink, Ingredient, PizzaIngredient, Dessert

items_pointer = Blueprint('items', __name__)

password = 'qazWSX123%21%40%23'

# Create an engine
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/PDS')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

@items_pointer.route('/items')
def items():
    username = session.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    # Create a session
    session1 = Session()

    # Fetch items from the database
    pizzas = []
    pizza_records = session1.query(Pizza).all()
    for pizza in pizza_records:
        ingredients = session1.query(PizzaIngredient).filter_by(pizza_id=pizza.pizza_id).all()
        total_cost = 0
        for p in ingredients:
            ingredient = session1.query(Ingredient).filter_by(ingredient_id=p.ingredient_id).first()
            total_cost += ingredient.cost
        from decimal import Decimal
        price_with_profit_and_vat = total_cost * Decimal('1.40') * Decimal('1.09') 
        final_price = round(price_with_profit_and_vat, 2)
        pizzas.append({
            'name': pizza.name,
            'price': final_price,
            'ingredients': [session1.query(Ingredient).filter_by(ingredient_id=p.ingredient_id).first().name for p in ingredients]
        })
    drinks = session1.query(Drink).all()
    desserts = session1.query(Dessert).all()

    # Close the session
    session1.close()

    return render_template('items.html', username=username, pizzas=pizzas, drinks=drinks, desserts=desserts)