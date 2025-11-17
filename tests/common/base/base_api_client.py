"""
Base API client for HTTP requests
"""
import requests
from typing import Dict, Any, List, Optional


class BaseApiClient:
    """
    Base class for API clients.
    Provides common HTTP request functionality.
    """
    
    def __init__(self, base_url: str):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL of the API (e.g., "http://localhost:3000")
        """
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.created_resources: List[str] = []  # Track created resource IDs
    
    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make GET request"""
        return self.session.get(f"{self.base}{endpoint}", params=params)
    
    def _post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make POST request"""
        return self.session.post(f"{self.base}{endpoint}", json=data)
    
    def _patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Make PATCH request"""
        return self.session.patch(f"{self.base}{endpoint}", json=data)
    
    def _delete(self, endpoint: str) -> requests.Response:
        """Make DELETE request"""
        return self.session.delete(f"{self.base}{endpoint}")
    
    def health_check(self, endpoint: str = "/health") -> requests.Response:
        """
        Check API health.
        
        Args:
            endpoint: Health check endpoint (default: "/health")
            
        Returns:
            HTTP response
        """
        return self._get(endpoint)

