from typing import Any, Dict, List, Optional, Union, Type
from pydantic import BaseModel, Field, create_model
import logging

logger = logging.getLogger(__name__)

class SimpleField:
    """Enhanced SimpleField with support for all new features"""
    def __init__(self, field_type: str, description: str = "", required: bool = True,
                 default: Any = None, min_val: Optional[Union[int, float]] = None,
                 max_val: Optional[Union[int, float]] = None, min_length: Optional[int] = None,
                 max_length: Optional[int] = None, choices: Optional[List[Any]] = None,
                 min_items: Optional[int] = None, max_items: Optional[int] = None,
                 format_hint: Optional[str] = None, union_types: Optional[List[str]] = None):
        self.field_type = field_type
        self.description = description
        self.required = required
        self.default = default
        self.min_val = min_val
        self.max_val = max_val
        self.min_length = min_length
        self.max_length = max_length
        self.choices = choices
        self.min_items = min_items
        self.max_items = max_items
        self.format_hint = format_hint
        self.union_types = union_types or []

def simple_schema(fields: Dict[str, Union[str, SimpleField]]) -> Dict[str, Any]:
    """Generate JSON Schema from simple field definitions with enhanced support"""
    properties = {}
    required = []
    
    for field_name, field_def in fields.items():
        if isinstance(field_def, str):
            field_def = SimpleField(field_def)
        
        prop_schema = _simple_field_to_json_schema(field_def)
        properties[field_name] = prop_schema
        
        if field_def.required:
            required.append(field_name)
    
    schema = {
        "type": "object",
        "properties": properties
    }
    if required:
        schema["required"] = required
    
    return schema

def _simple_field_to_json_schema(field: SimpleField) -> Dict[str, Any]:
    """Convert SimpleField to JSON Schema property with enhanced features"""
    # Handle union types first
    if field.union_types and len(field.union_types) > 1:
        union_schemas = []
        for union_type in field.union_types:
            if union_type == "null":
                union_schemas.append({"type": "null"})
            else:
                union_schemas.append({"type": union_type})
        prop = {"anyOf": union_schemas}
        
        # Add description to the union
        if field.description:
            prop["description"] = field.description
        
        return prop
    
    # Regular single type
    prop = {"type": field.field_type}
    
    if field.description:
        prop["description"] = field.description
    if field.default is not None:
        prop["default"] = field.default
    
    # Handle enum/choices
    if field.choices:
        prop["enum"] = field.choices
    
    # Add format hints for special types
    if field.format_hint:
        if field.format_hint == "email":
            prop["format"] = "email"
        elif field.format_hint in ["url", "uri"]:
            prop["format"] = "uri"
        elif field.format_hint == "datetime":
            prop["format"] = "date-time"
        elif field.format_hint == "date":
            prop["format"] = "date"
        elif field.format_hint == "uuid":
            prop["format"] = "uuid"
        # Note: phone doesn't have a standard JSON Schema format
    
    # Numeric constraints
    if field.field_type in ["integer", "number"]:
        if field.min_val is not None:
            prop["minimum"] = field.min_val
        if field.max_val is not None:
            prop["maximum"] = field.max_val
    
    # String constraints
    if field.field_type == "string":
        if field.min_length is not None:
            prop["minLength"] = field.min_length
        if field.max_length is not None:
            prop["maxLength"] = field.max_length
    
    # Array constraints (for when this field itself is an array)
    if field.min_items is not None:
        prop["minItems"] = field.min_items
    if field.max_items is not None:
        prop["maxItems"] = field.max_items
    
    return prop

def list_of_objects_schema(item_fields: Dict[str, Union[str, SimpleField]],
                          description: str = "List of objects",
                          min_items: Optional[int] = None,
                          max_items: Optional[int] = None) -> Dict[str, Any]:
    """Generate schema for array of objects with enhanced constraints"""
    item_schema = simple_schema(item_fields)
    
    array_schema = {
        "type": "array",
        "description": description,
        "items": item_schema
    }
    
    # Add array size constraints
    if min_items is not None:
        array_schema["minItems"] = min_items
    if max_items is not None:
        array_schema["maxItems"] = max_items
    
    return array_schema

