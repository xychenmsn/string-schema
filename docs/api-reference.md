# API Reference

Complete API documentation for Simple Schema.

## Core API

### SimpleField

The core field definition class.

```python
class SimpleField:
    def __init__(self, field_type: str, description: str = "", required: bool = True,
                 default: Any = None, min_val: Optional[Union[int, float]] = None,
                 max_val: Optional[Union[int, float]] = None, min_length: Optional[int] = None,
                 max_length: Optional[int] = None, choices: Optional[List[Any]] = None,
                 min_items: Optional[int] = None, max_items: Optional[int] = None,
                 format_hint: Optional[str] = None, union_types: Optional[List[str]] = None)
```

**Parameters:**
- `field_type`: The base type (string, integer, number, boolean)
- `description`: Human-readable description
- `required`: Whether the field is required (default: True)
- `default`: Default value if field is not provided
- `min_val`, `max_val`: Numeric constraints
- `min_length`, `max_length`: String length constraints
- `choices`: List of allowed values (enum)
- `min_items`, `max_items`: Array size constraints
- `format_hint`: Special format (email, url, datetime, etc.)
- `union_types`: List of types for union fields

**Methods:**
- `to_dict()`: Convert to dictionary representation
- `from_dict(data)`: Create from dictionary (class method)

### Schema Builders

#### simple_schema()

```python
def simple_schema(fields: Dict[str, Union[str, SimpleField]]) -> Dict[str, Any]
```

Generate JSON Schema from field definitions.

**Example:**
```python
fields = {
    'name': SimpleField('string', 'Full name'),
    'age': SimpleField('integer', 'Age', min_val=0)
}
schema = simple_schema(fields)
```

#### list_of_objects_schema()

```python
def list_of_objects_schema(item_fields: Dict[str, Union[str, SimpleField]],
                          description: str = "List of objects",
                          min_items: Optional[int] = None,
                          max_items: Optional[int] = None) -> Dict[str, Any]
```

Generate schema for array of objects.

#### simple_array_schema()

```python
def simple_array_schema(item_type: str = 'string', description: str = 'Array of items',
                       min_items: Optional[int] = None, max_items: Optional[int] = None,
                       format_hint: Optional[str] = None) -> Dict[str, Any]
```

Generate schema for simple arrays.

#### quick_pydantic_model()

```python
def quick_pydantic_model(name: str, fields: Dict[str, Union[str, SimpleField]]) -> Type[BaseModel]
```

Create Pydantic model from field definitions.

## String Parsing API

### parse_string_schema()

```python
def parse_string_schema(schema_str: str, is_list: bool = False) -> Dict[str, Any]
```

Parse string-based schema definition into JSON Schema.

**Example:**
```python
schema = parse_string_schema("name:string, age:int, email:email")
```

### validate_string_schema()

```python
def validate_string_schema(schema_str: str) -> Dict[str, Any]
```

Validate string schema and return detailed feedback.

**Returns:**
```python
{
    'valid': bool,
    'errors': List[str],
    'warnings': List[str],
    'parsed_fields': Dict[str, Any],
    'generated_schema': Dict[str, Any],
    'features_used': List[str]
}
```

### get_string_schema_examples()

```python
def get_string_schema_examples() -> Dict[str, Dict[str, Any]]
```

Get all built-in string schema examples.

## Validation API

### validate_schema()

```python
def validate_schema(schema: Dict[str, Any]) -> Dict[str, Any]
```

Validate JSON Schema compliance.

### validate_simple_field()

```python
def validate_simple_field(field: SimpleField) -> Dict[str, Any]
```

Validate SimpleField instance.

## Built-in Schemas

### User Schemas

```python
def user_schema(include_email: bool = True, include_phone: bool = False, 
               include_profile: bool = False, include_preferences: bool = False) -> Dict[str, Any]

def user_list_schema(**kwargs) -> Dict[str, Any]
```

### Product Schemas

```python
def product_schema(include_price: bool = True, include_description: bool = True,
                  include_images: bool = False, include_reviews: bool = False) -> Dict[str, Any]

def product_list_schema(**kwargs) -> Dict[str, Any]
```

### Contact Schemas

