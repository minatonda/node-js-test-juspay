"""
Notes API client
"""
from typing import List, Optional, Dict, Any
import requests
import sys
import os

# Add tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base.base_api_client import BaseApiClient


class NotesApiClient(BaseApiClient):
    """
    API client for Notes endpoints.
    Extends BaseApiClient with Notes-specific methods.
    """
    
    def __init__(self, base_url: str):
        """Initialize Notes API client"""
        super().__init__(base_url)
        self.created_notes: List[str] = []  # Track created note IDs
    
    def create_note(
        self,
        title: str,
        body: str,
        tags: Optional[List[str]] = None
    ) -> requests.Response:
        """
        Create a new note.
        
        Args:
            title: Note title
            body: Note body/content
            tags: Optional list of tags
            
        Returns:
            HTTP response
        """
        data: Dict[str, Any] = {
            "title": title,
            "body": body,
        }
        if tags:
            data["tags"] = tags
        return self._post("/notes", data)
    
    def list_notes(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        sortBy: Optional[str] = None,
        sortOrder: Optional[str] = None,
    ) -> requests.Response:
        """
        List notes with pagination and filters.
        
        Args:
            page: Page number
            limit: Items per page
            search: Search keyword
            tags: Filter by tags
            sortBy: Sort field
            sortOrder: Sort order (ASC/DESC)
            
        Returns:
            HTTP response
        """
        params: Dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if limit is not None:
            params["limit"] = limit
        if search:
            params["search"] = search
        if tags:
            params["tags"] = tags
        if sortBy:
            params["sortBy"] = sortBy
        if sortOrder:
            params["sortOrder"] = sortOrder
        return self._get("/notes", params=params)
    
    def get_note(self, note_id: str) -> requests.Response:
        """
        Get a note by ID.
        
        Args:
            note_id: Note UUID
            
        Returns:
            HTTP response
        """
        return self._get(f"/notes/{note_id}")
    
    def update_note(
        self,
        note_id: str,
        title: Optional[str] = None,
        body: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> requests.Response:
        """
        Update a note (partial or complete).
        
        Args:
            note_id: Note UUID
            title: New title (optional)
            body: New body (optional)
            tags: New tags (optional)
            
        Returns:
            HTTP response
        """
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if tags is not None:
            data["tags"] = tags
        return self._patch(f"/notes/{note_id}", data)
    
    def delete_note(self, note_id: str) -> requests.Response:
        """
        Delete a note (soft delete).
        
        Args:
            note_id: Note UUID
            
        Returns:
            HTTP response
        """
        return self._delete(f"/notes/{note_id}")

