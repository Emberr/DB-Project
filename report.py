from flask import Blueprint, render_template, request
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
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
        age_min = request.form.get('age_min')
        age_max = request.form.get('age_max')
        month = request.form.get('month')

        if region:
            filters['region'] = region
        if gender:
            filters['gender'] = gender
        if age_min:
            filters['age_min'] = int(age_min)
        if age_max:
            filters['age_max'] = int(age_max)
        if month:
            filters['month'] = month

    query = session.query(
        func.date_format(Order.order_datetime, '%Y-%m').label('month'),
        func.sum(Order.total_price).label('total_earnings'),
        func.count(Order.order_id).label('total_orders')
    ).join(Customer).group_by('month')

    if 'region' in filters:
        query = query.filter(Customer.address == filters['region'])
    if 'gender' in filters:
        query = query.filter(Customer.gender == filters['gender'])
    if 'age_min' in filters and 'age_max' in filters:
        customers_with_age = session.query(Customer.customer_id).filter(
            func.year(datetime.today()) - func.year(Customer.birthdate) - (
                (func.month(datetime.today()), func.day(datetime.today())) < (func.month(Customer.birthdate), func.day(Customer.birthdate))
            ).between(filters['age_min'], filters['age_max'])
        ).subquery()
        query = query.filter(Order.customer_id.in_(customers_with_age))
    if 'month' in filters:
        query = query.filter(func.date_format(Order.order_datetime, '%Y-%m') == filters['month'])

    report_data = query.all()
    session.close()

    report_dict = {row.month: {'total_earnings': row.total_earnings, 'total_orders': row.total_orders} for row in report_data}

    if 'month' in filters:
        final_report_data = [{
            'month': filters['month'],
            'total_earnings': report_dict.get(filters['month'], {}).get('total_earnings', 0),
            'total_orders': report_dict.get(filters['month'], {}).get('total_orders', 0)
        }]
    else:
        final_report_data = [{
            'month': month,
            'total_earnings': report_dict.get(month, {}).get('total_earnings', 0),
            'total_orders': report_dict.get(month, {}).get('total_orders', 0)
        } for month in report_dict]

    return render_template('report.html', report_data=final_report_data, filters=filters)