def simple_array_schema(item_type: str = 'string', description: str = 'Array of items',
                       min_items: Optional[int] = None, max_items: Optional[int] = None,
                       format_hint: Optional[str] = None) -> Dict[str, Any]:
    """Generate schema for simple arrays like [string], [int], [email]"""
    items_schema = {"type": item_type}
    
    # Add format for special types
    if format_hint:
        if format_hint == "email":
            items_schema["format"] = "email"
        elif format_hint in ["url", "uri"]:
            items_schema["format"] = "uri"
        elif format_hint == "datetime":
            items_schema["format"] = "date-time"
        elif format_hint == "date":
            items_schema["format"] = "date"
        elif format_hint == "uuid":
            items_schema["format"] = "uuid"
    
    array_schema = {
        "type": "array",
        "description": description,
        "items": items_schema
    }
    
    # Add array size constraints
    if min_items is not None:
        array_schema["minItems"] = min_items
    if max_items is not None:
        array_schema["maxItems"] = max_items
    
    return array_schema

def quick_pydantic_model(name: str, fields: Dict[str, Union[str, SimpleField]]) -> Type[BaseModel]:
    """Create Pydantic model from simple field definitions"""
    pydantic_fields = {}
    
    for field_name, field_def in fields.items():
        if isinstance(field_def, str):
            field_def = SimpleField(field_def)
        
        python_type, field_info = _simple_field_to_pydantic(field_def)
        pydantic_fields[field_name] = (python_type, field_info)
    
    return create_model(name, **pydantic_fields)

def _simple_field_to_pydantic(field: SimpleField) -> tuple:
    """Convert SimpleField to Pydantic field specification"""
    # Type mapping
    type_mapping = {
        'string': str,
        'integer': int,
        'number': float,
        'boolean': bool
    }
    
    python_type = type_mapping.get(field.field_type, str)
    
    # Handle union types
    if field.union_types and len(field.union_types) > 1:
        from typing import Union as TypingUnion
        union_python_types = []
        for union_type in field.union_types:
            if union_type == "null":
                union_python_types.append(type(None))
            else:
                union_python_types.append(type_mapping.get(union_type, str))
        python_type = TypingUnion[tuple(union_python_types)]
    
    # Handle optional fields
    if not field.required:
        python_type = Optional[python_type]
    
    # Build Field arguments
    field_kwargs = {}
    
    if field.description:
        field_kwargs['description'] = field.description
    
    if field.default is not None:
        field_kwargs['default'] = field.default
    elif not field.required:
        field_kwargs['default'] = None
    
    # Numeric constraints
    if field.min_val is not None:
        field_kwargs['ge'] = field.min_val
    if field.max_val is not None:
        field_kwargs['le'] = field.max_val
    
    # String constraints
    if field.min_length is not None:
        field_kwargs['min_length'] = field.min_length
    if field.max_length is not None:
        field_kwargs['max_length'] = field.max_length
    
    return python_type, Field(**field_kwargs) if field_kwargs else Field()

# Enhanced built-in schemas
def user_schema(include_email: bool = True, include_phone: bool = False, 
               include_profile: bool = False, include_preferences: bool = False) -> Dict[str, Any]:
    """Generate enhanced user schema with special types"""
    fields = {
        'name': SimpleField('string', 'Full name', min_length=1, max_length=100),
        'age': SimpleField('integer', 'Age in years', min_val=13, max_val=120, required=False)
    }
    
    if include_email:
        fields['email'] = SimpleField('string', 'Email address', format_hint='email')
    
    if include_phone:
        fields['phone'] = SimpleField('string', 'Phone number', format_hint='phone', required=False)
    
    if include_profile:
        fields['bio'] = SimpleField('string', 'Biography', max_length=500, required=False)
        fields['avatar'] = SimpleField('string', 'Avatar URL', format_hint='url', required=False)
    
    if include_preferences:
        fields['theme'] = SimpleField('string', 'UI theme', choices=['light', 'dark'], required=False)
        fields['notifications'] = SimpleField('boolean', 'Email notifications enabled', required=False)
    
    return simple_schema(fields)

def product_schema(include_price: bool = True, include_description: bool = True,
                  include_images: bool = False, include_reviews: bool = False) -> Dict[str, Any]:
    """Generate enhanced product schema"""
    fields = {
        'name': SimpleField('string', 'Product name', min_length=1, max_length=200),
        'category': SimpleField('string', 'Product category', 
                               choices=['electronics', 'clothing', 'books', 'home', 'sports'])
    }
    
    if include_price:
        fields['price'] = SimpleField('number', 'Price', min_val=0)
    
    if include_description:
        fields['description'] = SimpleField('string', 'Product description', 
                                          max_length=1000, required=False)
    
    if include_images:
        # This would need to be handled as a nested array, which is complex
        # For now, we'll represent it as a simple field
        fields['image_urls'] = SimpleField('string', 'Comma-separated image URLs', required=False)
    
    if include_reviews:
        # Similarly, this would be a complex nested structure
        fields['avg_rating'] = SimpleField('number', 'Average rating', min_val=1.0, max_val=5.0, required=False)
        fields['review_count'] = SimpleField('integer', 'Number of reviews', min_val=0, required=False)
    
    return simple_schema(fields)

