import factory

from tests.implementation.db import Session
from tests.implementation.models import Booking


class BookingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Booking
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "flush"
