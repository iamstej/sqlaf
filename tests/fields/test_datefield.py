from datetime import date

from sqlaf import fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class DateFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(date=date(2022, 1, 1))
        BookingFactory(date=date(2022, 1, 1))
        BookingFactory(date=date(2022, 1, 2))
        BookingFactory(date=date(2022, 1, 1))
        BookingFactory(date=date(2022, 1, 4))

    # eq operator

    def test_eq_filter(self):
        class BookingFilter(filters.Filter):
            date = fields.DateField(Booking.date)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"date": "2022-01-01"}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[1].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[2].date, date(2022, 1, 1))

    # ~eq operator

    def test_not_eq_filter(self):
        class BookingFilter(filters.Filter):
            date = fields.DateField(Booking.date, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"date": "2022-01-01"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].date, date(2022, 1, 2))
        self.assertEqual(filtered_query[1].date, date(2022, 1, 4))

    # gt operator

    def test_gt_filter(self):
        class BookingFilter(filters.Filter):
            date = fields.DateField(Booking.date, operator="gt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"date": "2022-01-01"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].date, date(2022, 1, 2))
        self.assertEqual(filtered_query[1].date, date(2022, 1, 4))

    # gte operator

    def test_gte_filter(self):
        class BookingFilter(filters.Filter):
            date = fields.DateField(Booking.date, operator="gte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"date": "2022-01-01"}).all()
        self.assertEqual(len(filtered_query), 5)
        self.assertEqual(filtered_query[0].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[1].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[2].date, date(2022, 1, 2))
        self.assertEqual(filtered_query[3].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[4].date, date(2022, 1, 4))

    # lt operator

    def test_lt_filter(self):
        class BookingFilter(filters.Filter):
            date = fields.DateField(Booking.date, operator="lt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"date": "2022-01-02"}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[1].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[2].date, date(2022, 1, 1))

    # lte operator

    def test_lte_filter(self):
        class BookingFilter(filters.Filter):
            date = fields.DateField(Booking.date, operator="lte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"date": "2022-01-02"}).all()
        self.assertEqual(len(filtered_query), 4)
        self.assertEqual(filtered_query[0].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[1].date, date(2022, 1, 1))
        self.assertEqual(filtered_query[2].date, date(2022, 1, 2))
        self.assertEqual(filtered_query[3].date, date(2022, 1, 1))
