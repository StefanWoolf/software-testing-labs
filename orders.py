import json

TOPIC = "orders"


def create_order(session, producer, order):
    session.add(order)
    session.commit()
    event = {"id": order.id, "item_name": order.item_name, "quantity": order.quantity}
    producer.produce(TOPIC, json.dumps(event).encode())
    producer.flush()
    return order
