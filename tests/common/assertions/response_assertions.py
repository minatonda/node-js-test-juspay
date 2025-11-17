"""
Response assertion utilities for API testing
"""
from typing import List, Any, Dict, Optional
import requests
import sys
import os

# Add tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.models.test_result import TestResult


def assert_status_code(
    response: requests.Response,
    expected_codes: List[int],
    test_name: str,
    body_preview_length: int = 200
) -> TestResult:
    """
    Assert that response status code is in the expected list.
    
    Args:
        response: HTTP response object
        expected_codes: List of acceptable status codes
        test_name: Name of the test
        body_preview_length: Length of body preview in error message
        
    Returns:
        TestResult object
    """
    result = TestResult(test_name)
    
    if response.status_code not in expected_codes:
        body_preview = response.text[:body_preview_length] if response.text else "empty"
        result.fail(f"HTTP {response.status_code}, body={body_preview}")
    
    return result


def assert_json_structure(
    response: requests.Response,
    test_name: str,
    required_fields: Optional[List[str]] = None,
    expected_type: type = dict
) -> tuple[bool, TestResult, Any]:
    """
    Assert that response is valid JSON with expected structure.
    
    Args:
        response: HTTP response object
        test_name: Name of the test
        required_fields: List of required field names
        expected_type: Expected JSON type (dict, list, etc.)
        
    Returns:
        tuple: (success: bool, TestResult, parsed_json: Any)
    """
    result = TestResult(test_name)
    
    try:
        body = response.json()
    except (ValueError, AttributeError):
        result.fail("Response is not valid JSON")
        return False, result, None
    
    if not isinstance(body, expected_type):
        result.fail(f"Response is not of type {expected_type.__name__}")
        return False, result, None
    
    if required_fields:
        missing_fields = [field for field in required_fields if field not in body]
        if missing_fields:
            result.fail(f"Missing required fields: {missing_fields}")
            return False, result, body
    
    return True, result, body


def assert_pagination_structure(
    response: requests.Response,
    test_name: str
) -> tuple[bool, TestResult, Optional[Dict[str, Any]]]:
    """
    Assert that response has pagination structure.
    
    Expected structure:
    {
        "items": [...],
        "total": number,
        "page": number,
        "limit": number,
        "pageCount": number
    }
    
    Args:
        response: HTTP response object
        test_name: Name of the test
        
    Returns:
        tuple: (success: bool, TestResult, parsed_json: Dict or None)
    """
    success, result, body = assert_json_structure(
        response,
        test_name,
        required_fields=["items", "total", "page", "limit"],
        expected_type=dict
    )
    
    if not success:
        return False, result, None
    
    # Additional pagination-specific checks
    if not isinstance(body.get("items"), list):
        result.fail("Field 'items' is not an array")
        return False, result, body
    
    return True, result, body


def assert_field_value(
    data: Dict[str, Any],
    field_name: str,
    expected_value: Any,
    test_name: str
) -> TestResult:
    """
    Assert that a field in the data has the expected value.
    
    Args:
        data: Dictionary containing the data
        field_name: Name of the field to check
        expected_value: Expected value
        test_name: Name of the test
        
    Returns:
        TestResult object
    """
    result = TestResult(test_name)
    
    if field_name not in data:
        result.fail(f"Field '{field_name}' not found in response")
        return result
    
    actual_value = data.get(field_name)
    if actual_value != expected_value:
        result.fail(f"Expected {field_name}='{expected_value}', obtained '{actual_value}'")
        return result
    
    return result


def assert_field_type(
    data: Dict[str, Any],
    field_name: str,
    expected_type: type,
    test_name: str
) -> TestResult:
    """
    Assert that a field in the data has the expected type.
    
    Args:
        data: Dictionary containing the data
        field_name: Name of the field to check
        expected_type: Expected type
        test_name: Name of the test
        
    Returns:
        TestResult object
    """
    result = TestResult(test_name)
    
    if field_name not in data:
        result.fail(f"Field '{field_name}' not found in response")
        return result
    
    actual_value = data.get(field_name)
    if not isinstance(actual_value, expected_type):
        result.fail(
            f"Field '{field_name}' is not of type {expected_type.__name__}. "
            f"Type: {type(actual_value).__name__}, Value: {actual_value}"
        )
        return result
    
    return result