```python
def contact_schema(include_company: bool = False, include_address: bool = False,
                  include_social: bool = False) -> Dict[str, Any]

def contact_list_schema(**kwargs) -> Dict[str, Any]
```

### Article Schemas

```python
def article_schema(include_summary: bool = True, include_tags: bool = False,
                  include_metadata: bool = False) -> Dict[str, Any]

def article_list_schema(**kwargs) -> Dict[str, Any]
```

### Event Schemas

```python
def event_schema(include_location: bool = True, include_attendees: bool = False) -> Dict[str, Any]

def event_list_schema(**kwargs) -> Dict[str, Any]
```

## Integration APIs

### Pydantic Integration

```python
from simple_schema.integrations.pydantic import (
    create_pydantic_model,
    create_pydantic_from_json_schema,
    validate_pydantic_compatibility,
    generate_pydantic_code
)
```

#### create_pydantic_model()

```python
def create_pydantic_model(name: str, fields: Dict[str, Union[str, SimpleField]], 
                         base_class: Type[BaseModel] = BaseModel) -> Type[BaseModel]
```

### JSON Schema Integration

```python
from simple_schema.integrations.json_schema import (
    to_json_schema,
    to_json_schema_with_examples,
    validate_json_schema_compliance,
    optimize_json_schema
)
```

#### to_json_schema()

```python
def to_json_schema(fields: Dict[str, Union[str, SimpleField]], 
                  title: str = "Generated Schema",
                  description: str = "",
                  schema_version: str = "https://json-schema.org/draft/2020-12/schema") -> Dict[str, Any]
```

### OpenAPI Integration

```python
from simple_schema.integrations.openapi import (
    to_openapi_schema,
    create_openapi_component,
    create_openapi_request_body,
    create_openapi_response,
    validate_openapi_compatibility
)
```

#### to_openapi_schema()

```python
def to_openapi_schema(fields: Dict[str, Union[str, SimpleField]],
                     title: str = "Generated Schema",
                     description: str = "",
                     version: str = "1.0.0") -> Dict[str, Any]
```

## Recipe APIs

### Common Patterns

```python
from simple_schema.examples.recipes import (
    create_list_schema,
    create_nested_schema,
    create_enum_schema,
    create_union_schema,
    create_pagination_schema,
    create_api_response_schema,
    create_ecommerce_product_schema,
    create_blog_post_schema
)
```

#### create_list_schema()

```python
def create_list_schema(item_fields: Dict[str, Union[str, SimpleField]],
                      description: str = "List of items",
                      min_items: Optional[int] = None,
                      max_items: Optional[int] = None) -> Dict[str, Any]
```

#### create_pagination_schema()

```python
def create_pagination_schema(item_fields: Dict[str, Union[str, SimpleField]],
                           include_metadata: bool = True) -> Dict[str, Any]
```

#### create_api_response_schema()

```python
def create_api_response_schema(data_fields: Dict[str, Union[str, SimpleField]],
                             include_status: bool = True,
                             include_metadata: bool = False) -> Dict[str, Any]
```

## Utility Functions

### Field Creation Helpers

```python
from simple_schema.core.fields import (
    create_enhanced_field,
    create_special_type_field,
    create_enum_field,
    create_union_field
)
```

### Optimization

```python
from simple_schema.parsing.optimizer import (
    optimize_string_schema,
    suggest_improvements,
    simplify_schema,
    infer_types
)
```

## Error Handling

Simple Schema uses standard Python exceptions:

- `ValueError`: Invalid field definitions or schema structures
- `TypeError`: Incorrect parameter types
- `KeyError`: Missing required fields or properties

## Type Hints

Simple Schema is fully typed. Import types:

```python
from typing import Dict, List, Any, Optional, Union, Type
from pydantic import BaseModel
```

## Constants

### Supported Field Types

```python
BASIC_TYPES = ['string', 'integer', 'number', 'boolean']
SPECIAL_TYPES = ['email', 'url', 'uri', 'datetime', 'date', 'uuid', 'phone']
```

### Format Mappings

```python
FORMAT_MAPPING = {
    'email': 'email',
    'url': 'uri',
    'uri': 'uri',
    'datetime': 'date-time',
    'date': 'date',
    'uuid': 'uuid'
}
```