def contact_schema(include_company: bool = False, include_address: bool = False,
                  include_social: bool = False) -> Dict[str, Any]:
    """Generate enhanced contact schema"""
    fields = {
        'name': SimpleField('string', 'Contact name', min_length=1, max_length=100),
        'email': SimpleField('string', 'Email address', format_hint='email'),
        'phone': SimpleField('string', 'Phone number', format_hint='phone', required=False)
    }
    
    if include_company:
        fields['company'] = SimpleField('string', 'Company name', max_length=200, required=False)
        fields['job_title'] = SimpleField('string', 'Job title', max_length=100, required=False)
    
    if include_address:
        fields['address'] = SimpleField('string', 'Full address', max_length=500, required=False)
        fields['city'] = SimpleField('string', 'City', max_length=100, required=False)
        fields['country'] = SimpleField('string', 'Country', max_length=100, required=False)
    
    if include_social:
        fields['linkedin'] = SimpleField('string', 'LinkedIn URL', format_hint='url', required=False)
        fields['twitter'] = SimpleField('string', 'Twitter URL', format_hint='url', required=False)
        fields['website'] = SimpleField('string', 'Personal website', format_hint='url', required=False)
    
    return simple_schema(fields)

def article_schema(include_summary: bool = True, include_tags: bool = False,
                  include_metadata: bool = False) -> Dict[str, Any]:
    """Generate enhanced article schema"""
    fields = {
        'title': SimpleField('string', 'Article title', min_length=1, max_length=200),
        'content': SimpleField('string', 'Article content', min_length=10)
    }
    
    if include_summary:
        fields['summary'] = SimpleField('string', 'Brief summary', max_length=500, required=False)
    
    if include_tags:
        # Represented as comma-separated for simplicity
        fields['tags'] = SimpleField('string', 'Comma-separated tags', max_length=200, required=False)
    
    if include_metadata:
        fields['author'] = SimpleField('string', 'Author name', max_length=100, required=False)
        fields['published_date'] = SimpleField('string', 'Publication date', format_hint='date', required=False)
        fields['word_count'] = SimpleField('integer', 'Word count', min_val=0, required=False)
    
    return simple_schema(fields)

def event_schema(include_location: bool = True, include_attendees: bool = False) -> Dict[str, Any]:
    """Generate enhanced event schema"""
    fields = {
        'title': SimpleField('string', 'Event title', min_length=1, max_length=200),
        'date': SimpleField('string', 'Event date', format_hint='datetime'),
        'status': SimpleField('string', 'Event status', 
                             choices=['planned', 'active', 'completed', 'cancelled'])
    }
    
    if include_location:
        fields['venue'] = SimpleField('string', 'Venue name', max_length=200, required=False)
        fields['address'] = SimpleField('string', 'Event address', max_length=500, required=False)
        fields['is_online'] = SimpleField('boolean', 'Is online event', required=False)
        fields['meeting_url'] = SimpleField('string', 'Meeting URL', format_hint='url', required=False)
    
    if include_attendees:
        fields['max_attendees'] = SimpleField('integer', 'Maximum attendees', min_val=1, required=False)
        fields['current_attendees'] = SimpleField('integer', 'Current attendee count', min_val=0, required=False)
    
    return simple_schema(fields)

# List versions of schemas
def user_list_schema(**kwargs) -> Dict[str, Any]:
    """Generate schema for array of users"""
    user_fields = {}
    user_base = user_schema(**kwargs)
    
    # Convert properties to SimpleField definitions
    for field_name, field_schema in user_base['properties'].items():
        field_type = field_schema['type']
        required = field_name in user_base.get('required', [])
        
        simple_field = SimpleField(field_type, required=required)
        
        # Copy constraints
        if 'minimum' in field_schema:
            simple_field.min_val = field_schema['minimum']
        if 'maximum' in field_schema:
            simple_field.max_val = field_schema['maximum']
        if 'minLength' in field_schema:
            simple_field.min_length = field_schema['minLength']
        if 'maxLength' in field_schema:
            simple_field.max_length = field_schema['maxLength']
        if 'enum' in field_schema:
            simple_field.choices = field_schema['enum']
        if 'format' in field_schema:
            simple_field.format_hint = field_schema['format']
        
        user_fields[field_name] = simple_field
    
    return list_of_objects_schema(user_fields, "List of users")

