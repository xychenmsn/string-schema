"""
Pydantic integration for Simple Schema

Contains functions for creating Pydantic models from Simple Schema definitions.
"""

from typing import Any, Dict, List, Optional, Union, Type
import logging

from ..core.fields import SimpleField

# Optional pydantic import
try:
    from pydantic import BaseModel, Field, create_model
    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    BaseModel = None
    Field = None
    create_model = None

logger = logging.getLogger(__name__)


def create_pydantic_model(name: str, fields: Dict[str, Union[str, SimpleField]],
                         base_class: Type = None) -> Type:
    """
    Create Pydantic model from Simple Schema field definitions.

    Args:
        name: Name of the model class
        fields: Dictionary of field definitions
        base_class: Base class to inherit from (default: BaseModel)

    Returns:
        Dynamically created Pydantic model class
    """
    if not HAS_PYDANTIC:
        raise ImportError("Pydantic is required for create_pydantic_model. Install with: pip install pydantic")

    if base_class is None:
        base_class = BaseModel

    pydantic_fields = {}

    for field_name, field_def in fields.items():
        if isinstance(field_def, str):
            field_def = SimpleField(field_def)

        python_type, field_info = _simple_field_to_pydantic(field_def)
        pydantic_fields[field_name] = (python_type, field_info)

    # Create the model with the specified base class
    return create_model(name, __base__=base_class, **pydantic_fields)


def _simple_field_to_pydantic(field: SimpleField) -> tuple:
    """Convert SimpleField to Pydantic field specification"""
    if not HAS_PYDANTIC:
        raise ImportError("Pydantic is required for this function")

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


def create_pydantic_from_json_schema(name: str, json_schema: Dict[str, Any]) -> Type[BaseModel]:
    """
    Create Pydantic model from JSON Schema.
    
    Args:
        name: Name of the model class
        json_schema: JSON Schema dictionary
        
    Returns:
        Dynamically created Pydantic model class
    """
    if json_schema.get('type') != 'object':
        raise ValueError("JSON Schema must be of type 'object' to create Pydantic model")
    
    properties = json_schema.get('properties', {})
    required_fields = set(json_schema.get('required', []))
    
    pydantic_fields = {}
    
    for field_name, field_schema in properties.items():
        python_type, field_info = _json_schema_to_pydantic_field(field_schema, field_name in required_fields)
        pydantic_fields[field_name] = (python_type, field_info)
    
    return create_model(name, **pydantic_fields)


def _json_schema_to_pydantic_field(field_schema: Dict[str, Any], required: bool = True) -> tuple:
    """Convert JSON Schema field to Pydantic field specification"""
    # Type mapping
    type_mapping = {
        'string': str,
        'integer': int,
        'number': float,
        'boolean': bool
    }
    
    # Handle union types
    if 'anyOf' in field_schema:
        from typing import Union as TypingUnion
        union_types = []
        for union_option in field_schema['anyOf']:
            option_type = type_mapping.get(union_option.get('type', 'string'), str)
            union_types.append(option_type)
        python_type = TypingUnion[tuple(union_types)]
    else:
        field_type = field_schema.get('type', 'string')
        python_type = type_mapping.get(field_type, str)
    
    # Handle optional fields
    if not required:
        python_type = Optional[python_type]
    
    # Build Field arguments
    field_kwargs = {}
    
    if 'description' in field_schema:
        field_kwargs['description'] = field_schema['description']
    
    if 'default' in field_schema:
        field_kwargs['default'] = field_schema['default']
    elif not required:
        field_kwargs['default'] = None
    
    # Numeric constraints
    if 'minimum' in field_schema:
        field_kwargs['ge'] = field_schema['minimum']
    if 'maximum' in field_schema:
        field_kwargs['le'] = field_schema['maximum']
    
    # String constraints
    if 'minLength' in field_schema:
        field_kwargs['min_length'] = field_schema['minLength']
    if 'maxLength' in field_schema:
        field_kwargs['max_length'] = field_schema['maxLength']
    
    # Enum constraints
    if 'enum' in field_schema:
        # Pydantic handles enums automatically when values are provided
        pass
    
    return python_type, Field(**field_kwargs) if field_kwargs else Field()


def model_to_simple_fields(model: Type[BaseModel]) -> Dict[str, SimpleField]:
    """
    Convert Pydantic model to Simple Schema field definitions.
    
    Args:
        model: Pydantic model class
        
    Returns:
        Dictionary of SimpleField objects
    """
    fields = {}
    
    for field_name, field_info in model.model_fields.items():
        simple_field = _pydantic_field_to_simple_field(field_info, field_name)
        fields[field_name] = simple_field
    
    return fields


