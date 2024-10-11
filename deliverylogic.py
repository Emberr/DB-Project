from datetime import datetime, timedelta

from TABLES import DeliveryPerson, Delivery, Order, OrderPizza, DeliveryOrder, Session
import threading
import time

def assign_delivery():
    print('Assigning delivery')
    db_session = Session()
    pending_orders = db_session.query(Order).filter_by(status='Preparing').all()
    print(f'Found {len(pending_orders)} pending orders')

    for order in pending_orders:
        print('Assigning delivery for order', order.order_id)
        postal_code = order.delivery_address[:4]
        delivery_person = db_session.query(DeliveryPerson).filter(
            DeliveryPerson.postal_code == postal_code,
            DeliveryPerson.next_available <= datetime.now()
        ).first()

        if not delivery_person:
            delivery_person = db_session.query(DeliveryPerson).filter(
                DeliveryPerson.postal_code == postal_code
            ).order_by(DeliveryPerson.next_available).first()

        recent_deliveries = db_session.query(Delivery).filter(
            Delivery.deliverer_id == delivery_person.deliverer_id,
            Delivery.start_time >= datetime.now() - timedelta(minutes=3),
            Delivery.status == 'In Oven'
        ).all()

        total_pizzas = sum(
            db_session.query(OrderPizza).filter(
                OrderPizza.order_id == delivery_order.order_id
            ).count()
            for delivery in recent_deliveries
            for delivery_order in delivery.orders
        )
        print(total_pizzas)

        current_order_pizzas = db_session.query(OrderPizza).filter_by(order_id=order.order_id).count()

        if len(recent_deliveries) < 3 and total_pizzas + current_order_pizzas <= 3:
            if not recent_deliveries:
                new_delivery = Delivery(
                    deliverer_id=delivery_person.deliverer_id,
                    start_time=datetime.now(),
                    status='In Oven'
                )
                db_session.add(new_delivery)
                db_session.commit()
                print('New delivery created')
                db_session.refresh(new_delivery)
            else:
                new_delivery = recent_deliveries[0]

            delivery_order = DeliveryOrder(
                delivery_id=new_delivery.delivery_id,
                order_id=order.order_id
            )
            db_session.add(delivery_order)
            order.status = 'In Oven'

            if delivery_person.is_available:
                order.eta = datetime.now() + timedelta(minutes=18)
                delivery_person.next_available = datetime.now() + timedelta(minutes=30)
                db_session.commit()

            else:
                order.eta = delivery_person.next_available + timedelta(minutes=15)
                db_session.commit()
            if delivery_person.is_available:
                threading.Thread(target=update_order_status_after_delay,
                                 args=(order.order_id, new_delivery.delivery_id, delivery_person.deliverer_id)).start()
            else:
                threading.Thread(target=wait_for_delivery,
                                 args=(order.order_id, new_delivery.delivery_id, delivery_person.deliverer_id)).start
        else:
            print('Delivery person currently out, wait time increased')
            new_delivery = Delivery(
                deliverer_id=delivery_person.deliverer_id,
                start_time=datetime.now(),
                status='In Oven'
            )
            db_session.add(new_delivery)
            db_session.commit()
            print('New delivery created')
            db_session.refresh(new_delivery)
            order.eta = datetime.now() + timedelta(minutes=48)
            order.status = 'In Oven'
            delivery_order = DeliveryOrder(
                delivery_id=new_delivery.delivery_id,
                order_id=order.order_id
            )
            db_session.add(delivery_order)
            db_session.commit()
            threading.Thread(target=wait_for_delivery, args=(order.order_id, new_delivery.delivery_id, delivery_person.deliverer_id)).start()

def update_order_status_after_delay(order_id, delivery_id, deliverer_id):
    time.sleep(180)
    db_session = Session()
    order = db_session.query(Order).filter_by(order_id=order_id).first()
    delivery = db_session.query(Delivery).filter_by(delivery_id=delivery_id).first()
    delivery_person = db_session.query(DeliveryPerson).filter_by(deliverer_id=deliverer_id).first()
    print('Checking order status')
    if order and order.status == 'In Oven':
        print('Updating order status')
        order.status = 'Out for Delivery'
        delivery.status = 'Out for Delivery'
        delivery_person.is_available = False
        db_session.commit()
    while True:
        current_time = datetime.now()
        if order and order.status == 'Out for Delivery' and current_time >= order.eta:
            order.status = 'Delivered'
            delivery.status = 'Delivered'
            db_session.commit()
            print(f'Order {order_id} status updated to Delivered')

        if delivery_person and current_time >= delivery_person.next_available:
            delivery_person.is_available = True
            db_session.commit()
            print(f'Delivery person {deliverer_id} is now available')
            break

        time.sleep(30)
    db_session.close()

def wait_for_delivery(order_id, delivery_id, deliverer_id):
    time.sleep(180)
    db_session = Session()
    order = db_session.query(Order).filter_by(order_id=order_id).first()
    delivery = db_session.query(Delivery).filter_by(delivery_id=delivery_id).first()
    delivery_person = db_session.query(DeliveryPerson).filter_by(deliverer_id=deliverer_id).first()

    if order and order.status == 'In Oven':
        order.status = 'Waiting for Delivery'
        db_session.commit()
        print(f'Order {order_id} status updated to Waiting for Delivery')

    while True:
        current_time = datetime.now()
        if delivery_person and current_time >= delivery_person.next_available:
            order.status = 'Out for Delivery'
            delivery.status = 'Out for Delivery'
            delivery_person.next_available = delivery_person.next_available + timedelta(minutes=30)
            delivery_person.is_available = False
            db_session.commit()
            print(f'Order {order_id} status updated to Out for Delivery')
            break

        time.sleep(30)  # Check every 30 seconds

    while True:
        current_time = datetime.now()
        if order and order.status == 'Out for Delivery' and current_time >= order.eta:
            order.status = 'Delivered'
            delivery.status = 'Delivered'
            db_session.commit()
            print(f'Order {order_id} status updated to Delivered')

        if delivery_person and current_time >= delivery_person.next_available:
            delivery_person.is_available = True
            db_session.commit()
            print(f'Delivery person {deliverer_id} is now available')
            break

        time.sleep(30)  # Check every 30 seconds

    db_session.close()