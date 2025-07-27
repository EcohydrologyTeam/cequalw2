Testing Guide
=============

This guide covers testing practices for the CE-QUAL-W2 Python Library.

.. note::
   For detailed testing information and examples, see the 
   `TESTING.md <https://github.com/ecohydrology/cequalw2-Claude/blob/main/docs/TESTING.md>`_ 
   file in the documentation directory.

Overview
--------

The CE-QUAL-W2 Python Library uses pytest as its testing framework. The test suite is designed to:

* Ensure all functions work correctly with various inputs
* Validate data integrity and conversion accuracy
* Test file I/O operations with different formats
* Verify visualization functionality
* Check error handling and edge cases

Test Structure
--------------

The test suite is organized in the ``tests/`` directory:

.. code-block:: text

    tests/
    ├── test_datetime.py          # Date/time conversion tests
    ├── test_fileio.py           # File I/O operations tests
    ├── test_visualization.py    # Plotting and visualization tests
    ├── test_analysis.py         # Analysis and statistics tests
    ├── test_integration.py      # Integration tests
    ├── fixtures/                # Test data files
    │   ├── sample_csv.csv
    │   ├── sample_npt.npt
    │   └── sample_excel.xlsx
    └── conftest.py              # Pytest configuration and fixtures

Running Tests
-------------

Basic Test Execution
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Run all tests
    pytest

    # Run with verbose output
    pytest -v

    # Run specific test file
    pytest tests/test_datetime.py

    # Run specific test function
    pytest tests/test_datetime.py::test_single_day_conversion

Test Coverage
~~~~~~~~~~~~~

.. code-block:: bash

    # Run tests with coverage report
    pytest --cov=cequalw2

    # Generate HTML coverage report
    pytest --cov=cequalw2 --cov-report=html

    # View coverage in browser
    open htmlcov/index.html

Performance Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Run performance tests only
    pytest -m performance

    # Run with timing information
    pytest --durations=10

Test Categories
---------------

Unit Tests
~~~~~~~~~~

Test individual functions in isolation:

.. code-block:: python

    # test_datetime.py
    import pytest
    import datetime
    from cequalw2.utils import day_of_year_to_date, round_time

    class TestDateConversion:
        """Test date conversion utilities."""
        
        def test_single_day_conversion(self):
            """Test conversion of single day-of-year value."""
            dates = day_of_year_to_date(2023, [1.0])
            expected = datetime.datetime(2023, 1, 1, 0, 0)
            assert dates[0] == expected
        
        def test_fractional_day_conversion(self):
            """Test conversion with fractional day (time)."""
            dates = day_of_year_to_date(2023, [1.5])
            expected = datetime.datetime(2023, 1, 1, 12, 0)
            assert dates[0] == expected
        
        def test_leap_year_handling(self):
            """Test proper leap year handling."""
            # Day 366 should work in leap year
            dates = day_of_year_to_date(2024, [366.0])
            expected = datetime.datetime(2024, 12, 31, 0, 0)
            assert dates[0] == expected
        
        def test_invalid_day_error(self):
            """Test error handling for invalid day values."""
            with pytest.raises(ValueError):
                day_of_year_to_date(2023, [367.0])  # Too high for regular year

Integration Tests
~~~~~~~~~~~~~~~~~

Test complete workflows:

.. code-block:: python

    # test_integration.py
    import tempfile
    import os
    import pandas as pd
    from cequalw2.fileio import read, write_csv
    from cequalw2.visualization import plot
    
    class TestWorkflowIntegration:
        """Test complete analysis workflows."""
        
        def test_csv_roundtrip(self):
            """Test reading and writing CSV files."""
            # Create sample data
            data = pd.DataFrame({
                'temperature': [15.0, 16.0, 17.0],
                'do': [8.0, 7.5, 7.0]
            }, index=pd.date_range('2023-01-01', periods=3, freq='D'))
            
            with tempfile.TemporaryDirectory() as tmpdir:
                # Write data
                filepath = os.path.join(tmpdir, 'test.csv')
                write_csv(data, filepath, year=2023)
                
                # Read data back
                read_data = read(filepath, year=2023, 
                               data_columns=['temperature', 'do'])
                
                # Verify data integrity
                pd.testing.assert_frame_equal(data, read_data, check_exact=False)
        
        def test_plotting_workflow(self):
            """Test complete plotting workflow."""
            # Sample data
            data = pd.DataFrame({
                'temp': [15, 16, 17, 18],
                'do': [8, 7.5, 7, 6.5]
            }, index=pd.date_range('2023-01-01', periods=4, freq='D'))
            
            # Should not raise any exceptions
            fig = plot(data, ylabel='Test Parameters')
            assert fig is not None
            
            # Clean up
            plt.close(fig)

