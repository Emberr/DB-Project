import sqlalchemy as sa
from sqlalchemy.dialects.mysql import DECIMAL, VARCHAR, DATE, INTEGER
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean, insert
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

password = 'qazWSX123%21%40%23'

engine = sa.create_engine(f'mysql+pymysql://root:{password}@localhost/PDS')
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(25))
    birthdate = Column(Date)
    phone_number = Column(String(15))
    address = Column(String(50))
    username = Column(String(20), unique=True)
    password = Column(String(255))
    total_pizzas_ordered = Column(Integer)
    gender = Column(String(6))
    orders = relationship('Order', back_populates='customer')

class DiscountCode(Base):
    __tablename__ = 'discount_code'
    code = Column(String(7), primary_key=True)
    discount_percent = Column(DECIMAL(3, 2))
    valid_to = Column(Date)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    order_datetime = Column(DateTime)
    status = Column(String(50))
    eta = Column(DateTime)
    delivery_address = Column(String(50))
    total_price = Column(DECIMAL(7, 2))
    customer = relationship('Customer', back_populates='orders')
    pizzas = relationship('OrderPizza', back_populates='order')
    desserts = relationship('OrderDessert', back_populates='order')
    drinks = relationship('OrderDrink', back_populates='order')

class Pizza(Base):
    __tablename__ = 'pizza'
    pizza_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    ingredients = relationship('PizzaIngredient', back_populates='pizza')

class Ingredient(Base):
    __tablename__ = 'ingredient'
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(255))
    cost = Column(DECIMAL(5, 2))
    is_vegetarian = Column(Boolean)
    is_vegan = Column(Boolean)
    pizzas = relationship('PizzaIngredient', back_populates='ingredient')

class PizzaIngredient(Base):
    __tablename__ = 'pizza_ingredient'
    pizza_id = Column(Integer, ForeignKey('pizza.pizza_id'), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.ingredient_id'), primary_key=True)
    pizza = relationship('Pizza', back_populates='ingredients')
    ingredient = relationship('Ingredient', back_populates='pizzas')

class OrderPizza(Base):
    __tablename__ = 'order_pizza'
    pizza_id = Column(Integer, ForeignKey('pizza.pizza_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    quantity = Column(Integer)
    order = relationship('Order', back_populates='pizzas')
    pizza = relationship('Pizza')

class Dessert(Base):
    __tablename__ = 'dessert'
    dessert_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    cost = Column(DECIMAL(5, 2))
    orders = relationship('OrderDessert', back_populates='dessert')

class OrderDessert(Base):
    __tablename__ = 'order_dessert'
    dessert_id = Column(Integer, ForeignKey('dessert.dessert_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    quantity = Column(Integer)
    order = relationship('Order', back_populates='desserts')
    dessert = relationship('Dessert', back_populates='orders')

class Drink(Base):
    __tablename__ = 'drink'
    drink_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    cost = Column(DECIMAL(5, 2))
    orders = relationship('OrderDrink', back_populates='drink')

class OrderDrink(Base):
    __tablename__ = 'order_drink'
    drink_id = Column(Integer, ForeignKey('drink.drink_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    quantity = Column(Integer)
    order = relationship('Order', back_populates='drinks')
    drink = relationship('Drink', back_populates='orders')

class DeliveryPerson(Base):
    __tablename__ = 'delivery_person'
    deliverer_id = Column(Integer, primary_key=True)
    name = Column(String(25))
    is_available = Column(Boolean)
    postal_code = Column(String(4))
    next_available = Column(DateTime)
    deliveries = relationship('Delivery', back_populates='deliverer')

class Delivery(Base):
    __tablename__ = 'delivery'
    delivery_id = Column(Integer, primary_key=True)
    deliverer_id = Column(Integer, ForeignKey('delivery_person.deliverer_id'))
    start_time = Column(DateTime)
    status = Column(String(50))
    deliverer = relationship('DeliveryPerson', back_populates='deliveries')
    orders = relationship('DeliveryOrder', back_populates='delivery')

class DeliveryOrder(Base):
    __tablename__ = 'delivery_order'
    delivery_id = Column(Integer, ForeignKey('delivery.delivery_id'), primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    delivery = relationship('Delivery', back_populates='orders')
    order = relationship('Order')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
