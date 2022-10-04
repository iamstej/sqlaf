from abc import ABC, abstractmethod
from typing import Any

import sqlalchemy
from sqlalchemy import Column, func
from sqlalchemy.sql.elements import BinaryExpression

from sqlaf.exceptions import OperatorArgumentError


def eq(source: Column, value: Any) -> BinaryExpression:
    return source == value


def ieq(source: Column, value: Any) -> BinaryExpression:
    if not isinstance(value, str):
        raise OperatorArgumentError("case insensitive operator can only be used with string values")

    return func.lower(source) == value.lower()


def xeq(source: Column, value: Any) -> BinaryExpression:
    return source != value


def xieq(source: Column, value: Any) -> BinaryExpression:
    if not isinstance(value, str):
        raise OperatorArgumentError("case insensitive operator can only be used with string values")

    return func.lower(source) != value.lower()


def gt(source: Column, value: Any) -> BinaryExpression:
    if value is None:
        raise OperatorArgumentError("gt operator cannot be used with None")

    return source > value


def gte(source: Column, value: Any) -> BinaryExpression:
    if value is None:
        raise OperatorArgumentError("gte operator cannot be used with None")

    return source >= value


def lt(source: Column, value: Any) -> BinaryExpression:
    if value is None:
        raise OperatorArgumentError("lt operator cannot be used with None")

    return source < value


def lte(source: Column, value: Any) -> BinaryExpression:
    if value is None:
        raise OperatorArgumentError("lte operator cannot be used with None")

    return source <= value


def contains(source: Column, value: Any) -> BinaryExpression:
    return source.contains(value, autoescape=isinstance(value, str))


def xcontains(source: Column, value: Any) -> BinaryExpression:
    return sqlalchemy.not_(source.contains(value, autoescape=isinstance(value, str)))


def icontains(source: Column, value: Any) -> BinaryExpression:
    if not isinstance(value, str):
        raise OperatorArgumentError("icontains can only be using with string values")

    return func.lower(source).contains(value.lower(), autoescape=True)
