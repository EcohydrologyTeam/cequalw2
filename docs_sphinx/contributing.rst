Contributing
============

Thank you for your interest in contributing to the CE-QUAL-W2 Python Library!

.. note::
   For detailed contribution guidelines, see the 
   `CONTRIBUTING.md <https://github.com/ecohydrology/cequalw2-Claude/blob/main/CONTRIBUTING.md>`_ 
   file in the repository root.

Quick Start for Contributors
-----------------------------

Getting Started
~~~~~~~~~~~~~~~

1. **Fork and Clone**

   .. code-block:: bash

      # Fork on GitHub, then clone your fork
      git clone https://github.com/YOUR_USERNAME/cequalw2-Claude.git
      cd cequalw2-Claude

2. **Set Up Development Environment**

   .. code-block:: bash

      # Create virtual environment
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

      # Install in development mode
      pip install -e .
      pip install -r requirements-dev.txt

3. **Run Tests**

   .. code-block:: bash

      # Verify everything works
      pytest tests/

Types of Contributions
----------------------

We welcome various types of contributions:

Bug Reports
~~~~~~~~~~~

Help us improve by reporting issues:

* Use the GitHub issue template
* Include Python version and OS details
* Provide minimal reproducible example
* Include complete error messages

Feature Requests
~~~~~~~~~~~~~~~~

Suggest new functionality:

* Describe the use case clearly
* Explain the proposed interface
* Consider implementation complexity
* Discuss with maintainers first for major changes

Code Contributions
~~~~~~~~~~~~~~~~~~

Implement bug fixes or new features:

* Follow coding standards
* Add comprehensive tests
* Update documentation
* Keep changes focused and atomic

Documentation Improvements
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Enhance or clarify documentation:

* Fix typos and improve clarity
* Add examples for complex features
* Update API documentation
* Improve user guides

Development Workflow
--------------------

Creating a Feature Branch
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Ensure you're on main and up to date
   git checkout main
   git pull upstream main

   # Create feature branch
   git checkout -b feature/descriptive-name

Making Changes
~~~~~~~~~~~~~~

1. **Code Changes**: Follow the style guide and add tests
2. **Documentation**: Update relevant documentation
3. **Tests**: Ensure all tests pass and add new ones
4. **Commit**: Use clear, descriptive commit messages

.. code-block:: bash

   # Good commit messages
   git commit -m "Add support for reading NPT files with custom headers"
   git commit -m "Fix date conversion bug for leap years"

   # Avoid vague messages
   git commit -m "Fix bug"
   git commit -m "Update code"

Coding Standards
----------------

Python Style Guide
~~~~~~~~~~~~~~~~~~~

We follow PEP 8 with some modifications:

* **Line length**: 88 characters (Black formatter default)
* **Import order**: Use isort for import organization
* **Docstrings**: Google-style docstrings for all public functions

Code Formatting Tools
~~~~~~~~~~~~~~~~~~~~~

Use these tools to maintain consistent style:

.. code-block:: bash

   # Format code with Black
   black cequalw2/

   # Sort imports with isort
   isort cequalw2/

   # Check style with flake8
   flake8 cequalw2/

Example Code Style
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   """Module docstring describing the module's purpose."""

   import os
   from typing import List, Optional, Union

   import pandas as pd
   import numpy as np

   from cequalw2.utils import day_of_year_to_date


   def read_data_file(
       filepath: str, 
       year: int, 
       columns: List[str],
       skiprows: int = 3
   ) -> pd.DataFrame:
       """
       Read CE-QUAL-W2 data file and return processed DataFrame.
       
       Args:
           filepath: Path to the input file
           year: Start year for date conversion
           columns: List of column names
           skiprows: Number of header rows to skip
           
       Returns:
           DataFrame with datetime index and specified columns
           
       Raises:
           FileNotFoundError: If the input file doesn't exist
           ValueError: If columns are not found in the file
           
       Example:
           >>> df = read_data_file('output.csv', 2023, ['temp', 'do'])
           >>> print(df.shape)
           (365, 2)
       """
       if not os.path.exists(filepath):
           raise FileNotFoundError(f"File not found: {filepath}")
       
       # Implementation here
       pass