def product_list_schema(**kwargs) -> Dict[str, Any]:
    """Generate schema for array of products"""
    return _convert_object_to_list_schema(product_schema(**kwargs), "List of products")

def contact_list_schema(**kwargs) -> Dict[str, Any]:
    """Generate schema for array of contacts"""
    return _convert_object_to_list_schema(contact_schema(**kwargs), "List of contacts")

def article_list_schema(**kwargs) -> Dict[str, Any]:
    """Generate schema for array of articles"""
    return _convert_object_to_list_schema(article_schema(**kwargs), "List of articles")

def event_list_schema(**kwargs) -> Dict[str, Any]:
    """Generate schema for array of events"""
    return _convert_object_to_list_schema(event_schema(**kwargs), "List of events")

def _convert_object_to_list_schema(object_schema: Dict[str, Any], description: str) -> Dict[str, Any]:
    """Helper function to convert object schema to list schema"""
    fields = {}
    
    # Convert properties to SimpleField definitions
    for field_name, field_schema in object_schema['properties'].items():
        field_type = field_schema['type']
        required = field_name in object_schema.get('required', [])
        
        simple_field = SimpleField(field_type, required=required)
        
        # Copy constraints
        if 'minimum' in field_schema:
            simple_field.min_val = field_schema['minimum']
        if 'maximum' in field_schema:
            simple_field.max_val = field_schema['maximum']
        if 'minLength' in field_schema:
            simple_field.min_length = field_schema['minLength']
        if 'maxLength' in field_schema:
            simple_field.max_length = field_schema['maxLength']
        if 'enum' in field_schema:
            simple_field.choices = field_schema['enum']
        if 'format' in field_schema:
            simple_field.format_hint = field_schema['format']
        if 'description' in field_schema:
            simple_field.description = field_schema['description']
        
        fields[field_name] = simple_field
    
    return list_of_objects_schema(fields, description)

# Enhanced utility schemas
def simple_list_schema(item_type: str = 'string', description: str = 'List of items',
                      min_items: Optional[int] = None, max_items: Optional[int] = None) -> Dict[str, Any]:
    """Generate schema for simple arrays with enhanced constraints"""
    return simple_array_schema(item_type, description, min_items, max_items)

def key_value_schema(description: str = 'Key-value pairs') -> Dict[str, Any]:
    """Generate schema for flexible key-value objects"""
    return {
        "type": "object",
        "description": description,
        "additionalProperties": {"type": "string"}
    }

def enum_schema(field_name: str, values: List[str], description: str = "") -> Dict[str, Any]:
    """Generate schema for a single enum field"""
    fields = {
        field_name: SimpleField('string', description, choices=values)
    }
    return simple_schema(fields)

def union_schema(field_name: str, types: List[str], description: str = "") -> Dict[str, Any]:
    """Generate schema for a single union field"""
    fields = {
        field_name: SimpleField('string', description, union_types=types)
    }
    return simple_schema(fields)

# Enhanced examples with all new features
ENHANCED_EXAMPLES = {
    "simple_user": {
        "description": "Basic user information with special types",
        "schema": user_schema(include_email=True, include_phone=True),
        "prompt_example": "Extract user: John Doe, 25 years old, john@example.com, phone +1-555-0123"
    },
    
    "product_with_enum": {
        "description": "Product with category enum",
        "schema": product_schema(include_price=True, include_description=True),
        "prompt_example": "Product: iPhone 14, $999, Electronics category, Latest smartphone with advanced features"
    },
    
    "contact_with_social": {
        "description": "Contact with social media links",
        "schema": contact_schema(include_company=True, include_social=True),
        "prompt_example": "Contact: Jane Smith, jane@company.org, works at TechCorp as Developer, LinkedIn: linkedin.com/in/janesmith"
    },
    
    "simple_string_array": {
        "description": "Simple array of strings (FIXED!)",
        "schema": simple_array_schema('string', 'List of tags', max_items=5),
        "prompt_example": "Tags: python, javascript, react, machine-learning, AI"
    },
    
    "email_array": {
        "description": "Array of email addresses",
        "schema": simple_array_schema('string', 'List of emails', min_items=1, max_items=3, format_hint='email'),
        "prompt_example": "Emails: john@example.com, jane@company.org, admin@website.com"
    },
    
    "user_list": {
        "description": "List of user objects",
        "schema": user_list_schema(include_email=True),
        "prompt_example": "Users: John Doe (25, john@example.com), Jane Smith (30, jane@company.org)"
    },
    
    "enum_status": {
        "description": "Simple enum field",
        "schema": enum_schema('status', ['active', 'inactive', 'pending'], 'User status'),
        "prompt_example": "Status: active"
    },
    
    "union_id": {
        "description": "Union type field",
        "schema": union_schema('id', ['string', 'integer'], 'Flexible ID field'),
        "prompt_example": "ID: abc123 or ID: 12345"
    }
}

