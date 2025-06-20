"""
Simple Schema - A simple, LLM-friendly schema definition library

This library provides an intuitive way to define data schemas using simple syntax
that works well with Large Language Models for data extraction and validation.

Key Features:
- Simple field definitions with type hints
- String-based schema syntax parsing
- JSON Schema generation
- Pydantic model integration
- Built-in validation and optimization
"""

from .core.fields import SimpleField
from .core.builders import (
    simple_schema,
    list_of_objects_schema,
    simple_array_schema,
    quick_pydantic_model
)
from .parsing.string_parser import parse_string_schema
from .examples.presets import (
    user_schema,
    product_schema,
    contact_schema,
    article_schema,
    event_schema
)

__version__ = "1.0.0"
__author__ = "Simple Schema Team"

__all__ = [
    # Core classes
    "SimpleField",
    
    # Schema builders
    "simple_schema",
    "list_of_objects_schema", 
    "simple_array_schema",
    "quick_pydantic_model",
    
    # String parsing
    "parse_string_schema",
    
    # Built-in schemas
    "user_schema",
    "product_schema",
    "contact_schema",
    "article_schema",
    "event_schema",
]
