# itemspage.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from TABLES import Pizza, Drink, Ingredient, PizzaIngredient, Dessert, engine

items_pointer = Blueprint('items', __name__)

Session = sessionmaker(bind=engine)

@items_pointer.route('/items')
def items():
    username = session.get('username')
    if not username:
        flash('Please log in first.')
        return redirect(url_for('login.login'))

    session1 = Session()
    pizzas = []
    pizza_records = session1.query(Pizza).all()
    for pizza in pizza_records:
        ingredients = session1.query(PizzaIngredient).filter_by(pizza_id=pizza.pizza_id).all()
        ingredient_names = []
        is_vegetarian = True
        is_vegan = True
        total_cost = 0
        for p in ingredients:
            ingredient = session1.query(Ingredient).filter_by(ingredient_id=p.ingredient_id).first()
            ingredient_names.append(ingredient.name)
            total_cost += ingredient.cost
            if not ingredient.is_vegetarian:
                is_vegetarian = False
            if not ingredient.is_vegan:
                is_vegan = False
        from decimal import Decimal
        price_with_profit_and_vat = total_cost * Decimal('1.40') * Decimal('1.09')
        final_price = round(price_with_profit_and_vat, 2)
        pizzas.append({
            'id': pizza.pizza_id,
            'name': pizza.name,
            'price': final_price,
            'ingredients': ingredient_names,
            'is_vegetarian': is_vegetarian,
            'is_vegan': is_vegan
        })
    drinks = session1.query(Drink).all()
    desserts = session1.query(Dessert).all()

    session1.close()

    return render_template('items.html', username=username, pizzas=pizzas, drinks=drinks, desserts=desserts)