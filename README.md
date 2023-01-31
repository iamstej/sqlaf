# sqlaf

[![PyPI pyversions](https://img.shields.io/pypi/pyversions/sqlaf.svg)](https://pypi.python.org/pypi/sqlaf/)
[![pypi](https://img.shields.io/pypi/v/sqlaf)](https://pypi.org/project/sqlaf/)

sqlaf is a library for transforming query parameters into SQLAlchemy filters in a structured and organised manner

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sqlaf.

```bash
pip install sqlaf
```

## Usage

### Creating a Filter

A filter can be created by inheriting from the sqlaf `Filter` class and building up the fields to filter the query with.
The class variable name used will be the key that will be extracted from the query parameters for that given filter.

```python
from sqlaf import filters, fields

class TeamFilter(filters.Filter):

    founded_date = fields.DateField(Team.founded_date, operator="gte")
    name = fields.CharField(Team.name, operator="icontains")
    size = fields.IntegerField(Team.size, operator="eq")
```

### Using a Filter

A filter class can be used in the following ways:

#### Query parameter string with "?"
```python
query = session.query(Team)
query = TeamFilter(query).filter("?name=A&size=2")
```

#### Query parameter string without "?"

```python
query = session.query(Team)
query = TeamFilter(query).filter("name=A&size=2")
```

#### Query parameter string with dictionary

```python
query = session.query(Team)
query = TeamFilter(query).filter({"name": "A", "size": 2})
```


### Available Fields

The following fields are available out the box (in the usage below, the parameters are the defaults set for each field):


| Field         | Usage                                                                                        | Available Operators                                              | 
|---------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------|
| CharField     | `CharField(Model.field, operator="eq", default=None)`                                        | `"eq"`, `"~eq"`, `"ieq"`, `"~ieq"`, `"contains"`, `"icontains"`  | 
| IntegerField  | `IntegerField(Model.field, operator="eq", default=None)`                                     | `"eq"`, `"~eq"`, `"gt"`, `"gte"`, `"lt"`, `"lte"`                |
| EnumField     | `EnumField(Model.field, enum_class=Enum operator="eq", default=None)`                        | `"eq"`, `"~eq"`                                                  |
| BooleanField  | `BooleanField(Model.field, operator="eq", truthy=[True, 1], falsy=[False, 0], default=None)` | `"eq"`                                                           |
| ArrayField    | `ArrayField(Model.field, operator="eq", default=None)`                                       | `"contains"`, `"~contains"`                                      |
| DateField     | `DateField(Model.field, format=""%Y-%m-%d", operator="eq", default=None)`                    | `"eq", "~eq", "gt", "gte", "lt", "lte"`                          |
| DateTimeField | `DateTimeField(Model.field, format="%Y-%m-%dT%H:%M:%S%z", operator="eq", default=None)`      | `"eq", "~eq", "gt", "gte", "lt", "lte"`                                                                 |
| TimeField     | `TimeField(Model.field, format="%H:%M:%S%z", operator="eq", default=None)`                   | `"eq", "~eq", "gt", "gte", "lt", "lte"`                                                                 |


### Available Operators

The following operators are available out of the box.

| Key       | Name                      | Description                                                        | 
|-----------|---------------------------|--------------------------------------------------------------------|
| `eq`        | Case-sensitive equals     | The value is equal to the column value.                            | 
| `ieq`       | Case-insensitive equals   | The value is equal to the column value regardless of case.         |
| `~eq`       | Case-sensitive not equal  | The value is not equal to the column value.                        |
| `~ieq`      | Case-sensitive not equal  | The value is not equal to the column value regardless of case.     |
| `gt`        | Greater than              | The value is greater than the column value.                        |
| `gte`       | Greater than or equal     | The value is greater than or equal to the column value.            |
| `lt`        | Less than                 | The value is less than the column value.                           |
| `lte`       | Less than or equal        | The value is less than or equal to the column value.               |
| `contains`  | Contains                  | The value is contained within the column value.                    |
| `~contains` | Does not contain          | The value is not contained within the column value.                |
| `icontains` | Case-insensitive contains | The value is contained within the column value regardless of case. |

### Custom Operators

To extend the above operators, you can create custom operators:

```python
from sqlaf import filters, fields


def custom_operator(source, value):
    return column == value


class TeamFilter(filters.Filter):
    
    team_size = fields.IntegerField(Team.team_size, operator=custom_operator)
```

### Custom Filtering

If filtering is needed that is not covered by the sqlaf framework, add custom filtering
by using the `post_filter` function:

```python
from sqlaf import filters, fields

class TeamFilter(filters.Filter):
    
    size = fields.IntegerField(Team.size, operator="eq")
    
    def post_filter(self, data, filters):
        if name := data.get("name"):
            filters.append(Team.name == name)

        return filters
```

## Todo

- [ ] Prepare roadmap.
- [ ] Write better documentation.
- [ ] Establish contribution and release processes.

## Contributing

For the meantime, I will be maintaining the project myself while getting v1.0 prepared. After v1.0 is released, the guidelines and processes for contribution will be documented here :) 

## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)