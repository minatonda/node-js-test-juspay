"""
String utility functions for test data generation
"""
import uuid


def generate_random_string(length: int = 10) -> str:
    """
    Generates a random string using UUID hex.
    
    Args:
        length: Length of the string (default: 10)
        
    Returns:
        Random string
    """
    return uuid.uuid4().hex[:length]


def generate_unique_identifier() -> str:
    """
    Generates a unique identifier (UUID).
    
    Returns:
        UUID string
    """
    return str(uuid.uuid4())

