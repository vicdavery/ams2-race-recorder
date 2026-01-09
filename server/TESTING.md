# Testing Guide for AMS2 Web Server

Complete guide for running tests and understanding the test coverage.

## Overview

The test suite uses pytest and includes:
- **Route tests**: HTML page rendering and navigation
- **API tests**: REST endpoint validation
- **Database tests**: Data access and integrity
- **Integration tests**: End-to-end workflows

## Test Data

The tests use fixture data that includes:
- 3 test sessions (2 qualifying, 1 race)
- 3 test drivers (Alice Johnson, Bob Smith, Charlie Brown)
- 9 race results with F1 2024 points
- Pole position and fastest lap tracking

All data is temporary and created in-memory for each test run.

## Running Tests

### Option 1: Using Test Script (Recommended)

#### On Windows:
```bash
cd server
run_tests.bat
```

#### On Linux/Mac:
```bash
cd server
bash run_tests.sh
```

### Option 2: Using pytest Directly

#### Setup first:
```bash
cd server
bash setup.sh                # Linux/Mac
# or
setup.bat                    # Windows
```

#### Run tests:
```bash
source venv/bin/activate     # Linux/Mac
# or
venv\Scripts\activate.bat    # Windows

pytest -v
```

### Option 3: Run Specific Test

```bash
# Run a single test file
pytest tests/test_routes.py -v

# Run a specific test class
pytest tests/test_routes.py::TestIndexRoute -v

# Run a specific test
pytest tests/test_routes.py::TestIndexRoute::test_index_page_loads -v
```

## Test Organization

### test_routes.py
Tests for HTML page rendering and user interface:
- **TestIndexRoute**: Home page and session listing
- **TestSessionRoute**: Session detail pages
- **TestDriverRoute**: Driver profile pages
- **TestHealthRoute**: Health check endpoint
- **TestNotFoundRoute**: 404 error handling

### test_api.py
Tests for REST API endpoints:
- **TestSessionsAPI**: Get all sessions endpoint
- **TestSessionDetailAPI**: Session detail API
- **TestDriversAPI**: Get all drivers endpoint
- **TestDriverStatsAPI**: Driver statistics API
- **TestStandingsAPI**: Championship standings API
- **TestAPIResponseFormat**: Response format validation

### test_database.py
Tests for database operations:
- **TestDatabaseConnection**: Connection validation
- **TestGetSessions**: Session queries
- **TestGetSessionResults**: Results retrieval
- **TestGetDriverStats**: Statistics calculation
- **TestLapTimeFormatting**: Time format conversion
- **TestDatabaseIntegrity**: Data consistency

## Test Coverage

Current test coverage includes:

### Routes (15 tests)
- Index page loads and displays sessions
- Session detail pages with results
- Driver profile pages with statistics
- Error handling (404 pages)
- Page metadata and navigation

### API (22 tests)
- Sessions endpoint returns all sessions
- Session detail endpoint with results
- Drivers list endpoint
- Driver statistics endpoint
- Championship standings endpoint
- Response format validation (JSON)
- Error response format

### Database (18 tests)
- Database connections
- Session queries and limits
- Session results retrieval
- Driver statistics calculations
- Lap time formatting
- Foreign key integrity
- No orphaned records

**Total: 55 tests**

## Test Data Details

### Sessions

**Session 1: Qualifying at Silverstone**
- Type: Qualifying
- Track: Silverstone
- Date: 2025-01-09 14:30:00
- 3 participants

**Session 2: Race at Silverstone**
- Type: Race
- Track: Silverstone
- Date: 2025-01-09 15:00:00
- 3 participants
- F1 points awarded (25, 18, 15)

**Session 3: Race at Spa-Francorchamps**
- Type: Race
- Track: Spa-Francorchamps
- Date: 2025-01-10 14:00:00
- 3 participants
- F1 points awarded (25, 18, 15)

### Drivers

**Alice Johnson**
- 3 races
- 43 total points (25 + 18 = 43)
- 1 pole position
- 0 fastest laps
- Average finish: 1.67

**Bob Smith**
- 3 races
- 33 total points (18 + 15 = 33)
- 0 poles
- 1 fastest lap
- Average finish: 2.33

**Charlie Brown**
- 3 races
- 40 total points (15 + 25 = 40)
- 1 pole position
- 1 fastest lap
- Average finish: 1.67

## Expected Test Results

When all tests pass, you should see:

```
test_routes.py::TestIndexRoute::test_index_page_loads PASSED
test_routes.py::TestIndexRoute::test_index_displays_sessions PASSED
test_routes.py::TestIndexRoute::test_index_shows_session_types PASSED
...
test_database.py::TestDatabaseIntegrity::test_no_orphaned_records PASSED

======================== 55 passed in 2.34s ========================
```

## Troubleshooting Tests

### Virtual Environment Issues
If pytest is not found:
```bash
# Recreate venv
rm -rf venv
bash setup.sh
bash run_tests.sh
```

### Import Errors
Ensure you're running from the `server` directory:
```bash
cd /path/to/ams2/server
bash run_tests.sh
```

### Port Conflicts
If Flask test client fails:
- Make sure no other Flask server is running on port 5000
- Tests use an in-memory database, so conflicts shouldn't occur

### Database Locked
If you see database locked errors:
- Tests create temporary databases
- This shouldn't happen, but close any other database connections

## Adding New Tests

To add tests for new features:

1. **Create test file** in `tests/` directory:
```python
# tests/test_new_feature.py
import pytest

class TestNewFeature:
    def test_something(self, client):
        response = client.get('/new-endpoint')
        assert response.status_code == 200
```

2. **Run your new test**:
```bash
pytest tests/test_new_feature.py -v
```

3. **Add to fixtures** in `conftest.py` if needed

## Best Practices

1. **Use descriptive names**: Test names should describe what is being tested
2. **One assertion per test**: Each test should focus on one thing
3. **Use fixtures**: Share setup code via conftest.py fixtures
4. **Test edge cases**: Include tests for errors and boundary conditions
5. **Keep tests fast**: In-memory databases are used to speed up tests

## Performance

Tests typically complete in under 5 seconds on modern hardware:
- Database setup: ~100ms
- 55 tests: ~4 seconds
- Total: ~4.1 seconds

## Continuous Integration

To run tests in CI/CD:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests with coverage
pytest --cov=app tests/

# Exit with status code
pytest --tb=short
```

## Common Issues and Solutions

### Import errors in tests
**Problem**: `ModuleNotFoundError: No module named 'app'`
**Solution**: Ensure conftest.py is in the server directory

### Test database path issues
**Problem**: Tests fail with database path errors
**Solution**: Tests use temporary files; clean up with `rm -f *.db`

### Flask app already running
**Problem**: Port 5000 already in use
**Solution**: Tests use test client, not actual port; close Flask servers

## Support

For test-related issues:
1. Check this TESTING.md file
2. Review pytest documentation: https://docs.pytest.org/
3. Check Flask testing docs: https://flask.palletsprojects.com/testing/
4. Examine conftest.py for fixture setup
