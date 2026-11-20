import logging

import pytest
from confluent_kafka import Consumer, Producer
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session
from testcontainers.community.kafka import KafkaContainer
from testcontainers.community.postgres import PostgresContainer

import notifications
import orders
from factories import OrderFactory
from models import Base, Order


@pytest.fixture(scope="module")
def session():
    with PostgresContainer("postgres:16-alpine") as pg:
        engine = create_engine(pg.get_connection_url())
        Base.metadata.create_all(engine)
        with Session(engine) as s:
            OrderFactory._meta.sqlalchemy_session = s
            yield s


@pytest.fixture(scope="module")
def kafka():
    with KafkaContainer() as k:
        yield k.get_bootstrap_server()


def test_order_flow(session, kafka, caplog):
    OrderFactory.create_batch(3)
    order = OrderFactory.build()

    orders.create_order(session, Producer({"bootstrap.servers": kafka}), order)

    session.expire_all()
    saved = session.get(Order, order.id)
    assert (saved.item_name, saved.quantity) == (order.item_name, order.quantity)
    assert session.scalar(select(func.count()).select_from(Order)) == 4

    consumer = Consumer({
        "bootstrap.servers": kafka,
        "group.id": "notifications",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe([orders.TOPIC])
    with caplog.at_level(logging.INFO, logger="notifications"):
        event = notifications.receive_order_event(consumer)
    consumer.close()

    assert event["id"] == order.id
    assert event["item_name"] == order.item_name
    assert order.item_name in caplog.text
