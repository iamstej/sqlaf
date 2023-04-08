from datetime import date, datetime
from enum import Enum, IntEnum
from typing import Any, Callable, List, Union


from sqlaf.exceptions import FieldInstantiationException, FieldValidationException
from sqlaf.fields import Field


class CharField(Field):

    allowed_operators = ["eq", "~eq", "ieq", "~ieq", "contains", "icontains"]

    def transform(self, value: Any) -> str:
        value = super().transform(value)

        try:
            return str(value)
        except (TypeError, ValueError):
            raise FieldValidationException(f"{value} is not of type string.")


class IntegerField(Field):

    allowed_operators = ["eq", "~eq", "gt", "gte", "lt", "lte"]

    def transform(self, value: Any) -> int:
        value = super().transform(value)

        if value is None:
            return value

        try:
            return int(value)
        except (TypeError, ValueError):
            raise FieldValidationException(f"{value} is not of type integer.")


class EnumField(Field):

    allowed_operators = ["eq", "~eq"]

    def __init__(
        self,
        source,
        enum_class: Enum,
        operator: Union[str, Callable] = "eq",
        default: Any = None,
        null_values: List[Any] = [],
    ):
        super().__init__(source, operator=operator, default=default, null_values=null_values)

        if not enum_class:
            raise FieldInstantiationException("`enum_class` cannot be None.")

        self.enum_class = enum_class

    def transform(self, value: Any) -> Enum:
        value = super().transform(value)

        try:
            if issubclass(self.enum_class, IntEnum):
                value = int(value)

            return self.enum_class(value).value
        except (ValueError, TypeError):
            raise FieldInstantiationException(f"{value} is not of type {self.enum_class.__name__}.")


class BooleanField(Field):

    allowed_operators = ["eq"]
    truthy = [True, 1]
    falsy = [False, 0]

    def __init__(
        self,
        source,
        operator: Union[str, Callable] = "eq",
        truthy: List = [],
        falsy: List = [],
        default: Any = None,
        null_values: List[Any] = [],
    ):
        super().__init__(source, operator=operator, default=default, null_values=null_values)

        if truthy and isinstance(truthy, list):
            self.truthy = truthy

        if falsy and isinstance(falsy, list):
            self.falsy = falsy

    def transform(self, value: Any) -> bool:
        value = super().transform(value)

        if value in self.truthy:
            return True

        if value in self.falsy:
            return False

        raise FieldValidationException(f"{value} is an invalid truthy/falsy option.")


class ArrayField(Field):

    allowed_operators = ["contains", "~contains"]

    def __init__(
        self,
        source,
        operator: Union[str, Callable] = "contains",
        default: Any = None,
        null_values: List[Any] = [],
    ):
        super().__init__(source, operator=operator, default=default, null_values=null_values)

    def transform(self, value: Any):
        value = super().transform(value)

        if isinstance(value, list):
            return value

        if not isinstance(value, str):
            return None

        return value.split(",")


class DateField(Field):

    allowed_operators = ["eq", "~eq", "gt", "gte", "lt", "lte"]
    format = "%Y-%m-%d"

    def __init__(
        self,
        source,
        operator: Union[str, Callable] = "eq",
        format: str = None,
        default: Any = None,
        null_values: List[Any] = [],
    ):
        super().__init__(source, operator=operator, default=default, null_values=null_values)

        if format:
            self.format = format

    def _parse_datetime_string(self, value: Any):
        return datetime.strptime(value, self.format).date()

    def transform(self, value: Any):
        if isinstance(value, date):
            return value

        try:
            return self._parse_datetime_string(value)
        except ValueError:
            raise FieldValidationException(f"{value} does not conform to {self.format}")


class DateTimeField(DateField):

    datetime_type = datetime
    format = "%Y-%m-%dT%H:%M:%S%z"

    def _parse_datetime_string(self, value: Any):
        return datetime.strptime(value, self.format)


class TimeField(DateField):

    format = "%H:%M:%S%z"

    def _parse_datetime_string(self, value: Any):
        if "%z" in self.format or "%Z" in self.format:
            return datetime.strptime(value, self.format).timetz()

        return datetime.strptime(value, self.format).time()
