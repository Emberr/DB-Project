from datetime import datetime, timedelta
from TABLES import DeliveryPerson, Delivery, Order, OrderPizza, DeliveryOrder, Session
import threading
import time
from sqlalchemy.exc import OperationalError

def assign_delivery():
    print('Assigning delivery')
    with Session() as db_session:
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
                Delivery.start_time >= datetime.now() - timedelta(seconds=180),
                Delivery.status == 'In Oven'
            ).all()

            total_pizzas = db_session.query(OrderPizza).join(
                DeliveryOrder, OrderPizza.order_id == DeliveryOrder.order_id
            ).join(
                Delivery, DeliveryOrder.delivery_id == Delivery.delivery_id
            ).filter(
                Delivery.deliverer_id == delivery_person.deliverer_id,
                Delivery.start_time >= datetime.now() - timedelta(seconds=180),
                Delivery.status == 'In Oven'
            ).count()

            print(total_pizzas)

            current_order_pizzas = db_session.query(OrderPizza).filter_by(order_id=order.order_id).count()
            print(current_order_pizzas)

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
                else:
                    order.eta = delivery_person.next_available + timedelta(minutes=48)

                db_session.merge(order)
                db_session.commit()
                db_session.refresh(order)
                print(f'Order {order.order_id} eta updated to {order.eta} and status updated to {order.status}')

                if delivery_person.is_available:
                    threading.Thread(target=update_order_status_after_delay,
                                     args=(order.order_id, new_delivery.delivery_id, delivery_person.deliverer_id)).start()
                else:
                    threading.Thread(target=wait_for_delivery,
                                     args=(order.order_id, new_delivery.delivery_id, delivery_person.deliverer_id)).start()
            else:
                try:
                    print('Delivery person currently out, wait time increased')
                    print('Checking for other delivery person')
                    new_delivery = Delivery(
                        deliverer_id=delivery_person.deliverer_id,
                        start_time=datetime.now(),
                        status='Preparing'
                    )
                    db_session.add(new_delivery)
                    db_session.commit()
                    db_session.refresh(new_delivery)
                    print('New delivery created')

                    order.eta = datetime.now() + timedelta(minutes=48)
                    order.status = 'In Oven'
                    db_session.merge(order)
                    db_session.commit()
                    db_session.refresh(order)
                    print(f'Order {order.order_id} eta updated to {order.eta} and status updated to {order.status}')

                    delivery_order = DeliveryOrder(
                        delivery_id=new_delivery.delivery_id,
                        order_id=order.order_id
                    )
                    db_session.add(delivery_order)
                    db_session.commit()
                    print('New delivery order created')
                    threading.Thread(target=wait_for_delivery,
                                     args=(order.order_id, new_delivery.delivery_id, delivery_person.deliverer_id)).start()
                except OperationalError as e:
                    print(f"An error occurred: {e}")

def update_order_status_after_delay(order_id, delivery_id, deliverer_id):
    time.sleep(180)
    with Session() as db_session:
        order = db_session.query(Order).filter_by(order_id=order_id).first()
        delivery = db_session.query(Delivery).filter_by(delivery_id=delivery_id).first()
        delivery_person = db_session.query(DeliveryPerson).filter_by(deliverer_id=deliverer_id).first()
        print('Checking order status')
        if order and order.status == 'In Oven':
            print('Updating order status')
            order.status = 'Out for Delivery'
            delivery.status = 'Out for Delivery'
            delivery_person.is_available = False
            delivery_person.next_available = datetime.now() + timedelta(minutes=30)
            db_session.commit()
            db_session.refresh(order)
            db_session.refresh(delivery)
            db_session.refresh(delivery_person)
            print(f'Order {order.order_id} status updated to {order.status}')

        while True:
            current_time = datetime.now()
            if order and order.status == 'Out for Delivery' and current_time >= order.eta:
                order.status = 'Delivered'
                delivery.status = 'Delivered'
                db_session.commit()
                db_session.refresh(order)
                db_session.refresh(delivery)
                print(f'Order {order.order_id} status updated to Delivered')

            if delivery_person and current_time >= delivery_person.next_available:
                delivery_person.is_available = True
                db_session.commit()
                db_session.refresh(delivery_person)
                print(f'Delivery person {deliverer_id} is now available')
                break

            time.sleep(20)

def wait_for_delivery(order_id, delivery_id, deliverer_id):
    time.sleep(180)
    with Session() as db_session:
        order = db_session.query(Order).filter_by(order_id=order_id).first()
        delivery = db_session.query(Delivery).filter_by(delivery_id=delivery_id).first()
        delivery_person = db_session.query(DeliveryPerson).filter_by(deliverer_id=deliverer_id).first()

        if order and order.status == 'In Oven':
            order.status = 'Waiting for Delivery'
            db_session.commit()
            db_session.refresh(order)
            print(f'Order {order.order_id} status updated to Waiting for Delivery')

        while True:
            current_time = datetime.now()
            if delivery_person and current_time >= delivery_person.next_available:
                order.status = 'Out for Delivery'
                delivery.status = 'Out for Delivery'
                delivery_person.next_available = delivery_person.next_available + timedelta(minutes=30)
                delivery_person.is_available = False
                db_session.commit()
                db_session.refresh(order)
                db_session.refresh(delivery)
                db_session.refresh(delivery_person)
                print(f'Order {order.order_id} status updated to Out for Delivery')
                break

            time.sleep(20)

        while True:
            current_time = datetime.now()
            if order and order.status == 'Out for Delivery' and current_time >= order.eta:
                order.status = 'Delivered'
                delivery.status = 'Delivered'
                db_session.commit()
                db_session.refresh(order)
                db_session.refresh(delivery)
                print(f'Order {order.order_id} status updated to Delivered')

            if delivery_person and current_time >= delivery_person.next_available:
                delivery_person.is_available = True
                db_session.commit()
                db_session.refresh(delivery_person)
                print(f'Delivery person {deliverer_id} is now available')
                break

            time.sleep(20)