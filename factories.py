import factory

from models import Order


class OrderFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Order
        sqlalchemy_session_persistence = "commit"

    item_name = factory.Faker("word")
    quantity = factory.Faker("pyint", min_value=1, max_value=100)