Fixture Examples
----------------

Common Test Data
~~~~~~~~~~~~~~~~

.. code-block:: python

    # conftest.py
    import pytest
    import pandas as pd
    import tempfile
    import os

    @pytest.fixture
    def sample_data():
        """Create sample water quality data."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        data = pd.DataFrame({
            'temperature': 15 + 10 * np.sin(np.arange(100) * 2 * np.pi / 365),
            'dissolved_oxygen': 8 + 2 * np.cos(np.arange(100) * 2 * np.pi / 365),
            'ph': 7.5 + 0.5 * np.random.normal(0, 1, 100)
        }, index=dates)
        return data

    @pytest.fixture
    def temp_csv_file(sample_data):
        """Create temporary CSV file with sample data."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', 
                                       delete=False) as f:
            # Write CE-QUAL-W2 style header
            f.write("CE-QUAL-W2 Test Data\n")
            f.write("Generated for testing\n")
            f.write("Day,Temperature,DO,pH\n")
            
            # Write data with day-of-year format
            for i, (date, row) in enumerate(sample_data.iterrows()):
                day_of_year = date.timetuple().tm_yday
                f.write(f"{day_of_year},{row['temperature']:.2f},"
                       f"{row['dissolved_oxygen']:.2f},{row['ph']:.2f}\n")
            
            yield f.name
            
        # Cleanup
        os.unlink(f.name)

Parameterized Tests
~~~~~~~~~~~~~~~~~~~

Test multiple scenarios efficiently:

.. code-block:: python

    import pytest

    @pytest.mark.parametrize("year,expected_days", [
        (2023, 365),  # Regular year
        (2024, 366),  # Leap year
        (2000, 366),  # Leap year (divisible by 400)
        (1900, 365),  # Not leap year (divisible by 100, not 400)
    ])
    def test_year_length(year, expected_days):
        """Test correct handling of different year lengths."""
        max_day = expected_days
        dates = day_of_year_to_date(year, [max_day])
        assert dates[0].year == year
        assert dates[0].month == 12
        assert dates[0].day == 31

    @pytest.mark.parametrize("file_extension,expected_type", [
        ('.csv', 'CSV'),
        ('.npt', 'FIXED_WIDTH'),
        ('.opt', 'FIXED_WIDTH'),
        ('.xlsx', 'EXCEL'),
        ('.db', 'SQLITE'),
    ])
    def test_file_type_detection(file_extension, expected_type):
        """Test automatic file type detection."""
        from cequalw2.fileio import detect_file_type
        
        filename = f"test{file_extension}"
        detected_type = detect_file_type(filename)
        assert detected_type.value == expected_type

Error Handling Tests
--------------------

Testing Exception Cases
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class TestErrorHandling:
        """Test error handling and edge cases."""
        
        def test_file_not_found(self):
            """Test handling of missing files."""
            with pytest.raises(FileNotFoundError):
                read('nonexistent_file.csv', year=2023, data_columns=['temp'])
        
        def test_invalid_year(self):
            """Test handling of invalid year values."""
            with pytest.raises(ValueError):
                day_of_year_to_date(-1, [1.0])
        
        def test_empty_data_columns(self):
            """Test handling of empty column list."""
            with pytest.raises(ValueError):
                read('sample.csv', year=2023, data_columns=[])
        
        def test_missing_columns(self, temp_csv_file):
            """Test handling of missing columns in file."""
            with pytest.raises(KeyError):
                read(temp_csv_file, year=2023, 
                     data_columns=['nonexistent_column'])

Performance Tests
-----------------

Benchmarking Critical Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    import numpy as np

    @pytest.mark.performance
    class TestPerformance:
        """Performance tests for critical functions."""
        
        def test_large_date_conversion_performance(self):
            """Test performance of date conversion with large datasets."""
            # Create large dataset
            large_day_values = np.linspace(1, 365, 100000).tolist()
            
            start_time = time.time()
            dates = day_of_year_to_date(2023, large_day_values)
            end_time = time.time()
            
            # Should complete within reasonable time (adjust threshold as needed)
            assert end_time - start_time < 5.0  # 5 seconds
            assert len(dates) == len(large_day_values)
        
        def test_large_file_reading_performance(self):
            """Test performance of reading large files."""
            # This would require creating or using large test files
            pass

