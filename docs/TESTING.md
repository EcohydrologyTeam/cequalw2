# Testing Documentation

## Overview

The CE-QUAL-W2 Python library uses pytest for its test suite. All tests are located in the `tests/` directory and follow pytest conventions.

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_datetime.py

# Run a specific test class
pytest tests/test_datetime.py::TestDateTimeUtils

# Run a specific test method
pytest tests/test_datetime.py::TestDateTimeUtils::test_day_of_year_to_date_single_value
```

### Test Coverage

```bash
# Run tests with coverage report
pytest --cov=cequalw2

# Generate HTML coverage report
pytest --cov=cequalw2 --cov-report=html

# View coverage report in browser
open htmlcov/index.html
```

### Test Options

```bash
# Stop on first failure
pytest -x

# Run only tests that match pattern
pytest -k "datetime"

# Show local variables in tracebacks
pytest -l

# Show captured output
pytest -s
```

## Test Structure

### test_datetime.py

Tests for date/time conversion utilities in `cequalw2.utils.datetime`.

#### TestDateTimeUtils

**test_day_of_year_to_date_single_value**
- Tests conversion of a single day-of-year value
- Input: 1.5 (January 1 at noon)
- Expected: datetime(2023, 1, 1, 12, 0)

**test_day_of_year_to_date_multiple_values**
- Tests conversion of multiple values
- Input: [1.0, 32.5, 365.0]
- Expected: Jan 1 00:00, Feb 1 12:00, Dec 31 00:00

**test_day_of_year_to_date_leap_year**
- Tests handling of leap years
- Input: 366.0 in year 2024
- Expected: December 31, 2024

**test_day_of_year_to_date_empty_list**
- Tests edge case of empty input
- Input: []
- Expected: []

### test_io.py

Tests for file I/O operations in `cequalw2.fileio`.

#### TestIOReaders

**test_file_type_enum**
- Verifies FileType enumeration values
- UNKNOWN = 0, FIXED_WIDTH = 1, CSV = 2

**test_get_header_row_number_tsr_file**
- Tests header detection for TSR files
- TSR files should return header row 0
- Case-insensitive detection

**test_get_header_row_number_non_tsr_file**
- Tests header detection for non-TSR files
- Standard files should return header row 2

**test_split_fixed_width_line**
- Tests fixed-width line parsing
- Input: "ABC DEF GHI", width=4
- Expected: ["ABC ", "DEF ", "GHI"]

**test_split_fixed_width_line_exact_width**
- Tests when line length is exact multiple of field width
- Input: "ABCDEFGH", width=4
- Expected: ["ABCD", "EFGH"]

## Writing New Tests

### Test File Structure

```python
import pytest
from cequalw2.module import function_to_test


class TestClassName:
    """Group related tests in a class"""
    
    def test_function_normal_case(self):
        """Test normal expected behavior"""
        result = function_to_test(valid_input)
        assert result == expected_output
    
    def test_function_edge_case(self):
        """Test edge cases"""
        result = function_to_test(edge_input)
        assert result == edge_output
    
    def test_function_error_case(self):
        """Test error handling"""
        with pytest.raises(ExpectedError):
            function_to_test(invalid_input)
```

### Best Practices

1. **Descriptive Names**: Use clear, descriptive test names that explain what is being tested
2. **One Assertion**: Each test should ideally test one thing
3. **Arrange-Act-Assert**: Structure tests with setup, execution, and verification
4. **Test Edge Cases**: Include tests for empty inputs, boundary values, and error conditions
5. **Use Fixtures**: For repeated setup code, use pytest fixtures

### Example Test with Fixture

```python
import pytest
import pandas as pd
from cequalw2.visualization import plot


@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing"""
    return pd.DataFrame({
        'temp': [15.0, 16.0, 17.0],
        'do': [8.0, 7.5, 7.0]
    })


def test_plot_with_sample_data(sample_dataframe):
    """Test plotting with sample data"""
    fig = plot(sample_dataframe)
    assert fig is not None
    assert len(fig.axes) == 1
```

## Continuous Integration

### GitHub Actions

The project can be configured to run tests automatically on push/PR:

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7, 3.8, 3.9, '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
        pip install -e .
    - name: Run tests
      run: pytest --cov=cequalw2
```

## Debugging Tests

### Using pdb

```python
def test_complex_function():
    import pdb; pdb.set_trace()  # Debugger breakpoint
    result = complex_function()
    assert result == expected
```

### Viewing Test Output

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Verbose output with full diff
pytest -vv
```

## Test Data

For tests requiring data files, create a `tests/data/` directory:

```
tests/
├── __init__.py
├── test_datetime.py
├── test_io.py
└── data/
    ├── sample.csv
    ├── sample.npt
    └── sample.db
```

Access test data in tests:

```python
import os

def get_test_data_path(filename):
    """Get path to test data file"""
    return os.path.join(
        os.path.dirname(__file__), 
        'data', 
        filename
    )

def test_read_csv():
    filepath = get_test_data_path('sample.csv')
    df = read_csv(filepath, ['temp', 'do'])
    assert not df.empty
```

## Performance Testing

For performance-critical functions:

```python
import pytest
import time

def test_performance():
    """Ensure function completes within time limit"""
    start = time.time()
    result = expensive_function(large_input)
    duration = time.time() - start
    assert duration < 1.0  # Should complete in under 1 second
```

## Mocking External Dependencies

```python
from unittest.mock import patch, MagicMock

def test_database_function():
    """Test function that uses database"""
    with patch('sqlite3.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        result = function_using_database()
        
        mock_connect.assert_called_once()
        assert result == expected
```