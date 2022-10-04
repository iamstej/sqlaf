from datetime import date, datetime

from sqlaf import exceptions, fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class BookingFilter(filters.Filter):
    created_at = fields.DateTimeField(Booking.created_at, operator="lt")
    date = fields.DateField(Booking.date)
    guest_names = fields.ArrayField(Booking.guest_names)
    name = fields.CharField(Booking.name, operator="icontains")
    number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gte")


class IntegerFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(
            created_at=datetime(2020, 1, 1, 9, 0, 0),
            date=date(2020, 1, 5),
            name="Jim Halpert",
            number_of_heads=2,
            guest_names=["michael", "pam"],
        )
        BookingFactory(
            created_at=datetime(2020, 1, 2, 9, 0, 0),
            date=date(2020, 1, 5),
            name="Michael Scott",
            number_of_heads=7,
            guest_names=["pam"],
        )
        BookingFactory(
            created_at=datetime(2020, 1, 1, 9, 0, 0),
            date=date(2020, 1, 6),
            name="Dwight Schrute",
            number_of_heads=4,
            guest_names=["michael", "pam"],
        )
        BookingFactory(
            created_at=datetime(2020, 1, 1, 9, 0, 0),
            date=date(2020, 1, 5),
            name="Pam Beesly",
            number_of_heads=2,
            guest_names=["michael"],
        )
        BookingFactory(
            created_at=datetime(2020, 1, 3, 9, 0, 0),
            date=date(2020, 1, 6),
            name="Kevin Malone",
            number_of_heads=1,
            guest_names=["michael"],
        )

    def test_filter(self):
        query = self.session.query(Booking)
        filtered_query = (
            BookingFilter(query)
            .filter(
                {
                    "name": "A",
                    "number_of_heads": 2,
                    "guest_names": ["pam"],
                    "date": "2020-01-05",
                    "created_at": "2020-01-01T10:00:00+0000",
                }
            )
            .all()
        )
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")

    def test_filter_with_query_string(self):
        query = self.session.query(Booking)
        filtered_query = (
            BookingFilter(query)
            .filter("?name=A&number_of_heads=2&guest_names=pam&date=2020-01-05&created_at=2020-01-01T10:00:00%2B0000")
            .all()
        )
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")

    def test_filter_with_query_string_no_prefix(self):
        query = self.session.query(Booking)
        filtered_query = (
            BookingFilter(query)
            .filter("name=A&number_of_heads=2&guest_names=pam&date=2020-01-05&created_at=2020-01-01T10:00:00%2B0000")
            .all()
        )
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")

    def test_filter_with_invalid_query_string(self):
        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter("name?=!").all()
        self.assertEqual(len(filtered_query), 5)

    def test_filter_with_invalid_query_string_type(self):
        with self.assertRaises(exceptions.QueryParamaterDataException):
            query = self.session.query(Booking)
            BookingFilter(query).filter(10).all()
