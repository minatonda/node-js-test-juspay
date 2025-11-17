# Test Common Abstractions

This directory contains reusable abstractions and utilities for API testing, following the same principles used in the API codebase.

## 📁 Structure

```
common/
├── base/                          # Base classes
│   ├── base_api_client.py        # Base API client with HTTP methods
│   └── base_test_suite.py        # Base test suite with common utilities
├── models/                        # Data models
│   └── test_result.py            # Test result model
├── assertions/                    # Assertion utilities
│   └── response_assertions.py    # HTTP response assertions
├── patterns/                      # Test patterns
│   ├── crud_test_pattern.py      # CRUD test pattern
│   └── pagination_test_pattern.py # Pagination test pattern
└── utils/                         # Utility functions
    ├── json_util.py               # JSON utilities
    └── string_util.py             # String generation utilities
```

## 🏗️ Abstractions

### 1. Base API Client (`base/base_api_client.py`)

Base class for API clients providing common HTTP request functionality.

**Features:**
- Session management
- Common HTTP methods (GET, POST, PATCH, DELETE)
- Resource tracking
- Health check method

**Usage:**
```python
from common.base.base_api_client import BaseApiClient

class MyApiClient(BaseApiClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
    
    def my_endpoint(self):
        return self._get("/my-endpoint")
```

### 2. Base Test Suite (`base/base_test_suite.py`)

Base class for test suites with common test utilities and result tracking.

**Features:**
- Test result management
- Common assertions (status, JSON, pagination, fields)
- Test data management
- Summary generation

**Usage:**
```python
from common.base.base_test_suite import BaseTestSuite

class MyTestSuite(BaseTestSuite):
    def __init__(self, api_client):
        super().__init__(api_client)
    
    def test_something(self):
        r = self.api.my_endpoint()
        ok = self.assert_status(r, [200], "Test name")
        if ok:
            success, body = self.assert_json(r, "Valid JSON", ["id"])
```

### 3. Test Result Model (`models/test_result.py`)

Model for tracking test outcomes.

**Features:**
- Success/failure tracking
- Error messages
- String representation

**Usage:**
```python
from common.models.test_result import TestResult

result = TestResult("Test name")
result.fail("Error message")
# or
result.success("Success message")
```

### 4. Response Assertions (`assertions/response_assertions.py`)

Utilities for asserting HTTP response properties.

**Functions:**
- `assert_status_code()`: Assert HTTP status code
- `assert_json_structure()`: Assert JSON structure and required fields
- `assert_pagination_structure()`: Assert pagination structure
- `assert_field_value()`: Assert field value
- `assert_field_type()`: Assert field type

**Usage:**
```python
from common.assertions.response_assertions import assert_status_code, assert_json_structure

result = assert_status_code(response, [200, 201], "Test name")
success, result, body = assert_json_structure(response, "Test", ["id", "name"])
```

### 5. CRUD Test Pattern (`patterns/crud_test_pattern.py`)

Utilities for testing CRUD operations.

**Methods:**
- `test_create()`: Test create operation
- `test_read()`: Test read operation
- `test_update()`: Test update operation
- `test_delete()`: Test delete operation
- `test_not_found()`: Test 404 for invalid IDs

**Usage:**
```python
from common.patterns.crud_test_pattern import CrudTestPattern

success, resource = CrudTestPattern.test_create(
    create_func=lambda data: api.create(data),
    test_data={"name": "Test"},
    test_name="Create resource"
)
```

### 6. Pagination Test Pattern (`patterns/pagination_test_pattern.py`)

Utilities for testing pagination functionality.

**Methods:**
- `test_pagination_structure()`: Test pagination structure
- `test_pagination_params()`: Test pagination with specific params
- `test_pagination_page_count()`: Test page count calculation

**Usage:**
```python
from common.patterns.pagination_test_pattern import PaginationTestPattern

success, body = PaginationTestPattern.test_pagination_params(
    list_func=lambda params: api.list(params),
    page=1,
    limit=10,
    test_name="Pagination test"
)
```

### 7. JSON Utilities (`utils/json_util.py`)

Utilities for JSON operations.

**Functions:**
- `pretty()`: Pretty print JSON
- `safe_json_parse()`: Safely parse JSON
- `get_json_or_none()`: Get JSON from response or None

### 8. String Utilities (`utils/string_util.py`)

Utilities for string generation.

**Functions:**
- `generate_random_string()`: Generate random string
- `generate_unique_identifier()`: Generate UUID

## 📦 Benefits

1. **Consistency**: All tests follow the same patterns
2. **Reusability**: Utilities can be used across all test suites
3. **Maintainability**: Changes in one place affect all tests
4. **Less Code**: Reduced duplication and boilerplate
5. **Type Safety**: Strong typing throughout
6. **Better Organization**: Clear separation of concerns
7. **Easier Testing**: Simple APIs for common operations
8. **Scalability**: Easy to add new test suites following the same patterns

## 🔄 How to Use in New Test Suites

When creating a new test suite:

1. **API Client**: Extend `BaseApiClient` with endpoint-specific methods
2. **Test Suite**: Extend `BaseTestSuite` with test methods
3. **Assertions**: Use assertion utilities from `assertions/`
4. **Patterns**: Use test patterns from `patterns/` for common operations
5. **Utilities**: Use utilities from `utils/` for data generation and JSON handling

## 📝 Example: Complete Test Suite

```python
from api.notes_api_client import NotesApiClient
from common.base.base_test_suite import BaseTestSuite
from common.utils.string_util import generate_random_string

class NotesTestSuite(BaseTestSuite):
    def __init__(self, api: NotesApiClient):
        super().__init__(api)
        self.test_notes = []
    
    def test_create_note(self):
        title = f"Test {generate_random_string(8)}"
        r = self.api.create_note(title, "Body")
        ok = self.assert_status(r, [200, 201], "Create note")
        if ok:
            success, body = self.assert_json(r, "Valid JSON", ["id"])
            if success:
                self.test_notes.append(body)
        return ok
```

## 🎯 Alignment with API Patterns

These abstractions mirror the patterns used in the API:

- **Base Classes**: Similar to `BaseEntity` and `SoftDeletableEntity`
- **Utilities**: Similar to `pagination.util.ts` and `soft-delete.util.ts`
- **Patterns**: Similar to reusable DTOs and service patterns
- **Models**: Similar to entity models

This ensures consistency between API implementation and testing.

