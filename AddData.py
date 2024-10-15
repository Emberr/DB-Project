from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker
from TABLES import Ingredient, Base, Pizza, Drink, Dessert, PizzaIngredient, DeliveryPerson, DiscountCode
from datetime import datetime, timedelta

password = 'qazWSX123%21%40%23'

# Create an engine
engine = create_engine(f'mysql+pymysql://root:{password}@localhost/PDS')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session
session = Session()



# Insert data
pizza_ingredients = [
    {'code': 'QWERT1', 'discount_percent': 0.10, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'ASDFG2', 'discount_percent': 0.15, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'ZXCVB3', 'discount_percent': 0.20, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'YUIOP4', 'discount_percent': 0.05, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'HJKLZ5', 'discount_percent': 0.125, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'MNBVC6', 'discount_percent': 0.1875, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'PLMKO7', 'discount_percent': 0.22, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'JNHBG8', 'discount_percent': 0.075, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'QAZWS9', 'discount_percent': 0.25, 'valid_to': datetime.now() + timedelta(days=30)},
    {'code': 'XEDCR0', 'discount_percent': 0.17, 'valid_to': datetime.now() + timedelta(days=30)},
        ]


for pizza_ingredient in pizza_ingredients:
    session.execute(insert(DiscountCode).values(pizza_ingredient))

session.commit()

session.close()