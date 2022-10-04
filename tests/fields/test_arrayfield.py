from sqlaf import fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class BooleanFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(guest_names=["michael", "dwight", "pam", "jim"])
        BookingFactory(guest_names=["kevin", "angela", "toby", "michael"])
        BookingFactory(guest_names=["jim", "michael"])

    # contains operator

    def test_contains_filter_with_string_array_single_item(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": "jim"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].guest_names, ["michael", "dwight", "pam", "jim"])
        self.assertEqual(filtered_query[1].guest_names, ["jim", "michael"])

    def test_contains_filter_with_string_array_multiple_items(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": "jim,michael"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].guest_names, ["michael", "dwight", "pam", "jim"])
        self.assertEqual(filtered_query[1].guest_names, ["jim", "michael"])

    def test_contains_filter_with_array_single_item(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": ["jim"]}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].guest_names, ["michael", "dwight", "pam", "jim"])
        self.assertEqual(filtered_query[1].guest_names, ["jim", "michael"])

    def test_contains_filter_with_array_multiple_items(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": ["jim", "michael"]}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].guest_names, ["michael", "dwight", "pam", "jim"])
        self.assertEqual(filtered_query[1].guest_names, ["jim", "michael"])

    # ~contains operator

    def test_not_contains_filter_with_string_array_single_item(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names, operator="~contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": "jim"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].guest_names, ["kevin", "angela", "toby", "michael"])

    def test_not_contains_filter_with_string_array_multiple_items(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names, operator="~contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": "jim,michael"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].guest_names, ["kevin", "angela", "toby", "michael"])

    def test_not_contains_filter_with_array_single_item(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names, operator="~contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": ["jim"]}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].guest_names, ["kevin", "angela", "toby", "michael"])

    def test_not_contains_filter_with_array_multiple_items(self):
        class BookingFilter(filters.Filter):
            guest_names = fields.ArrayField(Booking.guest_names, operator="~contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"guest_names": ["jim", "michael"]}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].guest_names, ["kevin", "angela", "toby", "michael"])
