# Notes Service API Tests

Python test suite to validate Notes Service API functionalities.

## Prerequisites

- Python 3.9 or higher
- Notes Service API running (default port 3000)

## Installation

```bash
# Install dependencies
cd tests
pip install -r requirements.txt

# Or use pip3
pip3 install -r requirements.txt
```

## Execution

### Basic Tests

```bash
# Tests on default URL (http://localhost:3000)
python run_tests.py

# Specify API URL
python run_tests.py --base http://localhost:3000
```

### Run with permissions

```bash
chmod +x run_tests.py
./run_tests.py
```

## What is tested

### 1. Note CRUD
- ✓ Create valid note
- ✓ Create note with tags
- ✓ Create note without tags
- ✓ Required field validation
- ✓ Get note by ID
- ✓ Update note (partial)
- ✓ Update note (complete)
- ✓ Delete note (soft delete)
- ✓ Deleted note does not appear in listing

### 2. Listing and Pagination
- ✓ List all notes
- ✓ Pagination (page and limit)
- ✓ Sorting (createdAt, updatedAt, title)
- ✓ Ascending and descending order

### 3. Search
- ✓ Search by keywords in title
- ✓ Search by keywords in content
- ✓ Case-insensitive search

### 4. Filters
- ✓ Filter by tags (single tag)
- ✓ Filter by multiple tags
- ✓ Combination of search and tag filter

### 5. Validations
- ✓ Title too long (should fail)
- ✓ Empty title (should fail)
- ✓ Empty body (should fail)
- ✓ Invalid ID (should return 404)

### 6. Health Check
- ✓ /health endpoint responds correctly

## Test Structure

```
tests/
├── run_tests.py       # Main test script
├── requirements.txt   # Python dependencies
└── README.md         # This documentation
```

## Script Features

### Automatic Data Generation

The script automatically generates:
- **Unique titles**: `Test Note {timestamp}`
- **Random content**: Generated text for each note
- **Random tags**: Tags generated for filter tests

### Test Flow

1. Health check
2. Create valid note
3. Create note with tags
4. Create note without tags
5. Validate required fields
6. Get note by ID
7. List all notes
8. Test pagination
9. Test sorting
10. Search by keywords
11. Filter by tags
12. Combine search and filter
13. Update note (partial)
14. Update note (complete)
15. Delete note
16. Verify soft delete

## Test Output

Tests display:

```
✓ Test name - additional information (if any)
✗ Test name failed - failure reason

==== SUMMARY ====
✓ Test 1
✓ Test 2
✗ Test 3 failed - HTTP 404, body=...

16/16 tests passed.
```

## Execution Example

```bash
$ python run_tests.py --base http://localhost:3000

Base: http://localhost:3000
Starting tests...

✓ Health check responds correctly
✓ Create valid note
✓ Create note with tags
✓ Create note without tags
✓ Validation: empty title → 400
✓ Validation: empty body → 400
✓ Get note by ID
✓ List all notes
✓ Pagination works correctly
✓ Sort by createdAt DESC
✓ Search by keywords in title
✓ Tag filter works
✓ Update note (partial)
✓ Update note (complete)
✓ Delete note (soft delete)
✓ Deleted note does not appear in listing

==== SUMMARY ====
✓ Health check responds correctly
✓ Create valid note
...

16/16 tests passed.
```

## Troubleshooting

### API is not responding

```bash
# Check if API is running
curl http://localhost:3000/health
```

### Installation error

```bash
# Use pip3 instead of pip
pip3 install -r requirements.txt
```

### Permission error

```bash
# Give execution permission
chmod +x run_tests.py
```

## Contributing

To add new tests:

1. Open `run_tests.py`
2. Add a new method in the `Suite` class
3. Call the method in `main()`

Example:

```python
def test_new_feature(self):
    r = self.api.call_endpoint()
    ok = self.assert_status(r, [200], "New feature works")
    return ok
```

## License

UNLICENSED

