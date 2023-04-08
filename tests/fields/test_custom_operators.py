from sqlaf import fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


def lower_case_eq(field, value) -> bool:
    return field == value.lower()


class CustomOperatorTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(name="100% michael scott")
        BookingFactory(name="jim halpert")
        BookingFactory(name="pam halpert\beesly")  # NOQA

    def test_custom_operator(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator=lower_case_eq)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "Jim Halpert"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "jim halpert")
