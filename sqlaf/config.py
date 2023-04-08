from typing import Callable, Dict

from sqlaf import operators

FILTER_OPERATORS: Dict[str, Callable] = {
    "eq": operators.eq,
    "ieq": operators.ieq,
    "~eq": operators.xeq,
    "~ieq": operators.xieq,
    "gt": operators.gt,
    "gte": operators.gte,
    "lt": operators.lt,
    "lte": operators.lte,
    "~contains": operators.xcontains,
    "contains": operators.contains,
    "icontains": operators.icontains,
}
