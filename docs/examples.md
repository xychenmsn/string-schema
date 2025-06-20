# Examples

Practical examples and use cases for Simple Schema.

## Basic Examples

### Simple User Schema

```python
from simple_schema import SimpleField, simple_schema

# Define user fields
fields = {
    'name': SimpleField('string', 'Full name', min_length=1, max_length=100),
    'email': SimpleField('string', 'Email address', format_hint='email'),
    'age': SimpleField('integer', 'Age', min_val=0, max_val=120, required=False)
}

# Generate schema
user_schema = simple_schema(fields)
```

### String-Based Definition

```python
from simple_schema import parse_string_schema

# Same schema using string syntax
schema_str = """
{
    name: string(min=1, max=100),
    email: email,
    age: int(0, 120)?
}
"""

user_schema = parse_string_schema(schema_str)
```

## Array Examples

### Simple Arrays

```python
# Array of strings
tags_schema = parse_string_schema("[string]")

# Array with constraints
limited_tags = parse_string_schema("[string](max=5)")

# Array of emails
emails_schema = parse_string_schema("[email](min=1, max=3)")
```

### Object Arrays

```python
# Array of user objects
users_schema = parse_string_schema("""
[{
    name: string(min=1, max=100),
    email: email,
    role: enum(admin, user, guest)
}](min=1, max=50)
""")
```

## Special Types

### Format Hints

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

schema = parse_string_schema(schema_str)
```

### Enum Types

```python
# Status field with specific choices
status_schema = parse_string_schema("""
{
    status: enum(active, inactive, pending, suspended),
    priority: choice(low, medium, high, urgent),
    category: select(tech, business, personal)
}
""")
```

### Union Types

```python
# Flexible ID field
flexible_schema = parse_string_schema("""
{
    id: string|uuid,
    value: string|int|float,
    response: string|null
}
""")
```

## Real-World Examples

### E-commerce Product

```python
product_schema = parse_string_schema("""
{
    id: uuid,
    name: string(min=1, max=200),
    description: text(max=2000)?,
    price: number(min=0),
    currency: enum(USD, EUR, GBP, JPY),
    category: enum(electronics, clothing, books, home, sports),
    brand: string(max=100)?,
    sku: string(max=50),
    in_stock: bool,
    stock_quantity: int(min=0)?,
    weight: number(min=0)?,
    dimensions: string?,
    images: [url](max=10)?,
    tags: [string](max=20)?,
    reviews: [{
        rating: int(1, 5),
        comment: text(max=1000),
        reviewer_name: string(max=100),
        verified: bool?,
        date: date
    }](max=100)?,
    created_at: datetime,
    updated_at: datetime
}
""")
```

### User Management System

```python
user_management_schema = parse_string_schema("""
[{
    id: string|uuid,
    profile: {
        username: string(min=3, max=30),
        email: email,
        first_name: string(min=1, max=50),
        last_name: string(min=1, max=50),
        phone: phone?,
        avatar: url?,
        bio: text(max=500)?
    },
    account: {
        status: enum(active, inactive, suspended, pending_verification),
        role: enum(admin, moderator, user, guest),
        permissions: [string]?,
        email_verified: bool,
        phone_verified: bool?,
        two_factor_enabled: bool,
        last_login: datetime?,
        login_count: int(min=0)
    },
    preferences: {
        theme: choice(light, dark, auto),
        language: string(min=2, max=5),
        timezone: string?,
        notifications: {
            email: bool,
            sms: bool?,
            push: bool
        }
    }?,
    metadata: {
        created_at: datetime,
        updated_at: datetime,
        created_by: string?,
        notes: text?
    }
}](min=1, max=1000)
""")
```

### API Response Structure

```python
api_response_schema = parse_string_schema("""
{
    success: bool,
    data: object|array|null,
    message: string?,
    errors: [{
        field: string?,
        code: string,
        message: string,
        details: object?
    }]?,
    meta: {
        timestamp: datetime,
        request_id: uuid,
        version: string,
        rate_limit: {
            limit: int,
            remaining: int,
            reset: datetime
        }?
    }?,
    pagination: {
        page: int(min=1),
        per_page: int(min=1, max=100),
        total: int(min=0),
        total_pages: int(min=0),
        has_next: bool,
        has_prev: bool
    }?
}
""")
```

### Blog/CMS System

```python
blog_schema = parse_string_schema("""
{
    post: {
        id: uuid,
        title: string(min=1, max=200),
        slug: string(min=1, max=200),
        content: text(min=10),
        excerpt: text(max=500)?,
        status: enum(draft, published, archived, scheduled),
        published_at: datetime?,
        scheduled_for: datetime?
    },
    author: {
        id: uuid,
        name: string(min=1, max=100),
        email: email,
        bio: text(max=1000)?,
        avatar: url?,
        social: {
            twitter: url?,
            linkedin: url?,
            website: url?
        }?
    },
    content: {
        category: {
            id: uuid,
            name: string(min=1, max=100),
            slug: string(min=1, max=100),
            description: text?
        },
        tags: [{
            id: uuid,
            name: string(min=1, max=50),
            slug: string(min=1, max=50)
        }](max=20)?,
        featured_image: {
            url: url,
            alt_text: string(max=200)?,
            caption: string(max=500)?
        }?,
        seo: {
            meta_title: string(max=60)?,
            meta_description: string(max=160)?,
            keywords: [string](max=10)?
        }?
    },
    engagement: {
        view_count: int(min=0),
        like_count: int(min=0),
        comment_count: int(min=0),
        share_count: int(min=0),
        comments: [{
            id: uuid,
            author_name: string(min=1, max=100),
            author_email: email,
            content: text(min=1, max=2000),
            status: enum(pending, approved, rejected, spam),
            created_at: datetime,
            parent_id: uuid?
        }](max=1000)?
    }
}
""")
```

## Integration Examples

### Pydantic Model Generation

```python
from simple_schema import SimpleField
from simple_schema.integrations.pydantic import create_pydantic_model

