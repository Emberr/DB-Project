import sqlalchemy as sa
from sqlalchemy import Table, Column, INTEGER, VARCHAR, DateTime, Boolean, MetaData, ForeignKey
from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, DATE, INTEGER
from sqlalchemy import Table, Column, Integer, VARCHAR, Date, DateTime, ForeignKey, DECIMAL, Boolean

engine = sa.create_engine('mysql://root:ASALanas20)%@localhost/PizzaDeliverySystem')
metadata = sa.MetaData()

# Customer table
customer = Table('customer', metadata,
    Column('customer_id', INTEGER, primary_key=True),
    Column('name', VARCHAR(25)),
    Column('birthdate', DATE),
    Column('phone_number', VARCHAR(15)),
    Column('address', VARCHAR(50)),
    Column('username', VARCHAR(10)),
    Column('password', VARCHAR(255)),
    Column('total_pizzas_ordered', INTEGER)
)

# DiscountCode table
discount_code = Table('discount_code', metadata,
    Column('code', VARCHAR(7), primary_key=True),
    Column('discount_percent', DECIMAL(3, 2)),
    Column('is_used', Boolean),
    Column('customer_id', INTEGER, ForeignKey('customer.customer_id')),
    Column('valid_to', DATE)
)

# Orders table
orders = Table('orders', metadata,
    Column('order_id', INTEGER, primary_key=True),
    Column('customer_id', INTEGER, ForeignKey('customer.customer_id')),
    Column('order_datetime', DateTime),
    Column('status', VARCHAR(15)),
    Column('eta', DateTime),
    Column('delivery_address', VARCHAR(50)),
    Column('cancellation_deadline', DateTime),
    Column('discount_code', VARCHAR(7), ForeignKey('discount_code.code')),
    Column('total_price', DECIMAL(7, 2)),
    Column('is_birthday_applied', Boolean)
)

# Pizza table
pizza = Table('pizza', metadata,
    Column('pizza_id', INTEGER, primary_key=True),
    Column('name', VARCHAR(25)),
    Column('price', DECIMAL(5, 2)),
    Column('is_vegetarian', Boolean),
    Column('is_vegan', Boolean)
)

# Ingredient table
ingredient = Table('ingredient', metadata,
    Column('ingredient_id', INTEGER, primary_key=True),
    Column('name', VARCHAR(25)),
    Column('cost', DECIMAL(5, 2)),
    Column('is_vegetarian', Boolean),
    Column('is_vegan', Boolean)
)

# PizzaIngredient table
pizza_ingredient = Table('pizza_ingredient', metadata,
    Column('pizza_id', INTEGER, ForeignKey('pizza.pizza_id'), primary_key=True),
    Column('ingredient_id', INTEGER, ForeignKey('ingredient.ingredient_id'), primary_key=True)
)

# OrderPizza table
order_pizza = Table('order_pizza', metadata,
    Column('pizza_id', INTEGER, ForeignKey('pizza.pizza_id'), primary_key=True),
    Column('order_id', INTEGER, ForeignKey('orders.order_id'), primary_key=True),
    Column('quantity', INTEGER)
)

# Dessert table
dessert = Table('dessert', metadata,
    Column('dessert_id', INTEGER, primary_key=True),
    Column('name', VARCHAR(25)),
    Column('cost', DECIMAL(5, 2))
)

# OrderDessert table
order_dessert = Table('order_dessert', metadata,
    Column('dessert_id', INTEGER, ForeignKey('dessert.dessert_id'), primary_key=True),
    Column('order_id', INTEGER, ForeignKey('orders.order_id'), primary_key=True),
    Column('quantity', INTEGER)
)

# Drink table
drink = Table('drink', metadata,
    Column('drink_id', INTEGER, primary_key=True),
    Column('name', VARCHAR(25)),
    Column('cost', DECIMAL(5, 2))
)

# OrderDrink table
order_drink = Table('order_drink', metadata,
    Column('drink_id', INTEGER, ForeignKey('drink.drink_id'), primary_key=True),
    Column('order_id', INTEGER, ForeignKey('orders.order_id'), primary_key=True),
    Column('quantity', INTEGER)
)

# DeliveryPerson table
delivery_person = Table('delivery_person', metadata,
    Column('deliverer_id', INTEGER, primary_key=True),
    Column('name', VARCHAR(25)),
    Column('shift', Boolean),
    Column('is_available', Boolean)
)

# Delivery table
delivery = Table('delivery', metadata,
    Column('delivery_id', INTEGER, primary_key=True),
    Column('deliverer_id', INTEGER, ForeignKey('delivery_person.deliverer_id')),
    Column('start_time', DateTime),
    Column('status', VARCHAR(15),)
)

# DeliveryOrder table
delivery_order = Table('delivery_order', metadata,
    Column('delivery_id', INTEGER, ForeignKey('delivery.delivery_id'), primary_key=True),
    Column('order_id', INTEGER, ForeignKey('orders.order_id'), primary_key=True)
)




metadata.create_all(engine)