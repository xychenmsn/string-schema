"""
Simple Schema - A simple, LLM-friendly schema definition library

This library provides an intuitive way to define data schemas using simple syntax
that works well with Large Language Models for data extraction and validation.

Key Features:
- Clear, descriptive function names that tell you exactly what they do
- Direct conversion paths: string → JSON Schema, Pydantic, OpenAPI
- String-based schema syntax parsing
- JSON Schema generation
- Pydantic model integration
- Built-in validation and optimization
"""

# Main conversion functions (clear names)
from .parsing.string_parser import (
    string_to_json_schema,
    validate_string_syntax,
    # Legacy names for backward compatibility
    parse_string_schema,
    validate_string_schema
)

# Integration functions (clear names)
from .integrations.pydantic import (
    string_to_pydantic,
    string_to_pydantic_code,
    json_schema_to_pydantic,
    # Legacy names for backward compatibility
    create_pydantic_from_json_schema
)

from .integrations.openapi import (
    string_to_openapi
)

from .integrations.json_schema import (
    json_schema_to_openapi,
    # Legacy names for backward compatibility
    convert_to_openapi_schema
)

# Note: Built-in presets moved to examples/ directory
# Import them from simple_schema.examples.presets if needed

__version__ = "1.0.0"
__author__ = "Simple Schema Team"

__all__ = [
    # 🎯 Main conversion functions (recommended)
    "string_to_json_schema",        # String → JSON Schema
    "string_to_pydantic",           # String → Pydantic model
    "string_to_pydantic_code",      # String → Pydantic code
    "string_to_openapi",            # String → OpenAPI schema
    "validate_string_syntax",       # Validate string syntax

    # 🔄 Intermediate conversion functions
    "json_schema_to_pydantic",      # JSON Schema → Pydantic model
    "json_schema_to_openapi",       # JSON Schema → OpenAPI schema

    # 🔙 Legacy names (for backward compatibility)
    "parse_string_schema",
    "validate_string_schema",
    "create_pydantic_from_json_schema",
    "convert_to_openapi_schema",
]
