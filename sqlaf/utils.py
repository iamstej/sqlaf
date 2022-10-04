import inspect
from typing import Any, Dict
from urllib.parse import parse_qs


def get_public_attrs(instance: Any):
    """Get the public attributes of a class that are not routing attributes.

    Args:
        instance (Any): The instance or class to get the attributes for.

    Returns:
        List[String]: List of attribute names.
    """
    attributes = inspect.getmembers(instance, lambda a: not (inspect.isroutine(a)))
    return [a[0] for a in attributes if not (a[0].startswith("_") or a[0].startswith("__") or a[0].endswith("__"))]


def parse_query_string(query_string: str) -> Dict:
    """Parse a querystring and return it in a dictionary format.

    Args:
        query_string (str): Query string

    Returns:
        Dict: Query string represented in dictionary format.
    """
    if not query_string:
        return {}

    if query_string[0] == "?":
        query_string = query_string[1:]

    return {k: v[0] for k, v in parse_qs(query_string).items()}
