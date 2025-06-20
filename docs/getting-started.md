# Getting Started with Simple Schema

Simple Schema is a Python library that makes it easy to define data schemas using intuitive syntax that works well with Large Language Models (LLMs) for data extraction and validation.

## 🎯 Status: Production Ready

✅ **All tests passing** (66/66 tests pass)
✅ **Critical bugs fixed** (array parsing now works correctly)
✅ **Complete feature set** (all enhanced syntax working)
✅ **Comprehensive documentation** (getting started, API reference, examples)
✅ **Clean architecture** (modular, extensible design)

## Installation

### Basic Installation

Install Simple Schema using pip:

```bash
pip install simple-schema
```

### With Optional Dependencies

```bash
pip install pydantic  # For Pydantic model generation
```

### Development Installation

For contributing to the project:

```bash
git clone <repository-url>
cd simple-schema
pip install -e .
pip install pytest  # For running tests
```

## Your First Schema

Let's start with a simple example:

```python
from simple_schema import SimpleField, simple_schema

# Define fields using SimpleField objects
fields = {
    'name': SimpleField('string', 'Full name', min_length=1, max_length=100),
    'age': SimpleField('integer', 'Age in years', min_val=0, max_val=120),
    'email': SimpleField('string', 'Email address', format_hint='email')
}

# Generate JSON Schema
schema = simple_schema(fields)
print(schema)
```

This creates a JSON Schema that looks like:

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Full name",
      "minLength": 1,
      "maxLength": 100
    },
    "age": {
      "type": "integer",
      "description": "Age in years",
      "minimum": 0,
      "maximum": 120
    },
    "email": {
      "type": "string",
      "description": "Email address",
      "format": "email"
    }
  },
  "required": ["name", "age", "email"]
}
```

## String-Based Schema Definition

For even simpler syntax, you can define schemas using strings:

```python
from simple_schema import parse_string_schema

# Define schema using string syntax
schema_str = """
{
    name: string(min=1, max=100),
    age: int(0, 120),
    email: email,
    status: enum(active, inactive, pending)
}
"""

schema = parse_string_schema(schema_str)
```

## Built-in Schema Presets

Simple Schema includes common schema patterns:

```python
from simple_schema import user_schema, product_schema

# Use built-in user schema
user = user_schema(include_email=True, include_phone=True)

# Use built-in product schema
product = product_schema(include_price=True, include_description=True)
```

## Working with Arrays

Define arrays of simple types or objects:

```python
# Simple arrays
tags_schema = parse_string_schema("[string]")
scores_schema = parse_string_schema("[int]")

# Arrays with constraints
limited_tags = parse_string_schema("[string](max=5)")

# Arrays of objects
users_schema = parse_string_schema("[{name:string, email:email}]")
```

## Special Types and Format Hints

Simple Schema supports special types that provide hints for better data extraction:

```python
schema_str = """
{
    email: email,           # Email validation
    website: url,           # URL validation
    created: datetime,      # DateTime parsing
    birthday: date,         # Date parsing
    id: uuid,              # UUID validation
    phone: phone           # Phone formatting
}
"""
```

## Enum and Union Types

Define constrained values and flexible types:

```python
# Enum types for specific choices
status_schema = parse_string_schema("status: enum(active, inactive, pending)")

# Union types for flexible data
id_schema = parse_string_schema("id: string|uuid")
value_schema = parse_string_schema("value: string|int|null")
```

## Integration with Pydantic

Convert schemas to Pydantic models:

```python
from simple_schema import quick_pydantic_model

fields = {
    'name': SimpleField('string', 'Full name'),
    'age': SimpleField('integer', 'Age', min_val=0)
}

# Create Pydantic model
UserModel = quick_pydantic_model('User', fields)

# Use the model
user = UserModel(name="John Doe", age=30)
print(user.name)  # "John Doe"
```

## Validation

Validate your schemas:

```python
from simple_schema.parsing import validate_string_schema
from simple_schema.core.validators import validate_schema

# Validate string schema
result = validate_string_schema("name:string, age:int, email:email")
print(f"Valid: {result['valid']}")
print(f"Features used: {result['features_used']}")

# Validate JSON schema
json_schema = simple_schema(fields)
validation = validate_schema(json_schema)
print(f"Valid: {validation['valid']}")
```

## 🎓 Progressive Examples: From Simple to Complex

### 1. 🌱 Extremely Simple - Single Field

```python
from simple_schema import parse_string_schema

# Just a name field
schema = parse_string_schema("name:string")
```

### 2. 🌿 Basic - Multiple Fields

```python
# Basic user information
schema = parse_string_schema("name:string, age:int, active:bool")
```

### 3. 🌳 Adding Constraints

```python
# With validation constraints
schema = parse_string_schema("""
name:string(min=1, max=100),
age:int(0, 120),
email:email
""")
```

### 4. 🌲 Optional Fields

```python
# Some fields are optional (marked with ?)
schema = parse_string_schema("""
name:string(min=1, max=100),
email:email,
phone:phone?,
bio:text(max=500)?
""")
```

### 5. 🏞️ Arrays

```python
# Simple arrays
tags_schema = parse_string_schema("[string]")
scores_schema = parse_string_schema("[int]")

# Arrays with constraints
limited_tags = parse_string_schema("[string](max=5)")
email_list = parse_string_schema("[email](min=1, max=3)")
```

### 6. 🏔️ Enums and Choices

```python
# Predefined choices
schema = parse_string_schema("""
name:string,
status:enum(active, inactive, pending),
priority:choice(low, medium, high, urgent),
category:select(tech, business, personal)
""")
```

### 7. 🌌 Union Types

```python
# Flexible field types
schema = parse_string_schema("""
id:string|uuid,
value:string|int|float,
response:string|null
""")
```

### 8. 🏗️ Object Arrays

```python
# Arrays of structured objects
schema = parse_string_schema("""
[{
    name:string(min=1, max=100),
    email:email,
    role:enum(admin, user, guest)
}](min=1, max=50)
""")
```

## Next Steps

Now that you understand the basics:

1. **Explore [String Syntax](string-syntax.md)** - Complete syntax reference with all features
2. **Check [Examples](examples.md)** - Real-world use cases and patterns
3. **Review [API Reference](api-reference.md)** - Complete API documentation
4. **See [Advanced Usage](advanced-usage.md)** - Complex patterns and optimization

## Common Patterns

### User Registration Form

```python
registration_schema = parse_string_schema("""
{
    username: string(min=3, max=20),
    email: email,
    password: string(min=8),
    age: int(13, 120)?,
    terms_accepted: bool
}
""")
```

### API Response

```python
api_response_schema = parse_string_schema("""
{
    success: bool,
    data: object,
    message: string?,
    timestamp: datetime
}
""")
```

### Product Catalog

```python
product_schema = parse_string_schema("""
{
    id: uuid,
    name: string(min=1, max=200),
    price: number(min=0),
    category: enum(electronics, clothing, books, home),
    tags: [string](max=10)?,
    in_stock: bool
}
""")
```

These examples show how Simple Schema makes it easy to define clear, validated data structures that work well with both traditional APIs and LLM-based data extraction.
