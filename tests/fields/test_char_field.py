from sqlaf import fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class CharFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(name="100% Michael Scott")
        BookingFactory(name="Jim Halpert")
        BookingFactory(name="Pam Halpert\Beesly")  # NOQA

    # eq operator

    def test_eq_filter(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "Jim Halpert"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")

    # ieq operator

    def test_ieq_filter(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="ieq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "jim halpert"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")

    # ~eq operator

    def test_not_eq_filter(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "Jim Halpert"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].name, "100% Michael Scott")
        self.assertEqual(filtered_query[1].name, "Pam Halpert\Beesly")  # NOQA

    # ~ieq operator

    def test_not_ieq_filter(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="~ieq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "jim halpert"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].name, "100% Michael Scott")
        self.assertEqual(filtered_query[1].name, "Pam Halpert\Beesly")  # NOQA

    # contains operator

    def test_contains_filter(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "m Ha"}).order_by(Booking.name).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")
        self.assertEqual(filtered_query[1].name, "Pam Halpert\Beesly")  # NOQA

    def test_contains_filter_percentage_escape_check(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "100%"}).order_by(Booking.name).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "100% Michael Scott")

    def test_contains_filter_percentage_escape_check_single_char(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "%"}).order_by(Booking.name).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "100% Michael Scott")

    def test_contains_filter_backslash_escape_check(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "t\Be"}).order_by(Booking.name).all()  # NOQA
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Pam Halpert\Beesly")  # NOQA

    def test_contains_filter_backslash_escape_check_single_char(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "\\"}).order_by(Booking.name).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Pam Halpert\Beesly")  # NOQA

    def test_contains_filter_case_sensitive(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="contains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "m ha"}).order_by(Booking.name).all()
        self.assertEqual(len(filtered_query), 0)

    # icontains operator

    def test_icontains_filter(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="icontains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "m ha"}).order_by(Booking.name).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].name, "Jim Halpert")
        self.assertEqual(filtered_query[1].name, "Pam Halpert\Beesly")  # NOQA

    def test_icontains_filter_escaped(self):
        class BookingFilter(filters.Filter):
            name = fields.CharField(Booking.name, operator="icontains")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "t\\b"}).order_by(Booking.name).all()  # NOQA
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "Pam Halpert\Beesly")  # NOQA
