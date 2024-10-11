from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from TABLES import Ingredient, Base, Pizza, Drink, Dessert, PizzaIngredient

password = 'qazWSX123%21%40%23'

# Create an engine
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/PDS')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()



# Insert data
pizza_ingredients = [
    # Gooey Cheese ALL Over Your Face (Four Cheese Pizza)
    {'pizza_id': 1, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 1, 'ingredient_id': 3},  # Cheddar Cheese
    {'pizza_id': 1, 'ingredient_id': 4},  # Parmesan Cheese
    {'pizza_id': 1, 'ingredient_id': 5},  # Gorgonzola Cheese
    {'pizza_id': 1, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 1, 'ingredient_id': 7},  # Pizza Dough

    # So Not Halal Mode (Pepperoni Pizza)
    {'pizza_id': 2, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 2, 'ingredient_id': 8},  # Pepperoni
    {'pizza_id': 2, 'ingredient_id': 19},  # Italian Sausage
    {'pizza_id': 2, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 2, 'ingredient_id': 7},  # Pizza Dough

    # Performance Enhancer (Pineapple Pizza)
    {'pizza_id': 3, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 3, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 3, 'ingredient_id': 7},  # Pizza Dough
    {'pizza_id': 3, 'ingredient_id': 9},  # Pineapple

    # Veggie Virgin (Vegetarian Pizza)
    {'pizza_id': 4, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 4, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 4, 'ingredient_id': 7},  # Pizza Dough
    {'pizza_id': 4, 'ingredient_id': 10},  # Bell Pepper
    {'pizza_id': 4, 'ingredient_id': 11},  # Onion
    {'pizza_id': 4, 'ingredient_id': 12},  # Black Olives

    # Vegan (Not good, do not order)
    {'pizza_id': 5, 'ingredient_id': 2},  # Vegan Mozzarella Cheese
    {'pizza_id': 5, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 5, 'ingredient_id': 7},  # Pizza Dough

    # Indian Slums (Chicken Curry Pizza)
    {'pizza_id': 6, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 6, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 6, 'ingredient_id': 7},  # Pizza Dough
    {'pizza_id': 6, 'ingredient_id': 13},  # Chicken
    {'pizza_id': 6, 'ingredient_id': 14},  # Curry Sauce

    # The Border Jumper (Mexican Pizza)
    {'pizza_id': 7, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 7, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 7, 'ingredient_id': 7},  # Pizza Dough
    {'pizza_id': 7, 'ingredient_id': 17},  # Jalapeños
    {'pizza_id': 7, 'ingredient_id': 18},  # Black Beans

    # O'Block (Chicago's Finest Pizza)
    {'pizza_id': 8, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 8, 'ingredient_id': 3},  # Cheddar Cheese
    {'pizza_id': 8, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 8, 'ingredient_id': 7},  # Pizza Dough
    {'pizza_id': 8, 'ingredient_id': 8},  # Pepperoni
    {'pizza_id': 8, 'ingredient_id': 19},  # Italian Sausage

    # The Bomber (Kebab Pizza)
    {'pizza_id': 9, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 9, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 9, 'ingredient_id': 7},  # Pizza Dough
    {'pizza_id': 9, 'ingredient_id': 15},  # Kebab Meat

    # The Greek Freak (Gyros Pizza)
    {'pizza_id': 10, 'ingredient_id': 1},  # Mozzarella Cheese
    {'pizza_id': 10, 'ingredient_id': 6},  # Tomato Sauce
    {'pizza_id': 10, 'ingredient_id': 7},  # Pizza Dough
    {'pizza_id': 10, 'ingredient_id': 16},  # Gyros Meat
]


for pizza_ingredient in pizza_ingredients:
    session.execute(insert(PizzaIngredient).values(pizza_ingredient))

session.commit()

session.close()