Mock and Patch Tests
--------------------

Testing External Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from unittest.mock import patch, mock_open
    import pandas as pd

    class TestMocking:
        """Test using mocks for external dependencies."""
        
        @patch('pandas.read_csv')
        def test_csv_reading_with_mock(self, mock_read_csv):
            """Test CSV reading function using mocked pandas."""
            # Setup mock return value
            mock_data = pd.DataFrame({
                'day_of_year': [1.0, 2.0, 3.0],
                'temperature': [15.0, 16.0, 17.0]
            })
            mock_read_csv.return_value = mock_data
            
            # Test function
            from cequalw2.fileio import read_csv
            result = read_csv('dummy.csv', data_columns=['temperature'])
            
            # Verify mock was called correctly
            mock_read_csv.assert_called_once()
            assert 'temperature' in result.columns
        
        @patch('matplotlib.pyplot.savefig')
        def test_plot_saving_with_mock(self, mock_savefig, sample_data):
            """Test plot saving using mocked matplotlib."""
            from cequalw2.visualization import plot
            
            fig = plot(sample_data)
            
            # Verify savefig would be called if we called it
            # (This tests the plot creation, not actual file saving)
            assert fig is not None

Test Configuration
------------------

pytest.ini Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    # pytest.ini
    [tool:pytest]
    testpaths = tests
    python_files = test_*.py
    python_classes = Test*
    python_functions = test_*
    addopts = 
        --verbose
        --strict-markers
        --disable-warnings
    markers =
        unit: Unit tests
        integration: Integration tests
        performance: Performance tests
        slow: Slow tests that can be skipped

Coverage Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    # .coveragerc
    [run]
    source = cequalw2
    omit = 
        */tests/*
        */venv/*
        */env/*
        setup.py

    [report]
    exclude_lines =
        pragma: no cover
        def __repr__
        raise AssertionError
        raise NotImplementedError

Continuous Integration
----------------------

GitHub Actions Example
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

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
        - uses: actions/checkout@v3
        
        - name: Set up Python ${{ matrix.python-version }}
          uses: actions/setup-python@v4
          with:
            python-version: ${{ matrix.python-version }}
            
        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -e .[dev]
            
        - name: Run tests
          run: |
            pytest --cov=cequalw2 --cov-report=xml
            
        - name: Upload coverage to Codecov
          uses: codecov/codecov-action@v3

Best Practices
--------------

Writing Good Tests
~~~~~~~~~~~~~~~~~~

1. **Test Naming**: Use descriptive names that explain what is being tested
2. **Test Structure**: Follow Arrange-Act-Assert pattern
3. **Independence**: Tests should not depend on each other
4. **Coverage**: Aim for high code coverage but focus on critical paths
5. **Speed**: Keep tests fast; use mocks for slow operations

Example of Well-Structured Test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def test_temperature_data_validation_with_valid_range(self):
        """Test that temperature validation passes for realistic values."""
        # Arrange
        valid_temps = [5.0, 15.0, 25.0, 30.0]  # Realistic water temperatures
        data = pd.DataFrame({'temperature': valid_temps})
        
        # Act
        result = validate_temperature_data(data)
        
        # Assert
        assert result['is_valid'] is True
        assert len(result['issues']) == 0
        assert result['validated_data'].equals(data)

Running Tests in Development
----------------------------

Pre-commit Testing
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Run quick tests before committing
    pytest tests/test_datetime.py tests/test_fileio.py -v

    # Run all tests except slow ones
    pytest -m "not slow"

    # Run with coverage for development
    pytest --cov=cequalw2 --cov-report=term-missing

Debugging Failed Tests
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Run failed tests only
    pytest --lf

    # Run with debugging on first failure
    pytest -x --pdb

    # Run with more verbose output
    pytest -vv -s

Contributing Tests
------------------

When adding new features, include:

1. **Unit tests** for individual functions
2. **Integration tests** for complete workflows  
3. **Error handling tests** for edge cases
4. **Performance tests** for critical code paths
5. **Documentation** explaining test purpose

Test Review Checklist
~~~~~~~~~~~~~~~~~~~~~~

- [ ] All new code has corresponding tests
- [ ] Tests cover both success and failure cases
- [ ] Tests are independent and can run in any order
- [ ] Test names clearly describe what is being tested
- [ ] Tests run quickly (< 1 second each for unit tests)
- [ ] Mock external dependencies appropriately
- [ ] Update test documentation as needed