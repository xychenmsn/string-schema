# Simple Schema

A simple, LLM-friendly schema definition library for Python that converts intuitive string syntax into structured data schemas.

## 🎯 What Simple Schema Does

Simple Schema takes human-readable text descriptions and converts them into structured schemas for data validation, extraction, and API documentation. Perfect for LLM data extraction, API development, and configuration validation.

**Input:** Human-readable string syntax
**Output:** JSON Schema, Pydantic models, or OpenAPI specifications

## 🚀 Core Functions & Use Cases

### 📝 Schema Definition Functions

| Function                  | Input         | Output               | Use Case                        |
| ------------------------- | ------------- | -------------------- | ------------------------------- |
| `parse_string_schema()`   | String syntax | JSON Schema dict     | LLM data extraction, validation |
| `simple_schema()`         | Field objects | JSON Schema dict     | Programmatic schema building    |
| `to_json_schema()`        | Field objects | Standard JSON Schema | API documentation, validation   |
| `create_pydantic_model()` | Field objects | Pydantic model class | Data validation, FastAPI        |
| `to_openapi_schema()`     | Field objects | OpenAPI schema dict  | API documentation               |

### 🎯 Key Scenarios

- **🤖 LLM Data Extraction**: Define extraction schemas that LLMs can easily follow
- **🔧 API Development**: Generate Pydantic models and OpenAPI docs from simple syntax
- **✅ Data Validation**: Create robust validation schemas with minimal code
- **📋 Configuration**: Define and validate application configuration schemas
- **🔄 Data Transformation**: Convert between different schema formats

## 📦 Installation

```bash
pip install simple-schema
```

Optional dependencies:

```bash
pip install pydantic  # For Pydantic model generation
```

## 🎓 Quick Examples

### 🌱 Simple Example - Basic User Data

```python
from simple_schema import parse_string_schema

# Define schema using intuitive string syntax
schema = parse_string_schema("""
name:string(min=1, max=100),
email:email,
age:int(0, 120)?,
active:bool
""")

# Result: JSON Schema dictionary ready for validation
print(schema)
# {
#   "type": "object",
#   "properties": {
#     "name": {"type": "string", "minLength": 1, "maxLength": 100},
#     "email": {"type": "string", "format": "email"},
#     "age": {"type": "integer", "minimum": 0, "maximum": 120},
#     "active": {"type": "boolean"}
#   },
#   "required": ["name", "email", "active"]
# }
```

### 🌳 Moderately Complex Example - Product Catalog

```python
# E-commerce product with arrays, enums, and nested objects
schema = parse_string_schema("""
{
    id:uuid,
    name:string(min=1, max=200),
    price:number(min=0),
    category:enum(electronics, clothing, books, home),
    tags:[string](max=10)?,
    inventory:{
        in_stock:bool,
        quantity:int(min=0)?
    },
    reviews:[{
        rating:int(1, 5),
        comment:text(max=500),
        verified:bool?
    }](max=50)?
}
""")

# Result: Complete JSON Schema with nested objects and arrays
# Ready for API validation, LLM extraction, or Pydantic model generation
```

> 📚 **For more examples and advanced syntax**, see our [detailed documentation](docs/string-syntax.md)

## 🔄 Output Formats & Results

### 📋 JSON Schema (Default Output)

```python
from simple_schema import parse_string_schema

# String syntax → JSON Schema dictionary
schema = parse_string_schema("name:string, email:email")

# Returns a standard JSON Schema dict:
# {
#   "type": "object",
#   "properties": {
#     "name": {"type": "string"},
#     "email": {"type": "string", "format": "email"}
#   },
#   "required": ["name", "email"]
# }
```

### 🐍 Pydantic Models (Python Classes)

```python
from simple_schema import SimpleField, simple_schema
from simple_schema.integrations.pydantic import create_pydantic_model

# Define fields
fields = {
    'name': SimpleField('string', min_length=1, max_length=100),
    'email': SimpleField('string', format_hint='email')
}

# Create Pydantic model class
UserModel = create_pydantic_model('User', fields)

# Use the model for validation
user = UserModel(name="John Doe", email="john@example.com")
print(user.json())  # {"name": "John Doe", "email": "john@example.com"}
```

### 🌐 OpenAPI Schemas (API Documentation)

```python
from simple_schema.integrations.openapi import to_openapi_schema

# Convert to OpenAPI 3.0 format
openapi_schema = to_openapi_schema(fields, title="User Schema")

# Returns OpenAPI-compatible schema dict for API documentation
```

### 📦 Built-in Presets (Ready-to-use Schemas)

```python
from simple_schema import user_schema, product_schema, contact_schema

# Get pre-built JSON Schema dictionaries
user = user_schema(include_email=True, include_phone=True)
product = product_schema(include_price=True, include_description=True)
contact = contact_schema(include_company=True)
```

## 🎨 String Syntax Reference

### Basic Types

- `string`, `int`, `number`, `bool` → Basic data types
- `email`, `url`, `datetime`, `date`, `uuid`, `phone` → Special validated types

### Field Modifiers

- `field_name:type` → Required field
- `field_name:type?` → Optional field
- `field_name:type(constraints)` → Field with validation

### Common Patterns

- `string(min=1, max=100)` → Length constraints
- `int(0, 120)` → Range constraints
- `[string]` → Simple arrays
- `[{name:string, email:email}]` → Object arrays
- `status:enum(active, inactive)` → Enum values
- `id:string|uuid` → Union types

> 📖 **Complete syntax guide**: See [docs/string-syntax.md](docs/string-syntax.md) for full reference

## ✅ Validation

```python
from simple_schema.parsing import validate_string_schema

# Validate your schema syntax
result = validate_string_schema("name:string, email:email, age:int?")

print(f"Valid: {result['valid']}")
print(f"Features used: {result['features_used']}")
```

## 🏗️ Common Use Cases

### 🤖 LLM Data Extraction

```python
# Define what data to extract
schema = parse_string_schema("""
{
    company_name: string,
    employees: [{name: string, email: email, role: string}],
    founded_year: int?,
    website: url?
}
""")
# Use schema in LLM prompts for structured data extraction
```

### 🔧 FastAPI Development

```python
from simple_schema.integrations.pydantic import create_pydantic_model

# Generate Pydantic models for FastAPI
UserModel = create_pydantic_model('User', fields)

# Use in FastAPI endpoints
@app.post("/users/")
async def create_user(user: UserModel):
    return user
```

### 📋 Configuration Validation

```python
# Validate app configuration
config_schema = parse_string_schema("""
{
    database: {host: string, port: int(1, 65535)},
    debug_mode: bool,
    features: [string]?
}
""")
```

## 📚 Documentation

- **[Getting Started](docs/getting-started.md)** - Quick start guide and installation
- **[String Syntax Guide](docs/string-syntax.md)** - Complete syntax reference
- **[API Reference](docs/api-reference.md)** - Full API documentation
- **[Examples](docs/examples.md)** - Practical examples and patterns

## 🧪 Testing

The library includes comprehensive tests covering all functionality:

```bash
# Run tests (requires pytest)
pip install pytest
pytest tests/

# Results: 66 tests passed, 3 skipped (Pydantic tests when not installed)
```

## 🤝 Contributing

Contributions are welcome! The codebase is well-organized and documented:

```
simple_schema/
├── core/          # Core functionality (fields, builders, validators)
├── parsing/       # String parsing and syntax
├── integrations/  # Pydantic, JSON Schema, OpenAPI
└── examples/      # Built-in schemas and recipes
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Simple Schema** - Making data validation simple, intuitive, and LLM-friendly! 🚀
