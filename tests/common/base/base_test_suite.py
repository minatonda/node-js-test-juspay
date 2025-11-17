"""
Base test suite class with common test utilities
"""
from typing import List, Dict, Any, Optional
import requests
import sys
import os

# Add tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.models.test_result import TestResult
from common.assertions.response_assertions import (
    assert_status_code,
    assert_json_structure,
    assert_pagination_structure,
    assert_field_value,
    assert_field_type
)


class BaseTestSuite:
    """
    Base class for test suites.
    Provides common test utilities and result tracking.
    """
    
    def __init__(self, api_client):
        """
        Initialize test suite.
        
        Args:
            api_client: API client instance
        """
        self.api = api_client
        self.results: List[TestResult] = []
        self.test_data: List[Dict[str, Any]] = []  # Store test data
    
    def add_result(self, result: TestResult):
        """
        Add test result and print it.
        
        Args:
            result: TestResult object
        """
        print(str(result))
        self.results.append(result)
    
    def assert_status(
        self,
        response: requests.Response,
        expected_codes: List[int],
        test_name: str
    ) -> bool:
        """
        Assert HTTP status code and add result.
        
        Args:
            response: HTTP response
            expected_codes: List of acceptable status codes
            test_name: Name of the test
            
        Returns:
            True if assertion passed, False otherwise
        """
        result = assert_status_code(response, expected_codes, test_name)
        self.add_result(result)
        return result.ok
    
    def assert_json(
        self,
        response: requests.Response,
        test_name: str,
        required_fields: Optional[List[str]] = None
    ) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Assert JSON structure and add result.
        
        Args:
            response: HTTP response
            test_name: Name of the test
            required_fields: List of required field names
            
        Returns:
            tuple: (success: bool, parsed_json: Dict or None)
        """
        success, result, body = assert_json_structure(
            response,
            test_name,
            required_fields=required_fields
        )
        self.add_result(result)
        return success, body
    
    def assert_pagination(
        self,
        response: requests.Response,
        test_name: str
    ) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Assert pagination structure and add result.
        
        Args:
            response: HTTP response
            test_name: Name of the test
            
        Returns:
            tuple: (success: bool, parsed_json: Dict or None)
        """
        success, result, body = assert_pagination_structure(response, test_name)
        self.add_result(result)
        return success, body
    
    def assert_field(
        self,
        data: Dict[str, Any],
        field_name: str,
        expected_value: Any,
        test_name: str
    ) -> bool:
        """
        Assert field value and add result.
        
        Args:
            data: Dictionary containing the data
            field_name: Name of the field to check
            expected_value: Expected value
            test_name: Name of the test
            
        Returns:
            True if assertion passed, False otherwise
        """
        result = assert_field_value(data, field_name, expected_value, test_name)
        self.add_result(result)
        return result.ok
    
    def assert_field_is_type(
        self,
        data: Dict[str, Any],
        field_name: str,
        expected_type: type,
        test_name: str
    ) -> bool:
        """
        Assert field type and add result.
        
        Args:
            data: Dictionary containing the data
            field_name: Name of the field to check
            expected_type: Expected type
            test_name: Name of the test
            
        Returns:
            True if assertion passed, False otherwise
        """
        result = assert_field_type(data, field_name, expected_type, test_name)
        self.add_result(result)
        return result.ok
    
    def require_test_data(self, test_name: str, min_count: int = 1) -> bool:
        """
        Check if test data is available.
        Adds a failure result if data is not available.
        
        Args:
            test_name: Name of the test
            min_count: Minimum number of test data items required
            
        Returns:
            True if data is available, False otherwise
        """
        if len(self.test_data) < min_count:
            result = TestResult(test_name)
            result.fail(f"No test data available (need at least {min_count})")
            self.add_result(result)
            return False
        return True
    
    def summary(self) -> bool:
        """
        Print test summary and return success status.
        
        Returns:
            True if all tests passed, False otherwise
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r.ok)
        
        print("\n==== SUMMARY ====")
        for r in self.results:
            print(str(r))
        
        print(f"\n{passed}/{total} tests passed.")
        return passed == total

