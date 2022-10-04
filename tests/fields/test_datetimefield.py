from datetime import datetime, timezone

from sqlaf import fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class DateTimeFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(created_at=datetime(2022, 1, 1, 13, 0, tzinfo=timezone.utc))
        BookingFactory(created_at=datetime(2022, 1, 1, 15, 0, tzinfo=timezone.utc))
        BookingFactory(created_at=datetime(2022, 1, 2, 10, 0, tzinfo=timezone.utc))
        BookingFactory(created_at=datetime(2022, 1, 1, 17, 0, tzinfo=timezone.utc))
        BookingFactory(created_at=datetime(2022, 1, 4, 20, 0, tzinfo=timezone.utc))

    # eq operator

    def test_eq_filter(self):
        class BookingFilter(filters.Filter):
            created_at = fields.DateTimeField(Booking.created_at)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"created_at": "2022-01-01T13:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(
            filtered_query[0].created_at,
            datetime(2022, 1, 1, 13, 0, tzinfo=timezone.utc),
        )

    # # ~eq operator

    def test_not_eq_filter(self):
        class BookingFilter(filters.Filter):
            created_at = fields.DateTimeField(Booking.created_at, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"created_at": "2022-01-01T13:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 4)
        self.assertEqual(
            filtered_query[0].created_at,
            datetime(2022, 1, 1, 15, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[1].created_at,
            datetime(2022, 1, 2, 10, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[2].created_at,
            datetime(2022, 1, 1, 17, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[3].created_at,
            datetime(2022, 1, 4, 20, 0, tzinfo=timezone.utc),
        )

    # # gt operator

    def test_gt_filter(self):
        class BookingFilter(filters.Filter):
            created_at = fields.DateTimeField(Booking.created_at, operator="gt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"created_at": "2022-01-01T15:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(
            filtered_query[0].created_at,
            datetime(2022, 1, 2, 10, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[1].created_at,
            datetime(2022, 1, 1, 17, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[2].created_at,
            datetime(2022, 1, 4, 20, 0, tzinfo=timezone.utc),
        )

    # # gte operator

    def test_gte_filter(self):
        class BookingFilter(filters.Filter):
            created_at = fields.DateTimeField(Booking.created_at, operator="gte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"created_at": "2022-01-01T15:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 4)
        self.assertEqual(
            filtered_query[0].created_at,
            datetime(2022, 1, 1, 15, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[1].created_at,
            datetime(2022, 1, 2, 10, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[2].created_at,
            datetime(2022, 1, 1, 17, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[3].created_at,
            datetime(2022, 1, 4, 20, 0, tzinfo=timezone.utc),
        )

    # # lt operator

    def test_lt_filter(self):
        class BookingFilter(filters.Filter):
            created_at = fields.DateTimeField(Booking.created_at, operator="lt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"created_at": "2022-01-01T17:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(
            filtered_query[0].created_at,
            datetime(2022, 1, 1, 13, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[1].created_at,
            datetime(2022, 1, 1, 15, 0, tzinfo=timezone.utc),
        )

    # # lte operator

    def test_lte_filter(self):
        class BookingFilter(filters.Filter):
            created_at = fields.DateTimeField(Booking.created_at, operator="lte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"created_at": "2022-01-01T17:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(
            filtered_query[0].created_at,
            datetime(2022, 1, 1, 13, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[1].created_at,
            datetime(2022, 1, 1, 15, 0, tzinfo=timezone.utc),
        )
        self.assertEqual(
            filtered_query[2].created_at,
            datetime(2022, 1, 1, 17, 0, tzinfo=timezone.utc),
        )
