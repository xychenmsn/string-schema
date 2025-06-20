# Simple Schema

A simple, LLM-friendly schema definition library for Python that makes data extraction and validation intuitive and reliable.

## 🎯 Status: Production Ready

✅ **All tests passing** (66/66 tests pass)
✅ **Critical bugs fixed** (array parsing now works correctly)
✅ **Complete feature set** (all enhanced syntax working)
✅ **Comprehensive documentation** (getting started, API reference, examples)
✅ **Clean architecture** (modular, extensible design)

## 🚀 Key Features

- **🔤 Intuitive String Syntax**: Define schemas using human-readable text
- **🤖 LLM-Optimized**: Designed specifically for Large Language Model data extraction
- **📋 Multiple Output Formats**: Generate JSON Schema, Pydantic models, OpenAPI specs
- **✅ Rich Validation**: Comprehensive validation with detailed error reporting
- **🎨 Special Types**: Built-in support for email, URL, datetime, UUID, phone, etc.
- **📊 Array Support**: Simple arrays `[string]` and complex object arrays `[{name, email}]`
- **🔀 Union Types**: Flexible types like `string|int` or `string|null`
- **📝 Enum Support**: Constrained values with `enum(active, inactive, pending)`
- **⚙️ Smart Constraints**: Length, range, and size constraints with intuitive syntax
- **📦 Built-in Presets**: Common schemas for users, products, contacts, etc.

## 📦 Installation

```bash
pip install simple-schema
```

Optional dependencies:

```bash
pip install pydantic  # For Pydantic model generation
```

## 🎓 Examples: From Simple to Complex

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

### 9. 🏛️ Complex Nested Structures

```python
# Real-world e-commerce product
schema = parse_string_schema("""
{
    id:uuid,
    name:string(min=1, max=200),
    price:number(min=0),
    category:enum(electronics, clothing, books, home, sports),
    description:text(max=2000)?,
    images:[url](max=10)?,
    tags:[string](max=20)?,
    inventory:{
        in_stock:bool,
        quantity:int(min=0)?,
        warehouse:string?
    }?,
    reviews:[{
        rating:int(1, 5),
        comment:text(max=1000),
        reviewer:string(max=100),
        verified:bool?,
        date:date
    }](max=100)?
}
""")
```

### 10. 🌐 Enterprise-Level Schema

```python
# Complete user management system
schema = parse_string_schema("""
[{
    id:string|uuid,
    profile:{
        username:string(min=3, max=30),
        email:email,
        first_name:string(min=1, max=50),
        last_name:string(min=1, max=50),
        phone:phone?,
        avatar:url?,
        bio:text(max=500)?,
        social:{
            linkedin:url?,
            twitter:url?,
            github:url?,
            website:url?
        }?
    },
    account:{
        status:enum(active, inactive, suspended, pending_verification),
        role:enum(admin, moderator, user, guest),
        permissions:[string]?,
        email_verified:bool,
        phone_verified:bool?,
        two_factor_enabled:bool,
        last_login:datetime?,
        login_count:int(min=0),
        failed_login_attempts:int(min=0, max=10)
    },
    preferences:{
        theme:choice(light, dark, auto),
        language:string(min=2, max=5),
        timezone:string?,
        notifications:{
            email:bool,
            sms:bool?,
            push:bool,
            marketing:bool?
        }
    }?,
    metadata:{
        created_at:datetime,
        updated_at:datetime,
        created_by:string?,
        last_modified_by:string?,
        tags:[string](max=10)?,
        notes:text?
    }
}](min=1, max=1000)
""")
```

## 🔧 Alternative Usage Methods

### Method 1: SimpleField Objects (Programmatic)

```python
from simple_schema import SimpleField, simple_schema

# Define fields programmatically
fields = {
    'name': SimpleField('string', 'Full name', min_length=1, max_length=100),
    'age': SimpleField('integer', 'Age in years', min_val=0, max_val=120),
    'email': SimpleField('string', 'Email address', format_hint='email'),
    'status': SimpleField('string', 'User status', choices=['active', 'inactive'])
}

# Generate JSON Schema
schema = simple_schema(fields)
```

### Method 2: String Syntax (Recommended for LLMs)

```python
from simple_schema import parse_string_schema

# Define schema using intuitive string syntax
schema = parse_string_schema("""
{
    name: string(min=1, max=100),
    age: int(0, 120),
    email: email,
    status: enum(active, inactive)
}
""")
```