# Define fields
fields = {
    'name': SimpleField('string', 'Full name', min_length=1, max_length=100),
    'email': SimpleField('string', 'Email', format_hint='email'),
    'age': SimpleField('integer', 'Age', min_val=0, max_val=120, required=False)
}

# Create Pydantic model
UserModel = create_pydantic_model('User', fields)

# Use the model
user = UserModel(name="John Doe", email="john@example.com", age=30)
print(user.json())
```

### JSON Schema Export

```python
from simple_schema.integrations.json_schema import to_json_schema

# Convert to JSON Schema
json_schema = to_json_schema(
    fields,
    title="User Schema",
    description="Schema for user data validation"
)

# Add examples
from simple_schema.integrations.json_schema import to_json_schema_with_examples

examples = [
    {"name": "John Doe", "email": "john@example.com", "age": 30},
    {"name": "Jane Smith", "email": "jane@example.com"}
]

schema_with_examples = to_json_schema_with_examples(fields, examples)
```

### OpenAPI Integration

```python
from simple_schema.integrations.openapi import (
    to_openapi_schema,
    create_openapi_component,
    create_openapi_request_body,
    create_openapi_response
)

# Create OpenAPI schema
openapi_schema = to_openapi_schema(fields, title="User")

# Create component
component = create_openapi_component("User", fields)

# Create request body
request_body = create_openapi_request_body(fields, "User creation data")

# Create response
response = create_openapi_response(fields, "User data")
```

## Built-in Schema Examples

### Using Preset Schemas

```python
from simple_schema import user_schema, product_schema, contact_schema

# Basic user schema
basic_user = user_schema()

# Full user schema with all options
full_user = user_schema(
    include_email=True,
    include_phone=True,
    include_profile=True,
    include_preferences=True
)

# Product schema
product = product_schema(
    include_price=True,
    include_description=True,
    include_images=True,
    include_reviews=True
)

# Contact schema
contact = contact_schema(
    include_company=True,
    include_address=True,
    include_social=True
)
```

### Recipe Schemas

```python
from simple_schema.examples.recipes import (
    create_ecommerce_product_schema,
    create_blog_post_schema,
    create_pagination_schema,
    create_api_response_schema
)

# E-commerce product
ecommerce_product = create_ecommerce_product_schema()

# Blog post
blog_post = create_blog_post_schema()

# Paginated response
user_fields = {'name': SimpleField('string'), 'email': SimpleField('string')}
paginated_users = create_pagination_schema(user_fields)

# API response wrapper
api_response = create_api_response_schema(user_fields)
```

## Validation Examples

### String Schema Validation

```python
from simple_schema.parsing import validate_string_schema

schema_str = """
[{
    name: string(min=1, max=100),
    emails: [email](min=1, max=3),
    role: enum(admin, user, guest),
    profile: {
        bio: text?,
        social: [url]?
    }?,
    active: bool,
    last_login: datetime?
}](min=1, max=20)
"""

result = validate_string_schema(schema_str)

print(f"Valid: {result['valid']}")
print(f"Features used: {result['features_used']}")
print(f"Field count: {len(result['parsed_fields'])}")

if result['warnings']:
    print("Warnings:")
    for warning in result['warnings']:
        print(f"  - {warning}")
```

### Schema Compliance

```python
from simple_schema.integrations.json_schema import validate_json_schema_compliance

schema = simple_schema(fields)
compliance = validate_json_schema_compliance(schema)

print(f"Compliant: {compliance['valid']}")
print(f"Compliance level: {compliance['compliance_level']}")
```

## Performance Examples

### Large Schema Optimization

```python
from simple_schema.parsing.optimizer import optimize_string_schema, suggest_improvements

# Complex schema
complex_schema = """
[{
    user: {
        id: uuid,
        profile: {
            name: string(min=1, max=100),
            email: email,
            phone: phone?,
            address: {
                street: string?,
                city: string?,
                country: string?
            }?
        },
        preferences: {
            theme: enum(light, dark),
            notifications: bool,
            language: string?
        }?,
        metadata: {
            created: datetime,
            updated: datetime,
            tags: [string]?
        }
    }
}](min=1, max=1000)
"""

# Optimize schema
optimized = optimize_string_schema(complex_schema)

# Get suggestions
suggestions = suggest_improvements(complex_schema)
for suggestion in suggestions:
    print(f"💡 {suggestion}")
```

These examples demonstrate the flexibility and power of Simple Schema for defining data structures that work well with both traditional validation and LLM-based data extraction.
