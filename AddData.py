from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from TABLES import Ingredient, Base, Pizza, Drink, Dessert

# Create an engine
engine = create_engine('mysql+pymysql://root:qazWSX123%21%40%23@localhost/PDS')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Insert data
ingredients = [
    {'name': 'Mozzarella Cheese', 'cost': 1.50, 'is_vegetarian': True, 'is_vegan': False},
    {'name': 'Vegan Mozzarella Cheese', 'cost': 2.00, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Cheddar Cheese', 'cost': 1.50, 'is_vegetarian': True, 'is_vegan': False},
    {'name': 'Parmesan Cheese', 'cost': 1.75, 'is_vegetarian': True, 'is_vegan': False},
    {'name': 'Gorgonzola Cheese', 'cost': 2.00, 'is_vegetarian': True, 'is_vegan': False},
    {'name': 'Tomato Sauce', 'cost': 0.50, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Pizza Dough', 'cost': 2.00, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Pepperoni', 'cost': 3.00, 'is_vegetarian': False, 'is_vegan': False},
    {'name': 'Pineapple', 'cost': 1.00, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Bell Pepper', 'cost': 0.75, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Onion', 'cost': 0.50, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Black Olives', 'cost': 1.00, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Chicken', 'cost': 3.50, 'is_vegetarian': False, 'is_vegan': False},
    {'name': 'Curry Sauce', 'cost': 1.50, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Kebab Meat', 'cost': 3.50, 'is_vegetarian': False, 'is_vegan': False},
    {'name': 'Gyros Meat', 'cost': 3.00, 'is_vegetarian': False, 'is_vegan': False},
    {'name': 'Jalapeños', 'cost': 0.75, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Black Beans', 'cost': 0.75, 'is_vegetarian': True, 'is_vegan': True},
    {'name': 'Italian Sausage', 'cost': 3.00, 'is_vegetarian': False, 'is_vegan': False}
]

# Add and commit the data
for ingredient in ingredients:
    session.execute(insert(Ingredient).values(ingredient))

# Commit the transaction
session.commit()

# Close the session
session.close()