from typing import Dict, List

from sqlaf import fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class PostProcessTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(name="Jim Halpert", has_paid=True)
        BookingFactory(name="Micheal Scott", has_paid=True)
        BookingFactory(name="Jim Halpert", has_paid=False)

    def test_post_process(self):
        class BookingFilter(filters.Filter):
            has_paid = fields.BooleanField(Booking.has_paid)

            def post_filter(self, data: Dict, filters: List):
                if "name" in data:
                    filters.append(Booking.name == data.get("name"))

                return filters

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "Jim Halpert", "has_paid": True}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")
        self.assertEqual(filtered_query[0].has_paid, True)
