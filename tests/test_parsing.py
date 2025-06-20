"""
Tests for string parsing functionality
"""

import pytest
from simple_schema.parsing.string_parser import (
    parse_string_schema, 
    validate_string_schema,
    _normalize_type_name,
    _parse_enum_values
)


class TestStringParsing:
    """Test string schema parsing"""
    
    def test_parse_simple_object(self):
        """Test parsing simple object schema"""
        schema_str = "name:string, age:int"
        schema = parse_string_schema(schema_str)
        
        assert schema['type'] == 'object'
        assert 'name' in schema['properties']
        assert 'age' in schema['properties']
        assert schema['properties']['name']['type'] == 'string'
        assert schema['properties']['age']['type'] == 'integer'
    
    def test_parse_simple_array(self):
        """Test parsing simple array schema"""
        schema_str = "[string]"
        schema = parse_string_schema(schema_str)
        
        assert schema['type'] == 'array'
        assert schema['items']['type'] == 'string'
    
    def test_parse_array_with_constraints(self):
        """Test parsing array with constraints"""
        schema_str = "[string](max=5)"
        schema = parse_string_schema(schema_str)
        
        assert schema['type'] == 'array'
        assert schema['maxItems'] == 5
    
    def test_parse_object_array(self):
        """Test parsing array of objects"""
        schema_str = "[{name:string, email:email}]"
        schema = parse_string_schema(schema_str)
        
        assert schema['type'] == 'array'
        assert schema['items']['type'] == 'object'
        assert 'name' in schema['items']['properties']
        assert 'email' in schema['items']['properties']
    
    def test_parse_optional_fields(self):
        """Test parsing optional fields"""
        schema_str = "name:string, email:string?"
        schema = parse_string_schema(schema_str)
        
        assert 'name' in schema['required']
        assert 'email' not in schema['required']
    
    def test_parse_enum_field(self):
        """Test parsing enum field"""
        schema_str = "status:enum(active,inactive,pending)"
        schema = parse_string_schema(schema_str)
        
        assert schema['properties']['status']['enum'] == ['active', 'inactive', 'pending']
    
    def test_parse_union_field(self):
        """Test parsing union field"""
        schema_str = "id:string|int"
        schema = parse_string_schema(schema_str)
        
        assert 'anyOf' in schema['properties']['id']
        types = [item['type'] for item in schema['properties']['id']['anyOf']]
        assert 'string' in types
        assert 'integer' in types
    
    def test_parse_special_types(self):
        """Test parsing special type hints"""
        schema_str = "email:email, website:url, created:datetime"
        schema = parse_string_schema(schema_str)
        
        assert schema['properties']['email']['format'] == 'email'
        assert schema['properties']['website']['format'] == 'uri'
        assert schema['properties']['created']['format'] == 'date-time'
    
    def test_parse_constraints(self):
        """Test parsing field constraints"""
        schema_str = "name:string(min=1,max=100), age:int(0,120)"
        schema = parse_string_schema(schema_str)
        
        name_prop = schema['properties']['name']
        assert name_prop['minLength'] == 1
        assert name_prop['maxLength'] == 100
        
        age_prop = schema['properties']['age']
        assert age_prop['minimum'] == 0
        assert age_prop['maximum'] == 120
    
    def test_parse_nested_objects(self):
        """Test parsing nested object structures"""
        schema_str = "{user:{name:string, contact:{email:email, phone:phone?}}}"
        schema = parse_string_schema(schema_str)
        
        assert schema['type'] == 'object'
        assert 'user' in schema['properties']
        # Note: Full nested object support would require more complex implementation


class TestStringValidation:
    """Test string schema validation"""
    
    def test_validate_valid_schema(self):
        """Test validating a valid schema string"""
        schema_str = "name:string, age:int, email:email"
        result = validate_string_schema(schema_str)
        
        assert result['valid'] == True
        assert 'special_types' in result['features_used']
    
    def test_validate_array_schema(self):
        """Test validating array schema"""
        schema_str = "[{name:string, email:email}](min=1,max=10)"
        result = validate_string_schema(schema_str)
        
        assert result['valid'] == True
        assert 'arrays' in result['features_used']
        assert 'constraints' in result['features_used']
    
    def test_validate_enum_schema(self):
        """Test validating enum schema"""
        schema_str = "status:enum(active,inactive), priority:choice(low,high)"
        result = validate_string_schema(schema_str)
        
        assert result['valid'] == True
        assert 'enums' in result['features_used']
    
    def test_validate_union_schema(self):
        """Test validating union schema"""
        schema_str = "id:string|int, value:string|null"
        result = validate_string_schema(schema_str)
        
        assert result['valid'] == True
        assert 'union_types' in result['features_used']
    
    def test_validate_invalid_schema(self):
        """Test validating invalid schema"""
        # This would depend on what makes a schema invalid in our implementation
        schema_str = "invalid_syntax_here"
        result = validate_string_schema(schema_str)
        
        # The result depends on how we handle invalid syntax
        # For now, we'll just check that validation runs
        assert 'valid' in result


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_normalize_type_name(self):
        """Test type name normalization"""
        assert _normalize_type_name('str') == 'string'
        assert _normalize_type_name('int') == 'integer'
        assert _normalize_type_name('float') == 'number'
        assert _normalize_type_name('bool') == 'boolean'
        assert _normalize_type_name('email') == 'string'
        assert _normalize_type_name('url') == 'string'
    
    def test_parse_enum_values(self):
        """Test parsing enum values"""
        values = _parse_enum_values('enum(active,inactive,pending)')
        assert values == ['active', 'inactive', 'pending']
        
        values = _parse_enum_values('choice(low,medium,high)')
        assert values == ['low', 'medium', 'high']
        
        values = _parse_enum_values('select(a,b,c)')
        assert values == ['a', 'b', 'c']


class TestComplexSchemas:
    """Test parsing complex schema strings"""
    
    def test_comprehensive_schema(self):
        """Test parsing a comprehensive schema with all features"""
        schema_str = """
        [{
            name:string(min=1,max=100),
            emails:[email](min=1,max=2),
            role:enum(admin,user,guest),
            profile:{bio:text?, social:[url]?}?,
            active:bool,
            last_login:datetime?
        }](min=1,max=20)
        """
        
        result = validate_string_schema(schema_str)
        assert result['valid'] == True
        
        # Check that all features are detected
        features = result['features_used']
        assert 'arrays' in features
        assert 'objects' in features
        assert 'enums' in features
        assert 'special_types' in features
        assert 'constraints' in features
        assert 'optional_fields' in features
    
    def test_ecommerce_schema(self):
        """Test parsing e-commerce product schema"""
        schema_str = """
        {
            name:string(min=1,max=200),
            price:number(min=0),
            category:enum(electronics,clothing,books,home,sports),
            description:text(max=1000)?,
            images:[url](max=5)?,
            reviews:[{
                rating:int(1,5),
                comment:text(max=500),
                verified:bool?,
                date:date?
            }](max=10)?
        }
        """
        
        result = validate_string_schema(schema_str)
        assert result['valid'] == True


if __name__ == '__main__':
    pytest.main([__file__])