Testing Guidelines
------------------

Writing Tests
~~~~~~~~~~~~~

* Write tests for all new functionality
* Use descriptive test names
* Follow Arrange-Act-Assert pattern
* Test both normal and edge cases

.. code-block:: python

   import pytest
   import pandas as pd
   from cequalw2.utils import day_of_year_to_date


   class TestDateConversion:
       """Test date conversion utilities."""
       
       def test_single_day_conversion_normal_case(self):
           """Test conversion of single day-of-year value."""
           # Arrange
           year = 2023
           day_values = [1.0]
           expected = [datetime.datetime(2023, 1, 1, 0, 0)]
           
           # Act
           result = day_of_year_to_date(year, day_values)
           
           # Assert
           assert result == expected
       
       def test_empty_list_edge_case(self):
           """Test conversion with empty input list."""
           result = day_of_year_to_date(2023, [])
           assert result == []

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=cequalw2

   # Run specific test file
   pytest tests/test_datetime.py

Documentation Standards
-----------------------

Docstring Format
~~~~~~~~~~~~~~~~

Use Google-style docstrings for all public functions:

.. code-block:: python

   def complex_function(
       param1: str,
       param2: int,
       param3: Optional[List[str]] = None
   ) -> Dict[str, Any]:
       """
       One-line summary of what the function does.
       
       Longer description if needed, explaining the purpose,
       algorithm, or important implementation details.
       
       Args:
           param1: Description of parameter 1
           param2: Description of parameter 2
           param3: Optional parameter description
           
       Returns:
           Description of return value and its structure
           
       Raises:
           ValueError: When parameter validation fails
           FileNotFoundError: When input file is missing
           
       Example:
           Basic usage example:
           
           >>> result = complex_function("input", 42)
           >>> print(result['status'])
           'success'
           
       Note:
           Any important notes about usage, performance,
           or limitations.
       """

Documentation Updates
~~~~~~~~~~~~~~~~~~~~~

When making changes:

* Update README.md for new features
* Add examples to docs/EXAMPLES.md
* Update API documentation
* Ensure all examples work correctly

Pull Request Process
--------------------

Before Submitting
~~~~~~~~~~~~~~~~~

1. **Run Quality Checks**

   .. code-block:: bash

      # Format and check code
      black cequalw2/
      isort cequalw2/
      flake8 cequalw2/

      # Run tests
      pytest tests/

2. **Update Documentation**

   * Add docstrings to new functions
   * Update relevant documentation files
   * Add examples if appropriate

3. **Write Clear Commit Messages**

   .. code-block:: bash

      # Use descriptive commit messages
      git commit -m "Add support for reading NPT files with custom headers"

Creating Pull Request
~~~~~~~~~~~~~~~~~~~~~

1. **Push to Your Fork**

   .. code-block:: bash

      git push origin feature/your-feature-name

2. **Create Pull Request on GitHub**

   * Use the pull request template
   * Provide clear description of changes
   * Reference any related issues
   * Include screenshots for UI changes

Pull Request Template
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: markdown

   ## Description
   Brief description of changes made.

   ## Type of Change
   - [ ] Bug fix (non-breaking change fixing an issue)
   - [ ] New feature (non-breaking change adding functionality)
   - [ ] Breaking change (fix or feature causing existing functionality to change)
   - [ ] Documentation update

   ## Testing
   - [ ] All existing tests pass
   - [ ] New tests added for new functionality
   - [ ] Manual testing completed

   ## Checklist
   - [ ] Code follows project style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes (or breaking changes documented)

   ## Related Issues
   Fixes #(issue number)

Review Process
~~~~~~~~~~~~~~

