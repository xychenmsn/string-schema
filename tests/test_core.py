"""
Tests for core Simple Schema functionality
"""

import pytest
from simple_schema.core.fields import SimpleField
from simple_schema.core.builders import simple_schema, list_of_objects_schema, simple_array_schema
from simple_schema.core.validators import validate_schema, validate_simple_field


class TestSimpleField:
    """Test SimpleField class"""
    
    def test_basic_field_creation(self):
        """Test creating a basic SimpleField"""
        field = SimpleField('string', 'Test field')
        assert field.field_type == 'string'
        assert field.description == 'Test field'
        assert field.required == True
    
    def test_field_with_constraints(self):
        """Test creating field with constraints"""
        field = SimpleField(
            'string',
            'Test field',
            min_length=1,
            max_length=100,
            required=False
        )
        assert field.min_length == 1
        assert field.max_length == 100
        assert field.required == False
    
    def test_field_with_choices(self):
        """Test creating field with enum choices"""
        field = SimpleField('string', 'Status field', choices=['active', 'inactive'])
        assert field.choices == ['active', 'inactive']
    
    def test_field_with_union_types(self):
        """Test creating field with union types"""
        field = SimpleField('string', 'ID field', union_types=['string', 'integer'])
        assert field.union_types == ['string', 'integer']
    
    def test_field_to_dict(self):
        """Test converting field to dictionary"""
        field = SimpleField('string', 'Test field', min_length=1, max_length=100)
        field_dict = field.to_dict()
        
        assert field_dict['type'] == 'string'
        assert field_dict['description'] == 'Test field'
        assert field_dict['min_length'] == 1
        assert field_dict['max_length'] == 100
    
    def test_field_from_dict(self):
        """Test creating field from dictionary"""
        field_dict = {
            'type': 'string',
            'description': 'Test field',
            'min_length': 1,
            'max_length': 100,
            'required': True
        }
        field = SimpleField.from_dict(field_dict)
        
        assert field.field_type == 'string'
        assert field.description == 'Test field'
        assert field.min_length == 1
        assert field.max_length == 100
        assert field.required == True


class TestSchemaBuilders:
    """Test schema building functions"""
    
    def test_simple_schema_basic(self):
        """Test creating basic schema"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'age': SimpleField('integer', 'Age field')
        }
        schema = simple_schema(fields)
        
        assert schema['type'] == 'object'
        assert 'properties' in schema
        assert 'name' in schema['properties']
        assert 'age' in schema['properties']
        assert schema['required'] == ['name', 'age']
    
    def test_simple_schema_with_optional(self):
        """Test schema with optional fields"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'email': SimpleField('string', 'Email field', required=False)
        }
        schema = simple_schema(fields)
        
        assert schema['required'] == ['name']
        assert 'email' in schema['properties']
    
    def test_simple_schema_from_strings(self):
        """Test creating schema from string field definitions"""
        fields = {
            'name': 'string',
            'age': 'integer'
        }
        schema = simple_schema(fields)
        
        assert schema['type'] == 'object'
        assert len(schema['properties']) == 2
    
    def test_list_of_objects_schema(self):
        """Test creating array schema"""
        item_fields = {
            'name': SimpleField('string', 'Name field'),
            'email': SimpleField('string', 'Email field')
        }
        schema = list_of_objects_schema(item_fields, "List of users")
        
        assert schema['type'] == 'array'
        assert schema['description'] == "List of users"
        assert schema['items']['type'] == 'object'
        assert 'name' in schema['items']['properties']
    
    def test_simple_array_schema(self):
        """Test creating simple array schema"""
        schema = simple_array_schema('string', 'List of tags', min_items=1, max_items=5)
        
        assert schema['type'] == 'array'
        assert schema['items']['type'] == 'string'
        assert schema['minItems'] == 1
        assert schema['maxItems'] == 5
    
    def test_simple_array_with_format(self):
        """Test array with format hint"""
        schema = simple_array_schema('string', 'List of emails', format_hint='email')
        
        assert schema['items']['format'] == 'email'


class TestValidators:
    """Test validation functions"""
    
    def test_validate_simple_field_valid(self):
        """Test validating a valid field"""
        field = SimpleField('string', 'Test field', min_length=1, max_length=100)
        result = validate_simple_field(field)
        
        assert result['valid'] == True
        assert len(result['errors']) == 0
    
    def test_validate_simple_field_invalid_constraints(self):
        """Test validating field with invalid constraints"""
        field = SimpleField('string', 'Test field', min_length=100, max_length=1)
        result = validate_simple_field(field)
        
        assert result['valid'] == False
        assert len(result['errors']) > 0
    
    def test_validate_schema_valid(self):
        """Test validating a valid schema"""
        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'age': {'type': 'integer'}
            },
            'required': ['name']
        }
        result = validate_schema(schema)
        
        assert result['valid'] == True
        assert result['field_count'] == 2
    
    def test_validate_schema_invalid(self):
        """Test validating an invalid schema"""
        schema = {
            'properties': {
                'name': {'type': 'string'}
            }
            # Missing 'type' field
        }
        result = validate_schema(schema)
        
        assert result['valid'] == False
        assert len(result['errors']) > 0


if __name__ == '__main__':
    pytest.main([__file__])