def get_examples() -> Dict[str, Dict[str, Any]]:
    """Get all enhanced simple schema examples"""
    return ENHANCED_EXAMPLES.copy()

def print_examples():
    """Print all enhanced simple schema examples"""
    print("🔧 Enhanced Simple Schema Examples:")
    print("=" * 60)
    
    for name, example in ENHANCED_EXAMPLES.items():
        print(f"\n📋 {name.upper().replace('_', ' ')}")
        print(f"Description: {example['description']}")
        print(f"Prompt: {example['prompt_example']}")
        print(f"Schema Preview: {_schema_preview(example['schema'])}")
        print("-" * 40)

def _schema_preview(schema: Dict[str, Any]) -> str:
    """Generate a preview of the schema structure"""
    if schema.get('type') == 'object':
        properties = schema.get('properties', {})
        field_names = list(properties.keys())
        if len(field_names) <= 3:
            return f"Object with fields: {', '.join(field_names)}"
        else:
            return f"Object with {len(field_names)} fields: {', '.join(field_names[:3])}..."
    elif schema.get('type') == 'array':
        items = schema.get('items', {})
        if items.get('type') == 'object':
            item_fields = list(items.get('properties', {}).keys())
            return f"Array of objects with fields: {', '.join(item_fields[:3])}"
        else:
            return f"Array of {items.get('type', 'items')}"
    else:
        return f"{schema.get('type', 'unknown')} type"

# Test functions
def test_enhanced_simple_schemas():
    """Test enhanced simple schema functionality"""
    print("🧪 Testing Enhanced Simple Schema Features:")
    print("=" * 60)
    
    # Test 1: Special types
    print("\n1. Testing special types...")
    try:
        schema = user_schema(include_email=True, include_phone=True)
        print(f"   ✅ User schema with special types: {len(schema['properties'])} fields")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Enum fields
    print("\n2. Testing enum fields...")
    try:
        schema = product_schema(include_price=True)
        category_enum = schema['properties']['category'].get('enum')
        print(f"   ✅ Product schema with enum: {category_enum}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Simple arrays
    print("\n3. Testing simple arrays...")
    try:
        schema = simple_array_schema('string', 'Tags', max_items=5)
        print(f"   ✅ String array schema: {schema['type']} of {schema['items']['type']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Email arrays
    print("\n4. Testing email arrays...")
    try:
        schema = simple_array_schema('string', 'Emails', min_items=1, max_items=3, format_hint='email')
        print(f"   ✅ Email array schema with format: {schema['items'].get('format')}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Object arrays
    print("\n5. Testing object arrays...")
    try:
        schema = user_list_schema(include_email=True)
        print(f"   ✅ User list schema: {schema['type']} of objects")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Union types
    print("\n6. Testing union types...")
    try:
        union_field = SimpleField('string', union_types=['string', 'integer'])
        schema_prop = _simple_field_to_json_schema(union_field)
        print(f"   ✅ Union field schema: {'anyOf' in schema_prop}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("Enhanced simple schema tests completed!")

# Integration functions for compatibility
def create_enhanced_field(field_type: str, **kwargs) -> SimpleField:
    """Create enhanced SimpleField with all features"""
    return SimpleField(field_type, **kwargs)

def create_special_type_field(special_type: str, required: bool = True, **kwargs) -> SimpleField:
    """Create field with special type hints"""
    return SimpleField('string', format_hint=special_type, required=required, **kwargs)

def create_enum_field(values: List[str], required: bool = True, **kwargs) -> SimpleField:
    """Create enum field with specific values"""
    return SimpleField('string', choices=values, required=required, **kwargs)

def create_union_field(types: List[str], required: bool = True, **kwargs) -> SimpleField:
    """Create union field with multiple types"""
    primary_type = types[0] if types else 'string'
    return SimpleField(primary_type, union_types=types, required=required, **kwargs)

if __name__ == "__main__":
    # Run tests if script is executed directly
    test_enhanced_simple_schemas()
    print("\n" + "="*60)
    print_examples()