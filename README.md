# Simple Schema

A simple, LLM-friendly schema definition library for Python that converts intuitive string syntax into structured data schemas.

## 🎯 What Simple Schema Does

Simple Schema takes human-readable text descriptions and converts them into structured schemas for data validation, extraction, and API documentation. Perfect for LLM data extraction, API development, and configuration validation.

**Input:** Human-readable string syntax
**Output:** JSON Schema, Pydantic models, or OpenAPI specifications

## 🚀 Core Functions & Use Cases

### 📝 Core Functions (Clear & Descriptive Names)

| Function                    | Input            | Output               | Use Case                             |
| --------------------------- | ---------------- | -------------------- | ------------------------------------ |
| `string_to_json_schema()`   | String syntax    | JSON Schema dict     | Main conversion function             |
| `string_to_pydantic()`      | String syntax    | Pydantic model class | **Direct path** - string to Pydantic |
| `string_to_pydantic_code()` | String syntax    | Python code string   | **Code generation** - for templates  |
| `string_to_openapi()`       | String syntax    | OpenAPI schema dict  | **Direct path** - string to OpenAPI  |
| `validate_string_syntax()`  | String syntax    | Validation result    | Check syntax and get feedback        |
| `json_schema_to_pydantic()` | JSON Schema dict | Pydantic model class | When you already have JSON Schema    |
| `json_schema_to_openapi()`  | JSON Schema dict | OpenAPI schema dict  | When you already have JSON Schema    |
| Built-in presets            | Configuration    | JSON Schema dict     | Ready-to-use common schemas          |

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
from simple_schema import string_to_json_schema

# Define schema using intuitive string syntax
schema = string_to_json_schema("""
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
schema = string_to_json_schema("""
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
from simple_schema import string_to_json_schema

# String syntax → JSON Schema dictionary
schema = string_to_json_schema("name:string, email:email")

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
from simple_schema import string_to_pydantic

# Direct conversion: String syntax → Pydantic model
UserModel = string_to_pydantic('User', "name:string(min=1, max=100), email:email, age:int?")

# Use the model for validation
user = UserModel(name="John Doe", email="john@example.com")
print(user.model_dump_json())  # {"name": "John Doe", "email": "john@example.com"}
```

### 🔧 Code Generation (For Templates & Tools)

```python
from simple_schema import string_to_pydantic_code

# Generate Pydantic model code as a string
code = string_to_pydantic_code('User', "name:string(min=1, max=100), email:email, age:int?")
print(code)

# Output:
# from pydantic import BaseModel, Field
# from typing import Optional, Union
#
# class User(BaseModel):
#     name: str = Field(min_length=1, max_length=100)
#     email: str = Field(format='email')
#     age: Optional[int] = None

# Perfect for code generators, templates, or saving to files
with open('models.py', 'w') as f:
    f.write(code)
```

### 🌐 OpenAPI Schemas (API Documentation)

```python
from simple_schema.integrations.openapi import string_to_openapi

# Direct conversion: String syntax → OpenAPI schema
openapi_schema = string_to_openapi("name:string, email:email", title="User Schema")

# Alternative: Two-step process if you need the JSON Schema too
from simple_schema import string_to_json_schema
from simple_schema.integrations.json_schema import json_schema_to_openapi

json_schema = string_to_json_schema("name:string, email:email")
openapi_schema = json_schema_to_openapi(json_schema)
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
from simple_schema import validate_string_syntax

# Validate your schema syntax
result = validate_string_syntax("name:string, email:email, age:int?")

print(f"Valid: {result['valid']}")
print(f"Features used: {result['features_used']}")
print(f"Field count: {len(result['parsed_fields'])}")

if result['warnings']:
    for warning in result['warnings']:
        print(f"⚠️ {warning}")
```

## 🏗️ Common Use Cases

### 🤖 LLM Data Extraction

```python
from simple_schema import string_to_json_schema

# Define what data to extract
schema = string_to_json_schema("""
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
from simple_schema import string_to_pydantic

# Direct conversion: String → Pydantic model
UserModel = string_to_pydantic('User', "name:string, email:email, age:int?")

# Use in FastAPI endpoints
@app.post("/users/")
async def create_user(user: UserModel):
    return user
```

### 🏗️ Code Generation & Templates

```python
from simple_schema import string_to_pydantic_code

# Generate multiple model files
schemas = {
    'User': "name:string, email:email, role:enum(admin, user)",
    'Product': "name:string, price:number(min=0), category:string",
    'Order': "user_id:uuid, products:[uuid], total:number(min=0)"
}

for model_name, schema_str in schemas.items():
    code = string_to_pydantic_code(model_name, schema_str)
    with open(f'models/{model_name.lower()}.py', 'w') as f:
        f.write(code)
    print(f"Generated {model_name} model")
```

### 📋 Configuration Validation

```python
from simple_schema import string_to_json_schema

# Validate app configuration
config_schema = string_to_json_schema("""
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
