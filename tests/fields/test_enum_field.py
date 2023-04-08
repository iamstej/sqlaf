import enum

from sqlaf import exceptions, fields, filters
from tests.base import FilterTestCase
from tests.implementation.factories import BookingFactory
from tests.implementation.models import Booking


class NumberOfHeads(enum.IntEnum):

    three = 3
    four = 4
    five = 5


class Name(enum.Enum):

    michael = "michael"
    jim = "jim"
    dwight = "dwight"


class IntegerFieldTestCase(FilterTestCase):
    def setUp(self):
        super().setUp()
        BookingFactory(name="michael", number_of_heads=3)
        BookingFactory(name="jim", number_of_heads=4)
        BookingFactory(name="dwight", number_of_heads=5)

    # eq operator

    def test_eq_filter_int_enum(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(Booking.number_of_heads, NumberOfHeads)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 4)

    def test_eq_filter_string_enum(self):
        class BookingFilter(filters.Filter):
            name = fields.EnumField(Booking.name, Name)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "michael"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, "michael")

    def test_eq_filter_default_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(Booking.number_of_heads, NumberOfHeads, default=NumberOfHeads.four)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, 4)

    def test_eq_filter_int_enum_none(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(Booking.number_of_heads, NumberOfHeads)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": None}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 4)
        self.assertEqual(filtered_query[2].number_of_heads, 5)

    def test_eq_filter_null_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(Booking.number_of_heads, NumberOfHeads, null_values=["null"])

        BookingFactory(number_of_heads=None)
        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "null"}).all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].number_of_heads, None)

    # ~eq operator

    def test_not_eq_filter_int_enum(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(Booking.number_of_heads, NumberOfHeads, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": 4}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 5)

    def test_not_eq_filter_string_enum(self):
        class BookingFilter(filters.Filter):
            name = fields.EnumField(Booking.name, Name, operator="~eq")

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"name": "michael"}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].name, "jim")
        self.assertEqual(filtered_query[1].name, "dwight")

    def test_not_eq_filter_default_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(
                Booking.number_of_heads,
                NumberOfHeads,
                operator="~eq",
                default=NumberOfHeads.four.value,
            )

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({}).all()
        self.assertEqual(len(filtered_query), 2)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 5)

    def test_not_eq_filter_null_value(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(
                Booking.number_of_heads,
                NumberOfHeads,
                operator="~eq",
                null_values=["null"],
            )

        BookingFactory(number_of_heads=None)
        query = self.session.query(Booking)
        filtered_query = BookingFilter(query).filter({"number_of_heads": "null"}).all()
        self.assertEqual(len(filtered_query), 3)

    # exceptions

    def test_invalid_int_enum_option(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(Booking.number_of_heads, NumberOfHeads)

        query = self.session.query(Booking)

        with self.assertRaises(exceptions.FieldInstantiationException):
            BookingFilter(query, raise_exceptions=True).filter({"number_of_heads": 6}).all()

    def test_invalid_int_enum_option_ignore_exceptions(self):
        class BookingFilter(filters.Filter):
            number_of_heads = fields.EnumField(Booking.number_of_heads, NumberOfHeads)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query, raise_exceptions=False).filter({"number_of_heads": 6}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].number_of_heads, 3)
        self.assertEqual(filtered_query[1].number_of_heads, 4)
        self.assertEqual(filtered_query[2].number_of_heads, 5)

    def test_invalid_str_enum_option(self):
        class BookingFilter(filters.Filter):
            name = fields.EnumField(Booking.name, Name)

        query = self.session.query(Booking)

        with self.assertRaises(exceptions.FieldInstantiationException):
            BookingFilter(query, raise_exceptions=True).filter({"name": "pam"}).all()

    def test_invalid_string_enum_option_ignore_exceptions(self):
        class BookingFilter(filters.Filter):
            name = fields.EnumField(Booking.name, Name)

        query = self.session.query(Booking)
        filtered_query = BookingFilter(query, raise_exceptions=False).filter({"name": "pam"}).all()
        self.assertEqual(len(filtered_query), 3)
        self.assertEqual(filtered_query[0].name, "michael")
        self.assertEqual(filtered_query[1].name, "jim")
        self.assertEqual(filtered_query[2].name, "dwight")
