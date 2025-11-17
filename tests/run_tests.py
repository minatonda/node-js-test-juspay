#!/usr/bin/env python3
"""
Notes Service API Test Suite (Python) - Refactored with abstractions
--------------------------------------------------------------------
Requirements:
  - Python 3.9+
  - pip install requests

Execution:
  python run_tests_refactored.py --base http://localhost:3000

What is tested:
  ✓ Health check
  ✓ CRUD operations (Create, Read, Update, Delete)
  ✓ Required field validation
  ✓ Pagination
  ✓ Sorting
  ✓ Keyword search
  ✓ Tag filtering
  ✓ Soft delete

Notes:
  - Tests use random data to avoid conflicts with previous data.
  - Validates response structures and HTTP status codes.
  - Uses abstracted patterns for reusability.
"""
import argparse
import sys
import os
from typing import Dict, Any, List, Optional

# Add tests directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.notes_api_client import NotesApiClient
from common.base.base_test_suite import BaseTestSuite
from common.utils.string_util import generate_random_string
from common.utils.json_util import pretty
from common.models.test_result import TestResult
from common.patterns.pagination_test_pattern import PaginationTestPattern


class NotesTestSuite(BaseTestSuite):
    """
    Test suite for Notes API.
    Extends BaseTestSuite with Notes-specific tests.
    """
    
    def __init__(self, api: NotesApiClient):
        """Initialize Notes test suite"""
        super().__init__(api)
        # Use test_data from base class (alias for convenience)
        self.test_notes = self.test_data
    
    def test_health_check(self):
        """Test health check endpoint"""
        r = self.api.health_check()
        ok = self.assert_status(r, [200], "Health check responds correctly")
        if ok:
            success, body = self.assert_json(
                r,
                "Health check returns valid JSON",
                required_fields=["status"]
            )
        return ok
    
    def test_create_valid_note(self):
        """Test creating a valid note"""
        title = f"Test Note {generate_random_string(8)}"
        body = "This is the test note content."
        r = self.api.create_note(title, body)
        ok = self.assert_status(r, [200, 201], "Create valid note")
        if ok:
            success, body_resp = self.assert_json(
                r,
                "Create note returns valid JSON",
                required_fields=["id"]
            )
            if success and body_resp and "id" in body_resp:
                self.test_notes.append({
                    "id": body_resp["id"],
                    "title": title,
                    "body": body,
                })
                self.api.created_notes.append(body_resp["id"])
        return ok
    
    def test_create_note_with_tags(self):
        """Test creating a note with tags"""
        title = f"Note with Tags {generate_random_string(8)}"
        body = "Note content with tags."
        tags = ["work", "important", "urgent"]
        r = self.api.create_note(title, body, tags)
        ok = self.assert_status(r, [200, 201], "Create note with tags")
        if ok:
            success, body_resp = self.assert_json(
                r,
                "Create note with tags returns valid JSON",
                required_fields=["id"]
            )
            if success and body_resp and "id" in body_resp:
                self.test_notes.append({
                    "id": body_resp["id"],
                    "title": title,
                    "body": body,
                    "tags": tags,
                })
                self.api.created_notes.append(body_resp["id"])
                # Check if tags were saved correctly
                received_tags = body_resp.get("tags")
                if not self.assert_field_is_type(
                    body_resp,
                    "tags",
                    list,
                    "Tags were saved correctly"
                ):
                    # Additional check for tag values
                    if isinstance(received_tags, list) and received_tags != tags:
                        result = TestResult("Tags match expected values")
                        result.fail(f"Expected {tags}, obtained {received_tags}")
                        self.add_result(result)
        return ok
    
    def test_create_note_without_tags(self):
        """Test creating a note without tags"""
        title = f"Note without Tags {generate_random_string(8)}"
        body = "Note content without tags."
        r = self.api.create_note(title, body)
        ok = self.assert_status(r, [200, 201], "Create note without tags")
        if ok:
            success, body_resp = self.assert_json(
                r,
                "Create note without tags returns valid JSON",
                required_fields=["id"]
            )
            if success and body_resp and "id" in body_resp:
                self.test_notes.append({
                    "id": body_resp["id"],
                    "title": title,
                    "body": body,
                })
                self.api.created_notes.append(body_resp["id"])
        return ok
    
    def test_validation_empty_title(self):
        """Test validation: empty title"""
        r = self.api.create_note("", "Valid content")
        return self.assert_status(r, [400, 422], "Validation: empty title → 400")
    
    def test_validation_empty_body(self):
        """Test validation: empty body"""
        r = self.api.create_note("Valid title", "")
        return self.assert_status(r, [400, 422], "Validation: empty body → 400")
    
    def test_validation_title_too_long(self):
        """Test validation: title too long"""
        title = "A" * 300  # More than 255 characters
        r = self.api.create_note(title, "Valid content")
        return self.assert_status(r, [400, 422], "Validation: title too long → 400")
    
    def test_get_note_by_id(self):
        """Test getting a note by ID"""
        if not self.require_test_data("Get note by ID"):
            return False
        
        note_id = self.test_notes[0]["id"]
        r = self.api.get_note(note_id)
        ok = self.assert_status(r, [200], "Get note by ID")
        if ok:
            success, body = self.assert_json(
                r,
                "Returned note contains required fields",
                required_fields=["id", "title", "body"]
            )
        return ok
    
    def test_get_note_invalid_id(self):
        """Test getting a note with invalid ID"""
        invalid_id = "00000000-0000-0000-0000-000000000000"
        r = self.api.get_note(invalid_id)
        return self.assert_status(r, [404], "Get note with invalid ID → 404")
    
    def test_list_all_notes(self):
        """Test listing all notes"""
        r = self.api.list_notes()
        ok = self.assert_status(r, [200], "List all notes")
        if ok:
            success, body = self.assert_pagination(r, "List returns correct structure")
        return ok
    
    def test_pagination(self):
        """Test pagination functionality"""
        def list_with_params(params: Dict[str, Any]):
            return self.api.list_notes(
                page=params.get("page"),
                limit=params.get("limit")
            )
        
        success, body = PaginationTestPattern.test_pagination_params(
            list_with_params,
            page=1,
            limit=2,
            test_name="Pagination works correctly"
        )
        
        if success:
            result = TestResult("Pagination works correctly")
            self.add_result(result)
        else:
            result = TestResult("Pagination works correctly")
            result.fail("Pagination test failed")
            self.add_result(result)
        
        return success
    
    def test_sorting(self):
        """Test sorting functionality"""
        r = self.api.list_notes(sortBy="createdAt", sortOrder="DESC")
        ok = self.assert_status(r, [200], "Sort by createdAt DESC")
        if ok:
            success, body = self.assert_pagination(r, "Sorting returns paginated response")
            if success and body:
                items = body.get("items", [])
                if len(items) >= 2:
                    dates = [item.get("createdAt") for item in items if item.get("createdAt")]
                    result = TestResult("DESC sorting works correctly")
                    if dates != sorted(dates, reverse=True):
                        result.fail("Items are not sorted correctly")
                    self.add_result(result)
        return ok
    
    def test_search_by_keywords(self):
        """Test search by keywords"""
        if not self.require_test_data("Search by keywords in title"):
            return False
        
        # Search by the first note's title
        search_term = self.test_notes[0]["title"].split()[0]  # First word of title
        r = self.api.list_notes(search=search_term)
        ok = self.assert_status(r, [200], "Search by keywords in title")
        if ok:
            success, body = self.assert_pagination(r, "Search returns paginated response")
            if success and body:
                items = body.get("items", [])
                result = TestResult("Search returns relevant results")
                if len(items) == 0:
                    result.fail("Search did not return results")
                self.add_result(result)
        return ok
    
    def test_filter_by_tags(self):
        """Test filtering by tags"""
        if not any(note.get("tags") for note in self.test_notes):
            result = TestResult("Tag filter works")
            result.fail("No note with tags created previously")
            self.add_result(result)
            return False
        
        # Find a note with tags
        note_with_tags = next((n for n in self.test_notes if n.get("tags")), None)
        if not note_with_tags:
            result = TestResult("Tag filter works")
            result.fail("No note with tags found")
            self.add_result(result)
            return False
        
        tag = note_with_tags["tags"][0]
        r = self.api.list_notes(tags=[tag])
        ok = self.assert_status(r, [200], "Tag filter works")
        if ok:
            success, body = self.assert_pagination(r, "Tag filter returns paginated response")
            if success and body:
                items = body.get("items", [])
                result = TestResult("Filter returns notes with the tag")
                if len(items) == 0:
                    result.fail("Filter did not return results")
                else:
                    # Check if at least one note has the tag
                    found = any(tag in item.get("tags", []) for item in items)
                    if not found:
                        result.fail("No returned note contains the filtered tag")
                self.add_result(result)
        return ok
    
    def test_search_and_filter_combined(self):
        """Test combination of search and tag filter"""
        if not self.require_test_data("Combination of search and tag filter"):
            return False
        
        r = self.api.list_notes(search="test", tags=["work"])
        return self.assert_status(r, [200], "Combination of search and tag filter")
    
    def test_update_note_partial(self):
        """Test partial note update"""
        if not self.require_test_data("Update note (partial)"):
            return False
        
        note_id = self.test_notes[0]["id"]
        new_title = f"Updated Title {generate_random_string(6)}"
        r = self.api.update_note(note_id, title=new_title)
        ok = self.assert_status(r, [200], "Update note (partial)")
        if ok:
            success, body = self.assert_json(r, "Update returns valid JSON")
            if success and body:
                self.assert_field(body, "title", new_title, "Title was updated correctly")
        return ok
    
    def test_update_note_complete(self):
        """Test complete note update"""
        if not self.require_test_data("Update note (complete)"):
            return False
        
        note_id = self.test_notes[-1]["id"] if len(self.test_notes) > 1 else self.test_notes[0]["id"]
        new_title = f"Complete Title {generate_random_string(6)}"
        new_body = "Content completely updated."
        new_tags = ["updated", "complete"]
        r = self.api.update_note(note_id, title=new_title, body=new_body, tags=new_tags)
        ok = self.assert_status(r, [200], "Update note (complete)")
        if ok:
            success, body = self.assert_json(r, "Update returns valid JSON")
            if success and body:
                result = TestResult("All fields were updated")
                if (body.get("title") != new_title or
                    body.get("body") != new_body or
                    body.get("tags") != new_tags):
                    result.fail("Some fields were not updated correctly")
                self.add_result(result)
        return ok
    
    def test_delete_note(self):
        """Test note deletion (soft delete)"""
        if not self.require_test_data("Delete note (soft delete)"):
            return False
        
        # Use the last created note
        note_id = self.test_notes[-1]["id"]
        r = self.api.delete_note(note_id)
        return self.assert_status(r, [200], "Delete note (soft delete)")
    
    def test_deleted_note_not_in_listing(self):
        """Test that deleted note doesn't appear in listing"""
        if not self.require_test_data("Deleted note does not appear in listing"):
            return False
        
        # The last note was deleted in the previous test
        deleted_note_id = self.test_notes[-1]["id"]
        r = self.api.list_notes()
        ok = self.assert_status(r, [200], "List notes after deletion")
        if ok:
            success, body = self.assert_pagination(r, "List returns paginated response")
            if success and body:
                items = body.get("items", [])
                result = TestResult("Deleted note does not appear in listing")
                found = any(item.get("id") == deleted_note_id for item in items)
                if found:
                    result.fail("Deleted note still appears in listing")
                self.add_result(result)
        return ok
    
    def test_get_deleted_note(self):
        """Test that getting deleted note returns 404"""
        if not self.require_test_data("Get deleted note returns 404"):
            return False
        
        # The last note was deleted
        deleted_note_id = self.test_notes[-1]["id"]
        r = self.api.get_note(deleted_note_id)
        return self.assert_status(r, [404], "Get deleted note returns 404")


def main():
    """Main test execution"""
    ap = argparse.ArgumentParser(description="Tests for Notes Service API")
    ap.add_argument("--base", default="http://localhost:3000", help="API base URL")
    args = ap.parse_args()
    
    print(f"Base: {args.base}")
    print("Starting tests...\n")
    
    api = NotesApiClient(args.base)
    suite = NotesTestSuite(api)
    
    # Test order
    suite.test_health_check()
    
    suite.test_create_valid_note()
    suite.test_create_note_with_tags()
    suite.test_create_note_without_tags()
    
    suite.test_validation_empty_title()
    suite.test_validation_empty_body()
    suite.test_validation_title_too_long()
    
    suite.test_get_note_by_id()
    suite.test_get_note_invalid_id()
    
    suite.test_list_all_notes()
    suite.test_pagination()
    suite.test_sorting()
    
    suite.test_search_by_keywords()
    suite.test_filter_by_tags()
    suite.test_search_and_filter_combined()
    
    suite.test_update_note_partial()
    suite.test_update_note_complete()
    
    suite.test_delete_note()
    suite.test_deleted_note_not_in_listing()
    suite.test_get_deleted_note()
    
    ok = suite.summary()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

