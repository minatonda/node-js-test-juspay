"""
JSON utility functions for test responses
"""
import json
from typing import Any, Dict


def pretty(obj: Any) -> str:
    """Pretty print JSON object"""
    return json.dumps(obj, ensure_ascii=False, indent=2)


def safe_json_parse(response_text: str) -> tuple[bool, Any]:
    """
    Safely parse JSON from response text.
    
    Returns:
        tuple: (success: bool, parsed_data: Any)
    """
    try:
        return True, json.loads(response_text)
    except (json.JSONDecodeError, ValueError):
        return False, None


def get_json_or_none(response) -> Any:
    """
    Get JSON from response or None if parsing fails.
    
    Args:
        response: requests.Response object
        
    Returns:
        Parsed JSON or None
    """
    try:
        return response.json()
    except (json.JSONDecodeError, ValueError):
        return None

