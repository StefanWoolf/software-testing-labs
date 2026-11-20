import json
import logging
import time

log = logging.getLogger("notifications")


def receive_order_event(consumer, timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        msg = consumer.poll(1)
        if msg is None or msg.error():
            continue
        event = json.loads(msg.value())
        log.info("Новый заказ #%s: %s x%s", event["id"], event["item_name"], event["quantity"])
        return event
    raise TimeoutError("Событие о заказе не получено")
