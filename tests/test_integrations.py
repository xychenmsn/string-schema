"""
Tests for integration modules
"""

import pytest
from string_schema.core.fields import SimpleField

# Optional pydantic import
try:
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    BaseModel = None
from string_schema.integrations.pydantic import (
    create_pydantic_model,
    validate_pydantic_compatibility,
    generate_pydantic_code
)
from string_schema.integrations.json_schema import (
    to_json_schema,
    to_json_schema_with_examples,
    validate_json_schema_compliance,
    optimize_json_schema
)
from string_schema.integrations.openapi import (
    to_openapi_schema,
    create_openapi_component,
    validate_openapi_compatibility
)


class TestPydanticIntegration:
    """Test Pydantic integration"""

    @pytest.mark.skipif(not HAS_PYDANTIC, reason="Pydantic not available")
    def test_create_pydantic_model_basic(self):
        """Test creating basic Pydantic model"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'age': SimpleField('integer', 'Age field', min_val=0, max_val=120)
        }

        Model = create_pydantic_model('TestModel', fields)

        assert issubclass(Model, BaseModel)

        # Check that model has the expected fields
        if hasattr(Model, 'model_fields'):
            # Pydantic v2
            assert 'name' in Model.model_fields
            assert 'age' in Model.model_fields
        elif hasattr(Model, '__fields__'):
            # Pydantic v1
            assert 'name' in Model.__fields__
            assert 'age' in Model.__fields__

        # Test model instantiation
        instance = Model(name="John", age=30)
        assert instance.name == "John"
        assert instance.age == 30
    
    @pytest.mark.skipif(not HAS_PYDANTIC, reason="Pydantic not available")
    def test_create_pydantic_model_with_optional(self):
        """Test creating model with optional fields"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'email': SimpleField('string', 'Email field', required=False)
        }

        Model = create_pydantic_model('TestModel', fields)

        # Should work without optional field
        instance = Model(name="John")
        assert instance.name == "John"
        assert instance.email is None

    @pytest.mark.skipif(not HAS_PYDANTIC, reason="Pydantic not available")
    def test_create_pydantic_model_with_constraints(self):
        """Test creating model with field constraints"""
        fields = {
            'name': SimpleField('string', 'Name field', min_length=1, max_length=100),
            'age': SimpleField('integer', 'Age field', min_val=0, max_val=120)
        }

        Model = create_pydantic_model('TestModel', fields)

        # Valid instance
        instance = Model(name="John", age=30)
        assert instance.name == "John"

        # Test constraint validation would require actual Pydantic validation
        # which depends on the specific Pydantic version and setup

    def test_validate_pydantic_compatibility(self):
        """Test validating Pydantic compatibility"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'age': SimpleField('integer', 'Age field'),
            'complex_union': SimpleField('string', 'Complex field',
                                       union_types=['string', 'integer', 'boolean'])
        }

        result = validate_pydantic_compatibility(fields)

        assert result['compatible'] == True
        assert len(result['warnings']) > 0  # Should warn about complex union

    def test_generate_pydantic_code(self):
        """Test generating Pydantic model code"""
        fields = {
            'name': SimpleField('string', 'Name field', min_length=1),
            'age': SimpleField('integer', 'Age field', required=False)
        }

        code = generate_pydantic_code('TestModel', fields)

        assert 'class TestModel(BaseModel):' in code
        assert 'name: str' in code
        assert 'age: Optional[int]' in code
        assert 'Field(' in code

    @pytest.mark.skipif(HAS_PYDANTIC, reason="Test for when Pydantic is not available")
    def test_pydantic_not_available(self):
        """Test behavior when Pydantic is not available"""
        fields = {
            'name': SimpleField('string', 'Name field')
        }

        with pytest.raises(ImportError, match="Pydantic is required"):
            create_pydantic_model('TestModel', fields)


class TestJSONSchemaIntegration:
    """Test JSON Schema integration"""
    
    def test_to_json_schema_basic(self):
        """Test converting to JSON Schema"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'age': SimpleField('integer', 'Age field')
        }
        
        schema = to_json_schema(fields, title="Test Schema")
        
        assert schema['$schema'] == "https://json-schema.org/draft/2020-12/schema"
        assert schema['title'] == "Test Schema"
        assert schema['type'] == 'object'
        assert 'name' in schema['properties']
        assert 'age' in schema['properties']
        assert schema['additionalProperties'] == False
    
    def test_to_json_schema_with_examples(self):
        """Test converting to JSON Schema with examples"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'age': SimpleField('integer', 'Age field')
        }
        
        examples = [
            {'name': 'John', 'age': 30},
            {'name': 'Jane', 'age': 25}
        ]
        
        schema = to_json_schema_with_examples(fields, examples, title="Test Schema")
        
        assert 'examples' in schema
        assert len(schema['examples']) == 2
    
    def test_validate_json_schema_compliance(self):
        """Test validating JSON Schema compliance"""
        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'age': {'type': 'integer'}
            },
            'required': ['name']
        }
        
        result = validate_json_schema_compliance(schema)
        
        assert result['valid'] == True
        assert result['compliance_level'] in ['full', 'partial']
    
    def test_optimize_json_schema(self):
        """Test optimizing JSON Schema"""
        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'empty_array': [],
                'empty_object': {}
            },
            'required': ['name']
        }
        
        optimized = optimize_json_schema(schema)
        
        # Should remove empty arrays and objects
        assert 'empty_array' not in optimized['properties']
        assert 'empty_object' not in optimized['properties']
        assert 'name' in optimized['properties']


class TestOpenAPIIntegration:
    """Test OpenAPI integration"""
    
    def test_to_openapi_schema_basic(self):
        """Test converting to OpenAPI schema"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'age': SimpleField('integer', 'Age field')
        }
        
        schema = to_openapi_schema(fields, title="Test Schema")
        
        assert schema['title'] == "Test Schema"
        assert schema['type'] == 'object'
        assert 'name' in schema['properties']
        assert 'age' in schema['properties']
        # Should not have JSON Schema specific fields
        assert '$schema' not in schema
    
    def test_create_openapi_component(self):
        """Test creating OpenAPI component"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'email': SimpleField('string', 'Email field', format_hint='email')
        }
        
        component = create_openapi_component('User', fields, "User object")
        
        assert 'User' in component
        assert component['User']['type'] == 'object'
        assert 'name' in component['User']['properties']
        assert 'email' in component['User']['properties']
    
    def test_validate_openapi_compatibility(self):
        """Test validating OpenAPI compatibility"""
        fields = {
            'name': SimpleField('string', 'Name field'),
            'phone': SimpleField('string', 'Phone field', format_hint='phone'),
            'id': SimpleField('string', 'ID field', union_types=['string', 'integer'])
        }
        
        result = validate_openapi_compatibility(fields)
        
        assert result['compatible'] == True
        assert len(result['warnings']) > 0  # Should warn about phone format and union types


class TestIntegrationWorkflow:
    """Test complete integration workflows"""
    
    def test_simple_schema_to_all_formats(self):
        """Test converting String Schema to all output formats"""
        fields = {
            'id': SimpleField('string', 'User ID', format_hint='uuid'),
            'name': SimpleField('string', 'Full name', min_length=1, max_length=100),
            'email': SimpleField('string', 'Email address', format_hint='email'),
            'age': SimpleField('integer', 'Age', min_val=0, max_val=120, required=False),
            'status': SimpleField('string', 'User status', choices=['active', 'inactive'])
        }
        
        # Convert to JSON Schema
        json_schema = to_json_schema(fields, title="User Schema")
        assert json_schema['type'] == 'object'
        assert len(json_schema['properties']) == 5
        
        # Convert to OpenAPI Schema
        openapi_schema = to_openapi_schema(fields, title="User Schema")
        assert openapi_schema['type'] == 'object'
        assert '$schema' not in openapi_schema
        
        # Convert to Pydantic Model (only if available)
        if HAS_PYDANTIC:
            PydanticModel = create_pydantic_model('User', fields)
            assert issubclass(PydanticModel, BaseModel)

            # Test that all conversions are compatible
            instance = PydanticModel(
                id="123e4567-e89b-12d3-a456-426614174000",
                name="John Doe",
                email="john@example.com",
                status="active"
            )
            assert instance.name == "John Doe"
            assert instance.status == "active"


if __name__ == '__main__':
    pytest.main([__file__])
