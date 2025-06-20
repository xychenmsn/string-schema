"""
Tests for example schemas and recipes
"""

import pytest
from simple_schema.examples.presets import (
    user_schema,
    product_schema,
    contact_schema,
    article_schema,
    event_schema,
    get_examples
)
from simple_schema.examples.recipes import (
    create_list_schema,
    create_enum_schema,
    create_union_schema,
    create_pagination_schema,
    create_api_response_schema,
    create_ecommerce_product_schema,
    create_blog_post_schema
)


class TestPresetSchemas:
    """Test built-in preset schemas"""
    
    def test_user_schema_basic(self):
        """Test basic user schema"""
        schema = user_schema()
        
        assert schema['type'] == 'object'
        assert 'name' in schema['properties']
        assert 'age' in schema['properties']
        assert 'name' in schema['required']
    
    def test_user_schema_with_email(self):
        """Test user schema with email"""
        schema = user_schema(include_email=True)
        
        assert 'email' in schema['properties']
        assert schema['properties']['email']['format'] == 'email'
        assert 'email' in schema['required']
    
    def test_user_schema_with_phone(self):
        """Test user schema with phone"""
        schema = user_schema(include_phone=True)
        
        assert 'phone' in schema['properties']
        assert 'phone' not in schema['required']  # Phone is optional
    
    def test_user_schema_with_profile(self):
        """Test user schema with profile fields"""
        schema = user_schema(include_profile=True)
        
        assert 'bio' in schema['properties']
        assert 'avatar' in schema['properties']
        assert schema['properties']['avatar']['format'] == 'uri'
    
    def test_product_schema_basic(self):
        """Test basic product schema"""
        schema = product_schema()
        
        assert schema['type'] == 'object'
        assert 'name' in schema['properties']
        assert 'category' in schema['properties']
        assert 'enum' in schema['properties']['category']
    
    def test_product_schema_with_price(self):
        """Test product schema with price"""
        schema = product_schema(include_price=True)
        
        assert 'price' in schema['properties']
        assert schema['properties']['price']['minimum'] == 0
    
    def test_contact_schema_basic(self):
        """Test basic contact schema"""
        schema = contact_schema()
        
        assert schema['type'] == 'object'
        assert 'name' in schema['properties']
        assert 'email' in schema['properties']
        assert 'phone' in schema['properties']
    
    def test_contact_schema_with_company(self):
        """Test contact schema with company info"""
        schema = contact_schema(include_company=True)
        
        assert 'company' in schema['properties']
        assert 'job_title' in schema['properties']
    
    def test_article_schema_basic(self):
        """Test basic article schema"""
        schema = article_schema()
        
        assert schema['type'] == 'object'
        assert 'title' in schema['properties']
        assert 'content' in schema['properties']
        assert schema['properties']['content']['minLength'] == 10
    
    def test_event_schema_basic(self):
        """Test basic event schema"""
        schema = event_schema()
        
        assert schema['type'] == 'object'
        assert 'title' in schema['properties']
        assert 'date' in schema['properties']
        assert 'status' in schema['properties']
        assert 'enum' in schema['properties']['status']
    
    def test_get_examples(self):
        """Test getting all examples"""
        examples = get_examples()
        
        assert isinstance(examples, dict)
        assert len(examples) > 0
        
        for name, example in examples.items():
            assert 'description' in example
            assert 'schema' in example
            assert 'prompt_example' in example


