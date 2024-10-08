from flask import Blueprint, render_template, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from TABLES import Customer, Order, engine
from datetime import datetime

report_pointer = Blueprint('report', __name__)
Session = sessionmaker(bind=engine)

def calculate_age(birthdate):
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

@report_pointer.route('/report', methods=['GET', 'POST'])
def report():
    session = Session()
    filters = {}
    if request.method == 'POST':
        region = request.form.get('region')
        gender = request.form.get('gender')
        age = request.form.get('age')

        if region:
            filters['region'] = region
        if gender:
            filters['gender'] = gender
        if age:
            filters['age'] = int(age)

    query = session.query(
        func.date_format(Order.order_datetime, '%Y-%m').label('month'),
        func.sum(Order.total_price).label('total_earnings')
    ).join(Customer).group_by('month')

    if 'region' in filters:
        query = query.filter((Customer.address == filters['region']) | (Customer.postal_code == filters['region']))
    if 'gender' in filters:
        query = query.filter(Customer.gender == filters['gender'])
    if 'age' in filters:
        customers_with_age = session.query(Customer.customer_id).filter(
            func.year(datetime.today()) - func.year(Customer.birthdate) - (
                (func.month(datetime.today()), func.day(datetime.today())) < (func.month(Customer.birthdate), func.day(Customer.birthdate))
            ) == filters['age']
        ).subquery()
        query = query.filter(Order.customer_id.in_(customers_with_age))

    report_data = query.all()
    session.close()

    return render_template('report.html', report_data=report_data, filters=filters)