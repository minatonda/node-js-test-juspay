"""
CRUD test pattern utilities
"""
from typing import Dict, Any, List, Optional, Callable
import requests
import sys
import os

# Add tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.models.test_result import TestResult
from common.assertions.response_assertions import assert_status_code, assert_json_structure


class CrudTestPattern:
    """
    Utilities for testing CRUD operations.
    """
    
    @staticmethod
    def test_create(
        create_func: Callable[[Dict[str, Any]], requests.Response],
        test_data: Dict[str, Any],
        test_name: str,
        expected_status: List[int] = [200, 201],
        required_fields: Optional[List[str]] = None
    ) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Test create operation.
        
        Args:
            create_func: Function that creates the resource
            test_data: Data to create
            test_name: Name of the test
            expected_status: Expected HTTP status codes
            required_fields: Required fields in response
            
        Returns:
            tuple: (success: bool, created_resource: Dict or None)
        """
        response = create_func(test_data)
        result = assert_status_code(response, expected_status, test_name)
        
        if not result.ok:
            return False, None
        
        success, json_result, body = assert_json_structure(
            response,
            f"{test_name} - valid JSON",
            required_fields=required_fields or ["id"]
        )
        
        if not success:
            return False, None
        
        return True, body
    
    @staticmethod
    def test_read(
        read_func: Callable[[str], requests.Response],
        resource_id: str,
        test_name: str,
        expected_status: List[int] = [200],
        required_fields: Optional[List[str]] = None
    ) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Test read operation.
        
        Args:
            read_func: Function that reads the resource
            resource_id: ID of the resource
            test_name: Name of the test
            expected_status: Expected HTTP status codes
            required_fields: Required fields in response
            
        Returns:
            tuple: (success: bool, resource: Dict or None)
        """
        response = read_func(resource_id)
        result = assert_status_code(response, expected_status, test_name)
        
        if not result.ok:
            return False, None
        
        success, json_result, body = assert_json_structure(
            response,
            f"{test_name} - valid JSON",
            required_fields=required_fields
        )
        
        if not success:
            return False, None
        
        return True, body
    
    @staticmethod
    def test_update(
        update_func: Callable[[str, Dict[str, Any]], requests.Response],
        resource_id: str,
        update_data: Dict[str, Any],
        test_name: str,
        expected_status: List[int] = [200]
    ) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Test update operation.
        
        Args:
            update_func: Function that updates the resource
            resource_id: ID of the resource
            update_data: Data to update
            test_name: Name of the test
            expected_status: Expected HTTP status codes
            
        Returns:
            tuple: (success: bool, updated_resource: Dict or None)
        """
        response = update_func(resource_id, update_data)
        result = assert_status_code(response, expected_status, test_name)
        
        if not result.ok:
            return False, None
        
        success, json_result, body = assert_json_structure(
            response,
            f"{test_name} - valid JSON"
        )
        
        if not success:
            return False, None
        
        return True, body
    
    @staticmethod
    def test_delete(
        delete_func: Callable[[str], requests.Response],
        resource_id: str,
        test_name: str,
        expected_status: List[int] = [200, 204]
    ) -> bool:
        """
        Test delete operation.
        
        Args:
            delete_func: Function that deletes the resource
            resource_id: ID of the resource
            test_name: Name of the test
            expected_status: Expected HTTP status codes
            
        Returns:
            True if successful, False otherwise
        """
        response = delete_func(resource_id)
        result = assert_status_code(response, expected_status, test_name)
        return result.ok
    
    @staticmethod
    def test_not_found(
        read_func: Callable[[str], requests.Response],
        invalid_id: str,
        test_name: str
    ) -> bool:
        """
        Test that invalid ID returns 404.
        
        Args:
            read_func: Function that reads the resource
            invalid_id: Invalid resource ID
            test_name: Name of the test
            
        Returns:
            True if 404 is returned, False otherwise
        """
        response = read_func(invalid_id)
        result = assert_status_code(response, [404], test_name)
        return result.ok

