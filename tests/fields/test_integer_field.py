from sqlaf import exceptions, fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class IntegerFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(number_of_heads=3)
        BookingFactory(number_of_heads=4)
        BookingFactory(number_of_heads=5)

    # eq operator

    def test_eq_filter(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 4)

    def test_eq_filter_string_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "4"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 4)

    def test_eq_filter_none_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": None}).all()
        self.assertEqual(len(filtered_query), 0)

    def test_eq_filter_invalid_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads)

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": "four"}).all()

    def test_eq_filter_with_default(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, default=3)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 3)

    # ~eq operator

    def test_not_eq_filter(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).order_by(Booking.number_of_heads).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 5)

    def test_not_eq_filter_string_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "4"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 5)

    def test_not_eq_filter_none_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": None}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 4)
        self.assertEqual(filtered_query[2].number_of_heads, 5)

    def test_not_eq_filter_invalid_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="~eq")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": "four"}).all()

    def test_not_eq_filter_with_default(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="~eq", default=3)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({}).order_by(Booking.number_of_heads).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 4)
        self.assertEqual(filtered_query[1].number_of_heads, 5)

    # gt operator

    def test_gt_filter(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).order_by(Booking.number_of_heads).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 5)

    def test_gt_filter_string_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "4"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 5)

    def test_gt_filter_none_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gt")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.OperatorArgumentError):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": None}).all()

    def test_gt_filter_invalid_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gt")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": "four"}).all()

    # gte operator

    def test_gte_filter(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).order_by(Booking.number_of_heads).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 4)
        self.assertEqual(filtered_query[1].number_of_heads, 5)

    def test_gte_filter_string_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "4"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 4)
        self.assertEqual(filtered_query[1].number_of_heads, 5)

    def test_gte_filter_none_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gte")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.OperatorArgumentError):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": None}).all()

    def test_gte_filter_invalid_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="gte")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": "four"}).all()

    # lt operator

    def test_lt_filter(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).order_by(Booking.number_of_heads).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 3)

    def test_lt_filter_string_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lt")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "4"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 3)

    def test_lt_filter_none_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lt")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.OperatorArgumentError):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": None}).all()

    def test_lt_filter_invalid_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lt")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": "four"}).all()

    # lte operator

    def test_lte_filter(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).order_by(Booking.number_of_heads).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 4)

    def test_lte_filter_string_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lte")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "4"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 4)

    def test_lte_filter_none_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lte")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.OperatorArgumentError):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": None}).all()

    def test_lte_filter_invalid_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.IntegerField(Booking.number_of_heads, operator="lte")

        query = self.session.query(Booking)
        with self.assertRaises(exceptions.FieldValidationException):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": "four"}).all()
