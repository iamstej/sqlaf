from sqlaf import exceptions, fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class BooleanFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(has_paid=True)
        BookingFactory(has_paid=True)
        BookingFactory(has_paid=False)

    # eq operator

    def test_eq_filter(self):
        class BookingFilter(filters.Filter):
            has_paid = fields.BooleanField(Booking.has_paid)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"has_paid": True}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].has_paid, True)
        self.assertEqual(filtered_query[1].has_paid, True)

    def test_eq_filter_truthy_values(self):
        class BookingFilter(filters.Filter):
            has_paid = fields.BooleanField(Booking.has_paid, truthy=["has_paid"])

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"has_paid": "has_paid"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].has_paid, True)
        self.assertEqual(filtered_query[1].has_paid, True)

    def test_eq_filter_truthy_value_not_exist(self):
        class BookingFilter(filters.Filter):
            has_paid = fields.BooleanField(Booking.has_paid)

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"has_paid": "yes"}).all()

    def test_eq_filter_none_value(self):
        class BookingFilter(filters.Filter):
            has_paid = fields.BooleanField(Booking.has_paid)

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"has_paid": None}).all()

    # Edge cases

    def test_invalid_operator(self):
        with self.assertRaises(exceptions.FieldInstantiationException):

            class _(filters.Filter):
                has_paid = fields.BooleanField(Booking.has_paid, operator="~eq")