1. **Automated Checks**: All CI checks must pass
2. **Code Review**: At least one maintainer review required
3. **Testing**: Verify tests pass and coverage is maintained
4. **Documentation**: Ensure documentation is updated

Issue Guidelines
----------------

Bug Reports
~~~~~~~~~~~

Include the following information:

* **Environment**: Python version, OS, package versions
* **Description**: Clear description of the bug
* **Reproduction**: Minimal code to reproduce the issue
* **Expected vs Actual**: What you expected vs what happened
* **Error Messages**: Complete error messages and stack traces

Feature Requests
~~~~~~~~~~~~~~~~

Provide these details:

* **Use Case**: Describe the problem you're trying to solve
* **Proposed Solution**: Your ideas for implementation
* **Alternatives**: Other approaches you've considered
* **Additional Context**: Any other relevant information

Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

We expect all contributors to:

* Use welcoming and inclusive language
* Be respectful of differing viewpoints
* Accept constructive criticism gracefully
* Focus on what's best for the community
* Show empathy towards other community members

Getting Help
~~~~~~~~~~~~

* **Documentation**: Check existing documentation first
* **GitHub Issues**: Search existing issues
* **Discussions**: Use GitHub discussions for questions
* **Email**: Contact maintainers for sensitive issues

Recognition
-----------

Contributors are recognized in:

* **CONTRIBUTORS.md**: All contributors listed
* **Release Notes**: Significant contributions highlighted
* **Documentation**: Author attribution where appropriate
* **GitHub**: Contributor statistics and graphs

Release Process
---------------

For maintainers, the release process involves:

1. **Version Update**: Update version in setup.py and __init__.py
2. **Changelog**: Update CHANGELOG.md with new features and fixes
3. **Documentation**: Ensure documentation is current
4. **Testing**: Run full test suite
5. **Tagging**: Create release tag
6. **Distribution**: Upload to PyPI
7. **Announcement**: Announce release

Development Setup Details
-------------------------

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Install development dependencies
   pip install -r requirements-dev.txt

   # Contents of requirements-dev.txt:
   pytest>=6.0
   pytest-cov>=2.10
   black>=21.0
   isort>=5.0
   flake8>=3.8
   mypy>=0.812
   sphinx>=4.0
   sphinx-rtd-theme>=0.5

Pre-commit Hooks
~~~~~~~~~~~~~~~~

Set up pre-commit hooks to ensure code quality:

.. code-block:: bash

   # Install pre-commit
   pip install pre-commit

   # Install hooks
   pre-commit install

   # Run hooks manually
   pre-commit run --all-files

IDE Configuration
~~~~~~~~~~~~~~~~~

**VS Code Settings** (`.vscode/settings.json`):

.. code-block:: json

   {
       "python.formatting.provider": "black",
       "python.linting.enabled": true,
       "python.linting.flake8Enabled": true,
       "python.testing.pytestEnabled": true,
       "python.testing.unittestEnabled": false
   }

**PyCharm Configuration**:

* Set code style to Black
* Enable pytest as test runner
* Configure flake8 as external tool

Advanced Contributing
---------------------

Performance Improvements
~~~~~~~~~~~~~~~~~~~~~~~~

When contributing performance improvements:

* Include benchmarks showing improvement
* Test with realistic data sizes
* Consider memory usage implications
* Document any trade-offs

API Changes
~~~~~~~~~~~

For changes to public APIs:

* Discuss with maintainers first
* Maintain backward compatibility when possible
* Document breaking changes clearly
* Provide migration guide for users

Large Features
~~~~~~~~~~~~~~

For substantial new features:

1. **Design Document**: Create detailed design proposal
2. **Discussion**: Get community feedback
3. **Prototype**: Implement minimal working version
4. **Incremental**: Break into smaller pull requests
5. **Documentation**: Comprehensive documentation and examples

Thank you for contributing to the CE-QUAL-W2 Python Library! Your contributions help make water quality modeling more accessible and efficient for researchers and engineers worldwide.