class TestRecipeSchemas:
    """Test recipe schema functions"""
    
    def test_create_list_schema(self):
        """Test creating list schema"""
        from simple_schema.core.fields import SimpleField
        
        item_fields = {
            'name': SimpleField('string', 'Name field'),
            'email': SimpleField('string', 'Email field')
        }
        
        schema = create_list_schema(item_fields, "List of users", min_items=1, max_items=10)
        
        assert schema['type'] == 'array'
        assert schema['description'] == "List of users"
        assert schema['minItems'] == 1
        assert schema['maxItems'] == 10
        assert schema['items']['type'] == 'object'
    
    def test_create_enum_schema(self):
        """Test creating enum schema"""
        schema = create_enum_schema('status', ['active', 'inactive', 'pending'])
        
        assert schema['type'] == 'object'
        assert 'status' in schema['properties']
        assert schema['properties']['status']['enum'] == ['active', 'inactive', 'pending']
    
    def test_create_union_schema(self):
        """Test creating union schema"""
        schema = create_union_schema('id', ['string', 'integer'])
        
        assert schema['type'] == 'object'
        assert 'id' in schema['properties']
        # Union handling depends on implementation details
    
    def test_create_pagination_schema(self):
        """Test creating pagination schema"""
        from simple_schema.core.fields import SimpleField
        
        item_fields = {
            'name': SimpleField('string', 'Name field')
        }
        
        schema = create_pagination_schema(item_fields)
        
        assert schema['type'] == 'object'
        assert 'items' in schema['properties']
        assert 'total' in schema['properties']
        assert 'page' in schema['properties']
        assert 'per_page' in schema['properties']
    
    def test_create_api_response_schema(self):
        """Test creating API response schema"""
        from simple_schema.core.fields import SimpleField
        
        data_fields = {
            'message': SimpleField('string', 'Response message')
        }
        
        schema = create_api_response_schema(data_fields)
        
        assert schema['type'] == 'object'
        assert 'data' in schema['properties']
        assert 'success' in schema['properties']
        assert 'message' in schema['properties']
    
    def test_create_ecommerce_product_schema(self):
        """Test creating e-commerce product schema"""
        schema = create_ecommerce_product_schema()
        
        assert schema['type'] == 'object'
        assert 'id' in schema['properties']
        assert 'name' in schema['properties']
        assert 'price' in schema['properties']
        assert 'category' in schema['properties']
        assert 'sku' in schema['properties']
        
        # Check that it has reasonable constraints
        assert schema['properties']['price']['minimum'] == 0
        assert 'enum' in schema['properties']['category']
    
    def test_create_blog_post_schema(self):
        """Test creating blog post schema"""
        schema = create_blog_post_schema()
        
        assert schema['type'] == 'object'
        assert 'id' in schema['properties']
        assert 'title' in schema['properties']
        assert 'content' in schema['properties']
        assert 'author_id' in schema['properties']
        assert 'status' in schema['properties']
        
        # Check constraints
        assert schema['properties']['title']['minLength'] == 1
        assert schema['properties']['content']['minLength'] == 10
        assert 'enum' in schema['properties']['status']


class TestSchemaValidation:
    """Test that all example schemas are valid"""
    
    def test_all_preset_schemas_valid(self):
        """Test that all preset schemas are valid JSON Schema"""
        from simple_schema.core.validators import validate_schema
        
        # Test all preset schemas with various options
        schemas_to_test = [
            user_schema(),
            user_schema(include_email=True, include_phone=True, include_profile=True),
            product_schema(),
            product_schema(include_price=True, include_description=True),
            contact_schema(),
            contact_schema(include_company=True, include_social=True),
            article_schema(),
            article_schema(include_summary=True, include_tags=True, include_metadata=True),
            event_schema(),
            event_schema(include_location=True, include_attendees=True)
        ]
        
        for schema in schemas_to_test:
            result = validate_schema(schema)
            assert result['valid'] == True, f"Schema validation failed: {result['errors']}"
    
    def test_all_recipe_schemas_valid(self):
        """Test that all recipe schemas are valid"""
        from simple_schema.core.validators import validate_schema
        from simple_schema.core.fields import SimpleField
        
        # Test recipe schemas
        item_fields = {
            'name': SimpleField('string', 'Name field'),
            'email': SimpleField('string', 'Email field')
        }
        
        schemas_to_test = [
            create_list_schema(item_fields),
            create_enum_schema('status', ['active', 'inactive']),
            create_union_schema('id', ['string', 'integer']),
            create_pagination_schema(item_fields),
            create_api_response_schema(item_fields),
            create_ecommerce_product_schema(),
            create_blog_post_schema()
        ]
        
        for schema in schemas_to_test:
            result = validate_schema(schema)
            assert result['valid'] == True, f"Schema validation failed: {result['errors']}"


if __name__ == '__main__':
    pytest.main([__file__])
