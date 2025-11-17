"""
Pagination test pattern utilities
"""
from typing import Callable, Dict, Any, Optional, List
import requests
import sys
import os

# Add tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from common.models.test_result import TestResult
from common.assertions.response_assertions import assert_status_code, assert_pagination_structure, assert_field_value


class PaginationTestPattern:
    """
    Utilities for testing pagination functionality.
    """
    
    @staticmethod
    def test_pagination_structure(
        list_func: Callable[[Dict[str, Any]], requests.Response],
        params: Optional[Dict[str, Any]] = None,
        test_name: str = "Pagination structure is correct"
    ) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Test that list endpoint returns correct pagination structure.
        
        Args:
            list_func: Function that lists resources
            params: Query parameters
            test_name: Name of the test
            
        Returns:
            tuple: (success: bool, response_body: Dict or None)
        """
        response = list_func(params or {})
        success, result, body = assert_pagination_structure(response, test_name)
        return success, body
    
    @staticmethod
    def test_pagination_params(
        list_func: Callable[[Dict[str, Any]], requests.Response],
        page: int,
        limit: int,
        test_name: str = "Pagination parameters work correctly"
    ) -> tuple[bool, Optional[Dict[str, Any]]]:
        """
        Test pagination with specific page and limit.
        
        Args:
            list_func: Function that lists resources
            page: Page number
            limit: Items per page
            test_name: Name of the test
            
        Returns:
            tuple: (success: bool, response_body: Dict or None)
        """
        params = {"page": page, "limit": limit}
        response = list_func(params)
        result = assert_status_code(response, [200], test_name)
        
        if not result.ok:
            return False, None
        
        success, pagination_result, body = assert_pagination_structure(
            response,
            f"{test_name} - structure"
        )
        
        if not success:
            return False, None
        
        # Verify pagination parameters
        limit_result = assert_field_value(body, "limit", limit, f"{test_name} - limit")
        page_result = assert_field_value(body, "page", page, f"{test_name} - page")
        
        # Check items count
        items = body.get("items", [])
        if len(items) > limit:
            limit_result.fail(f"Returned items ({len(items)}) greater than limit ({limit})")
        
        all_ok = limit_result.ok and page_result.ok
        
        return all_ok, body
    
    @staticmethod
    def test_pagination_page_count(
        list_func: Callable[[Dict[str, Any]], requests.Response],
        test_name: str = "Pagination page count is correct"
    ) -> bool:
        """
        Test that pageCount is calculated correctly.
        
        Args:
            list_func: Function that lists resources
            test_name: Name of the test
            
        Returns:
            True if successful, False otherwise
        """
        # Get first page to know total
        params = {"page": 1, "limit": 10}
        response = list_func(params)
        success, result, body = assert_pagination_structure(response, test_name)
        
        if not success:
            return False
        
        total = body.get("total", 0)
        limit = body.get("limit", 10)
        page_count = body.get("pageCount", 0)
        expected_page_count = (total + limit - 1) // limit if limit > 0 else 0
        
        result = assert_field_value(
            body,
            "pageCount",
            expected_page_count,
            f"{test_name} - calculation"
        )
        
        return result.ok