def _pydantic_field_to_simple_field(field_info: Any, field_name: str) -> SimpleField:
    """Convert Pydantic field info to SimpleField"""
    # This is a simplified conversion - could be enhanced
    
    # Determine field type
    annotation = getattr(field_info, 'annotation', str)
    
    if annotation == str:
        field_type = 'string'
    elif annotation == int:
        field_type = 'integer'
    elif annotation == float:
        field_type = 'number'
    elif annotation == bool:
        field_type = 'boolean'
    else:
        # Handle Optional and Union types
        if hasattr(annotation, '__origin__'):
            if annotation.__origin__ is Union:
                # Union type - use first non-None type
                args = annotation.__args__
                non_none_types = [arg for arg in args if arg is not type(None)]
                if non_none_types:
                    first_type = non_none_types[0]
                    if first_type == str:
                        field_type = 'string'
                    elif first_type == int:
                        field_type = 'integer'
                    elif first_type == float:
                        field_type = 'number'
                    elif first_type == bool:
                        field_type = 'boolean'
                    else:
                        field_type = 'string'
                else:
                    field_type = 'string'
            else:
                field_type = 'string'
        else:
            field_type = 'string'
    
    # Determine if required
    required = field_info.is_required() if hasattr(field_info, 'is_required') else True
    
    # Get default value
    default = getattr(field_info, 'default', None)
    if default is ...:  # Ellipsis indicates no default
        default = None
    
    # Get description
    description = getattr(field_info, 'description', '')
    
    # Create SimpleField
    simple_field = SimpleField(
        field_type=field_type,
        description=description,
        required=required,
        default=default
    )
    
    return simple_field


def validate_pydantic_compatibility(fields: Dict[str, SimpleField]) -> Dict[str, Any]:
    """
    Validate that Simple Schema fields are compatible with Pydantic.
    
    Args:
        fields: Dictionary of SimpleField objects
        
    Returns:
        Validation result dictionary
    """
    result = {
        'compatible': True,
        'warnings': [],
        'errors': []
    }
    
    for field_name, field in fields.items():
        # Check for unsupported features
        if field.union_types and len(field.union_types) > 2:
            result['warnings'].append(f"Field '{field_name}' has complex union type - may need manual handling")
        
        if field.format_hint and field.format_hint not in ['email', 'url', 'uuid']:
            result['warnings'].append(f"Field '{field_name}' format hint '{field.format_hint}' may not be fully supported")
        
        # Check for conflicting constraints
        if field.min_val is not None and field.max_val is not None:
            if field.min_val > field.max_val:
                result['errors'].append(f"Field '{field_name}' has min_val > max_val")
        
        if field.min_length is not None and field.max_length is not None:
            if field.min_length > field.max_length:
                result['errors'].append(f"Field '{field_name}' has min_length > max_length")
    
    result['compatible'] = len(result['errors']) == 0
    return result


def generate_pydantic_code(name: str, fields: Dict[str, SimpleField]) -> str:
    """
    Generate Pydantic model code as a string.
    
    Args:
        name: Name of the model class
        fields: Dictionary of SimpleField objects
        
    Returns:
        Python code string for the Pydantic model
    """
    lines = [
        "from pydantic import BaseModel, Field",
        "from typing import Optional, Union",
        "",
        f"class {name}(BaseModel):"
    ]
    
    if not fields:
        lines.append("    pass")
        return "\n".join(lines)
    
    for field_name, field in fields.items():
        field_line = _generate_pydantic_field_code(field_name, field)
        lines.append(f"    {field_line}")
    
    return "\n".join(lines)


def _generate_pydantic_field_code(field_name: str, field: SimpleField) -> str:
    """Generate code for a single Pydantic field"""
    # Determine Python type
    type_mapping = {
        'string': 'str',
        'integer': 'int', 
        'number': 'float',
        'boolean': 'bool'
    }
    
    python_type = type_mapping.get(field.field_type, 'str')
    
    # Handle union types
    if field.union_types and len(field.union_types) > 1:
        union_types = []
        for union_type in field.union_types:
            if union_type == 'null':
                union_types.append('None')
            else:
                union_types.append(type_mapping.get(union_type, 'str'))
        python_type = f"Union[{', '.join(union_types)}]"
    
    # Handle optional
    if not field.required:
        if 'Union' not in python_type:
            python_type = f"Optional[{python_type}]"
    
    # Build field definition
    field_parts = []
    
    if field.description:
        field_parts.append(f"description='{field.description}'")
    
    if field.default is not None:
        if isinstance(field.default, str):
            field_parts.append(f"default='{field.default}'")
        else:
            field_parts.append(f"default={field.default}")
    elif not field.required:
        field_parts.append("default=None")
    
    # Add constraints
    if field.min_val is not None:
        field_parts.append(f"ge={field.min_val}")
    if field.max_val is not None:
        field_parts.append(f"le={field.max_val}")
    if field.min_length is not None:
        field_parts.append(f"min_length={field.min_length}")
    if field.max_length is not None:
        field_parts.append(f"max_length={field.max_length}")
    
    if field_parts:
        field_def = f"Field({', '.join(field_parts)})"
    else:
        field_def = "Field()"
    
    return f"{field_name}: {python_type} = {field_def}"
