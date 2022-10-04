from typing import Any, Dict, List

from sqlalchemy.orm.query import Query
from sqlalchemy.sql.elements import BinaryExpression

from sqlaf.exceptions import QueryParamaterDataException, SQLAlchemyFiltersBaseException
from sqlaf.fields import Field
from sqlaf.filters import IFilter
from sqlaf.utils import get_public_attrs, parse_query_string


class Filter(IFilter):
    def _get_filter_attributes(self) -> List[str]:
        """Get the public class attributes from the `Filter` class.

        Returns:
            List[str]: A list of public class attributes.
        """
        return get_public_attrs(self)

    def _transform_data(self, data: Any) -> Dict:
        """Transfer the data into a dictionary if it's not already in dictionary format.

        Args:
            data (Any): Query parameters in string or dictionary format.

        Returns:
            Dict: Query parameters in dictionary format.
        """
        if isinstance(data, dict):
            return data

        if isinstance(data, str):
            return parse_query_string(data)

        raise QueryParamaterDataException("data must be in dictionary or string format.")

    def filter(self, data: Any) -> Query:
        """Perform the filtering dependent on the `Filter` class config.

        Args:
            data (Any): The data to perform the filtering with.

        Returns:
            Query: Returns the original query with the filters generated from the filtering mechanism appended.
        """
        data = self._transform_data(data)
        filters: List[BinaryExpression] = []

        for key in self._get_filter_attributes():
            field = getattr(self, key)

            if not field or not isinstance(field, Field) or (key not in data and field.default is None):
                continue

            try:
                filter_expression = field.filter(value=data.get(key, field.default))
                filters.append(filter_expression)
            except SQLAlchemyFiltersBaseException as e:
                if self._raise_exceptions:
                    raise e

        self.post_filter(data, filters)
        return self._query.filter(*filters)

    def post_filter(self, data: Dict, filters: List):
        """If there is any filtering that needs performing manually post filtering, this function can be
            overridden and the filtering performed here.

            e.g.

            ```
            def post_filter(self, data: Dict, filters: List):
                name = data.get('name')

                if name:
                    filters.append(Model.name == name)

                return filters
            ```

        Args:
            data (Dict): Dictionary containing filter key values pairs.
            filters (List): The filters created post filter.

        Returns:
            List: An array of filters.
        """
        return filters
