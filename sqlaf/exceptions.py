class SQLAlchemyFiltersBaseException(Exception):
    """All exceptions specific to sqlalchemy-filters will derive from this base exception."""

    pass


class QueryParamaterDataException(SQLAlchemyFiltersBaseException):
    """The query parameter data was in the incorrect format."""

    pass


class FieldInstantiationException(SQLAlchemyFiltersBaseException):
    """Failed to instantiate the field due to it being configured incorrectly."""

    pass


class FieldValidationException(SQLAlchemyFiltersBaseException):
    """The data being passed in to the field does not match the field type and it is not possible to transform the data
    into the type expected by the field.
    """

    pass


class OperatorArgumentError(SQLAlchemyFiltersBaseException):
    """The filter operator logic could not be performed on the source and value that was passed into the operator."""

    pass
