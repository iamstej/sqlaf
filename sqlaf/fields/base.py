from typing import Any

from sqlalchemy.sql.elements import BinaryExpression

from sqlaf import config
from sqlaf.fields import IField
from sqlaf.exceptions import FieldInstantiationException, FieldValidationException


class Field(IField):

    allowed_operators = []

    def __init__(self, source, operator: str = "eq", default: Any = None):
        if self.allowed_operators and operator not in self.allowed_operators:
            raise FieldInstantiationException(f"{operator} not supported for {self.__class__}")

        self.default = default
        self.source = source
        self.operator = operator

    def transform(self, value: Any) -> Any:
        """Function which allows for manipulation of the value being passed in i.e. if the data needs to be in a
            certain format for a field type the manipulation would be performed here.

        Args:
            value (Any): The value to manipulate.

        Returns:
            Any: The manipulated value
        """
        return value

    def get_filters(self, value: Any) -> BinaryExpression:
        """Using the field source, operator and value, create a FilterHandler instance and perform the filtering which
            will return the SQLAlchemy filters that will be required to be performed.

        Args:
            value (Any): The value to filter with.

        Returns:
            BinaryExpression: An SQLAlchemy BinaryExpression filter.
        """
        operator_func = config.FILTER_OPERATORS.get(self.operator.lower())

        if not operator_func:
            raise NotImplementedError(f"{self.operator} is not a supported operator.")

        return operator_func(self.source, value)

    def filter(self, value: Any) -> BinaryExpression:
        """Facade function for transforming the data and then performing the filtering.

        Args:
            value (Any): The value to filter with.

        Raises:
            e: FieldValidationException

        Returns:
            BinaryExpression: An SQLAlchemy BinaryExpression filter.
        """
        try:
            value = self.transform(value)
        except FieldValidationException as e:
            raise e

        return self.get_filters(value)