### Method 3: Built-in Presets

```python
from simple_schema import user_schema, product_schema, contact_schema

# Use pre-built schemas
user = user_schema(include_email=True, include_phone=True, include_profile=True)
product = product_schema(include_price=True, include_description=True)
contact = contact_schema(include_company=True, include_social=True)
```

## 🔄 Output Formats

### JSON Schema

```python
from simple_schema.integrations.json_schema import to_json_schema

# Convert to standard JSON Schema
json_schema = to_json_schema(fields, title="User Schema", description="User data validation")
```

### Pydantic Models

```python
from simple_schema.integrations.pydantic import create_pydantic_model

# Generate Pydantic model (requires: pip install pydantic)
UserModel = create_pydantic_model('User', fields)

# Use the model
user = UserModel(name="John Doe", age=30, email="john@example.com", status="active")
print(user.json())
```

### OpenAPI Schemas

```python
from simple_schema.integrations.openapi import to_openapi_schema

# Convert to OpenAPI 3.0 format
openapi_schema = to_openapi_schema(fields, title="User Schema")
```

## 🎨 Complete Syntax Reference

### Basic Types

- `string`, `str`, `text` → String type
- `int`, `integer` → Integer type
- `number`, `float` → Number type
- `bool`, `boolean` → Boolean type

### Special Types (with automatic format validation)

- `email` → Email validation
- `url`, `uri` → URL validation
- `datetime` → DateTime parsing
- `date` → Date parsing
- `uuid` → UUID validation
- `phone` → Phone formatting

### Field Modifiers

- `field_name:type` → Required field
- `field_name:type?` → Optional field
- `field_name:type(constraints)` → Field with constraints

### Constraints

- `string(min=1, max=100)` → String length constraints
- `int(0, 120)` → Integer range (positional)
- `number(min=0, max=100)` → Number range (named)
- `text(max=500)` → Text with max length

### Arrays

- `[string]` → Simple array
- `[email](min=1, max=3)` → Constrained array
- `[{name:string, email:email}]` → Object array
- `tags:array(string, max=5)` → Alternative syntax

### Enums

- `status:enum(active, inactive, pending)` → Enum values
- `priority:choice(low, medium, high)` → Alternative syntax
- `category:select(tech, business, personal)` → Alternative syntax

### Union Types

- `id:string|uuid` → String or UUID
- `value:string|int|float` → Multiple types
- `response:string|null` → Nullable field

## ✅ Validation and Error Handling

```python
from simple_schema.parsing import validate_string_schema
from simple_schema.core.validators import validate_schema

# Validate string schema with detailed feedback
result = validate_string_schema("""
[{
    name:string(min=1, max=100),
    emails:[email](min=1, max=3),
    role:enum(admin, user, guest)
}](min=1, max=20)
""")

print(f"Valid: {result['valid']}")
print(f"Features used: {result['features_used']}")
print(f"Field count: {len(result['parsed_fields'])}")

if result['warnings']:
    for warning in result['warnings']:
        print(f"⚠️ {warning}")
```

## 🏗️ Real-World Use Cases

### 1. LLM Data Extraction

```python
# Perfect for LLM prompts
extraction_schema = parse_string_schema("""
Extract the following information:
{
    company_name: string(min=1, max=200),
    employees: [{
        name: string(min=1, max=100),
        email: email,
        role: enum(ceo, cto, developer, designer, manager),
        experience_years: int(0, 50)?
    }](min=1, max=100),
    founded_year: int(1800, 2024)?,
    website: url?,
    technologies: [string](max=20)?
}
""")
```

### 2. API Request/Response Validation

```python
# API endpoint schema
api_schema = parse_string_schema("""
{
    request: {
        user_id: uuid,
        action: enum(create, update, delete, view),
        data: object?,
        timestamp: datetime
    },
    response: {
        success: bool,
        data: object|array|null,
        message: string?,
        errors: [{
            field: string,
            code: string,
            message: string
        }]?
    }
}
""")
```

### 3. Configuration Validation

```python
# Application configuration
config_schema = parse_string_schema("""
{
    database: {
        host: string,
        port: int(1, 65535),
        name: string(min=1, max=64),
        ssl: bool?
    },
    redis: {
        url: url,
        timeout: int(1, 300)?
    }?,
    features: {
        auth_enabled: bool,
        rate_limiting: bool,
        debug_mode: bool?
    }
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
