from datetime import time, timezone

from sqlaf import fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class TimeFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(time=time(13, 0, tzinfo=timezone.utc))
        BookingFactory(time=time(15, 0, tzinfo=timezone.utc))
        BookingFactory(time=time(10, 0, tzinfo=timezone.utc))
        BookingFactory(time=time(17, 0, tzinfo=timezone.utc))
        BookingFactory(time=time(20, 0, tzinfo=timezone.utc))

    # eq operator

    def test_eq_filter(self):
        class BookingFilter(filters.Filter):
            time = fields.TimeField(Booking.time)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"time": "13:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].time, time(13, 0, tzinfo=timezone.utc))

    # # # ~eq operator

    def test_not_eq_filter(self):
        class BookingFilter(filters.Filter):
            time = fields.TimeField(Booking.time, "~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"time": "13:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 4)
        self.assertEqual(filtered_query[0].time, time(15, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[1].time, time(10, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[2].time, time(17, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[3].time, time(20, 0, tzinfo=timezone.utc))

    # # # gt operator

    def test_gt_filter(self):
        class BookingFilter(filters.Filter):
            time = fields.TimeField(Booking.time, "gt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"time": "13:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].time, time(15, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[1].time, time(17, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[2].time, time(20, 0, tzinfo=timezone.utc))

    # # # gte operator

    def test_gte_filter(self):
        class BookingFilter(filters.Filter):
            time = fields.TimeField(Booking.time, "gte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"time": "13:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 4)
        self.assertEqual(filtered_query[0].time, time(13, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[1].time, time(15, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[2].time, time(17, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[3].time, time(20, 0, tzinfo=timezone.utc))

    # # # lt operator

    def test_lt_filter(self):
        class BookingFilter(filters.Filter):
            time = fields.TimeField(Booking.time, "lt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"time": "15:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].time, time(13, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[1].time, time(10, 0, tzinfo=timezone.utc))

    # # # lte operator

    def test_lte_filter(self):
        class BookingFilter(filters.Filter):
            time = fields.TimeField(Booking.time, "lte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"time": "15:00:00+0000"}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].time, time(13, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[1].time, time(15, 0, tzinfo=timezone.utc))
        self.assertEqual(filtered_query[2].time, time(10, 0, tzinfo=timezone.utc))
