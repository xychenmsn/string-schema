"""
Tests for automatic timezone handling in string-schema utilities.
"""

import pytest
from datetime import datetime, timezone
from string_schema import validate_to_dict, string_to_model


def test_validate_to_dict_naive_datetime_gets_timezone():
    """Test that naive datetime objects get UTC timezone in validate_to_dict."""
    # Test data with naive datetime
    test_data = {
        "name": "Test Event",
        "event_time": datetime(2025, 8, 13, 12, 22, 13),  # Naive datetime
        "description": "A test event"
    }
    
    # Validate with string schema
    result = validate_to_dict(test_data, "name:string, event_time:datetime, description:string")
    
    # Should convert datetime to timezone-aware ISO string
    assert result["name"] == "Test Event"
    assert result["description"] == "A test event"
    assert result["event_time"] == "2025-08-13T12:22:13+00:00"


def test_validate_to_dict_timezone_aware_datetime_preserved():
    """Test that timezone-aware datetime objects preserve their timezone."""
    # Test data with timezone-aware datetime
    utc_datetime = datetime(2025, 8, 13, 12, 22, 13, tzinfo=timezone.utc)
    test_data = {
        "name": "UTC Event",
        "event_time": utc_datetime,
        "active": True
    }
    
    # Validate with string schema
    result = validate_to_dict(test_data, "name:string, event_time:datetime, active:bool")
    
    # Should preserve timezone information
    assert result["name"] == "UTC Event"
    assert result["active"] is True
    assert result["event_time"] == "2025-08-13T12:22:13+00:00"


def test_validate_to_dict_null_datetime_handled():
    """Test that null datetime values are handled correctly."""
    test_data = {
        "name": "No Time Event",
        "event_time": None,
        "priority": 1
    }
    
    # Validate with string schema (optional datetime)
    result = validate_to_dict(test_data, "name:string, event_time:datetime?, priority:int")
    
    # Should handle null values correctly
    assert result["name"] == "No Time Event"
    assert result["event_time"] is None
    assert result["priority"] == 1


def test_validate_to_dict_nested_datetime_handling():
    """Test timezone handling in nested objects."""
    test_data = {
        "user": {
            "name": "John",
            "last_login": datetime(2025, 8, 13, 10, 0, 0),  # Naive datetime
            "profile": {
                "created_at": datetime(2025, 8, 13, 9, 0, 0)  # Naive datetime
            }
        },
        "event_count": 5
    }
    
    # Validate with nested schema
    result = validate_to_dict(
        test_data, 
        "user:{name:string, last_login:datetime, profile:{created_at:datetime}}, event_count:int"
    )
    
    # Should handle nested datetime conversion
    assert result["user"]["name"] == "John"
    assert result["user"]["last_login"] == "2025-08-13T10:00:00+00:00"
    assert result["user"]["profile"]["created_at"] == "2025-08-13T09:00:00+00:00"
    assert result["event_count"] == 5


def test_validate_to_dict_array_datetime_handling():
    """Test timezone handling in arrays."""
    test_data = [
        {
            "id": 1,
            "name": "Event 1",
            "timestamp": datetime(2025, 8, 13, 12, 0, 0)  # Naive datetime
        },
        {
            "id": 2,
            "name": "Event 2", 
            "timestamp": datetime(2025, 8, 13, 13, 0, 0)  # Naive datetime
        }
    ]
    
    # Validate array schema
    result = validate_to_dict(test_data, "[{id:int, name:string, timestamp:datetime}]")
    
    # Should handle datetime conversion in array items
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["name"] == "Event 1"
    assert result[0]["timestamp"] == "2025-08-13T12:00:00+00:00"
    assert result[1]["id"] == 2
    assert result[1]["name"] == "Event 2"
    assert result[1]["timestamp"] == "2025-08-13T13:00:00+00:00"


def test_validate_to_dict_mixed_datetime_types():
    """Test handling of mixed datetime types (naive and timezone-aware)."""
    naive_datetime = datetime(2025, 8, 13, 12, 0, 0)  # Naive
    utc_datetime = datetime(2025, 8, 13, 12, 0, 0, tzinfo=timezone.utc)  # UTC
    
    test_data = {
        "naive_time": naive_datetime,
        "utc_time": utc_datetime,
        "null_time": None,
        "name": "Mixed Test"
    }
    
    # Validate with string schema
    result = validate_to_dict(
        test_data, 
        "naive_time:datetime, utc_time:datetime, null_time:datetime?, name:string"
    )
    
    # Should handle all datetime types correctly
    assert result["naive_time"] == "2025-08-13T12:00:00+00:00"  # Naive → UTC
    assert result["utc_time"] == "2025-08-13T12:00:00+00:00"    # UTC preserved
    assert result["null_time"] is None                          # Null preserved
    assert result["name"] == "Mixed Test"


def test_string_to_model_still_works():
    """Test that string_to_model functionality is not affected by timezone changes."""
    # Create model from string schema
    UserModel = string_to_model("name:string, created_at:datetime, active:bool")
    
    # Create instance with naive datetime
    user = UserModel(
        name="Test User",
        created_at=datetime(2025, 8, 13, 12, 0, 0),
        active=True
    )
    
    # Should create model instance successfully
    assert user.name == "Test User"
    assert isinstance(user.created_at, datetime)
    assert user.active is True
    
    # Model dump should work (timezone conversion happens in validate_to_dict)
    user_dict = user.model_dump() if hasattr(user, 'model_dump') else user.dict()
    assert user_dict["name"] == "Test User"
    assert isinstance(user_dict["created_at"], datetime)  # Still datetime in model_dump
    assert user_dict["active"] is True


def test_performance_impact_minimal():
    """Test that timezone conversion doesn't significantly impact performance."""
    import time
    
    # Large dataset for performance testing
    test_data = [
        {
            "id": i,
            "name": f"Event {i}",
            "timestamp": datetime(2025, 8, 13, 12, i % 60, 0)
        }
        for i in range(100)  # 100 items
    ]
    
    # Measure validation time
    start_time = time.time()
    result = validate_to_dict(test_data, "[{id:int, name:string, timestamp:datetime}]")
    end_time = time.time()
    
    # Should complete quickly (under 1 second for 100 items)
    processing_time = end_time - start_time
    assert processing_time < 1.0, f"Processing took too long: {processing_time:.3f}s"
    
    # Should process all items correctly
    assert len(result) == 100
    assert all("+00:00" in item["timestamp"] for item in result)


if __name__ == "__main__":
    pytest.main([__file__])
