# Contributing to CE-QUAL-W2 Python Library

Thank you for your interest in contributing to the CE-QUAL-W2 Python library! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Workflow](#contribution-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Types of Contributions

We welcome various types of contributions:

- **Bug reports**: Help us identify and fix issues
- **Feature requests**: Suggest new functionality
- **Code contributions**: Implement bug fixes or new features
- **Documentation improvements**: Enhance or clarify documentation
- **Performance improvements**: Optimize existing code
- **Test coverage**: Add tests for existing functionality

### Before You Start

1. Check existing [issues](https://github.com/ecohydrology/cequalw2-Claude/issues) to see if your contribution has already been discussed
2. For major changes, open an issue first to discuss the proposed changes
3. Ensure your contribution aligns with the project's goals and scope

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- pip or conda package manager

### Setting Up Your Development Environment

1. **Fork the repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/cequalw2-Claude.git
   cd cequalw2-Claude
   ```

2. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/ecohydrology/cequalw2-Claude.git
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

5. **Verify installation**
   ```bash
   python -c "import cequalw2; print('Success!')"
   pytest tests/
   ```

## Contribution Workflow

### Creating a Feature Branch

```bash
# Ensure you're on main and up to date
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

### Making Changes

1. Make your changes in logical, atomic commits
2. Follow the coding standards outlined below
3. Add tests for new functionality
4. Update documentation as needed
5. Ensure all tests pass

### Staying Up to Date

```bash
# Regularly sync with upstream
git fetch upstream
git checkout main
git merge upstream/main
git checkout feature/your-feature-name
git rebase main
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with some modifications:

- **Line length**: 88 characters (Black formatter default)
- **Import order**: Use `isort` to organize imports
- **Docstrings**: Use Google-style docstrings

### Code Formatting

We use automated tools to maintain consistent code style:

```bash
# Format code with Black
black cequalw2/

# Sort imports with isort
isort cequalw2/

# Check code style with flake8
flake8 cequalw2/

# Type checking with mypy (optional)
mypy cequalw2/
```

### Example Code Style

```python
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
```

### Naming Conventions

- **Functions and variables**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Modules**: `lowercase` or `snake_case`

### Type Hints

Use type hints for all public functions:

```python
from typing import List, Optional, Union, Dict, Any

def process_data(
    data: pd.DataFrame,
    columns: List[str],
    options: Optional[Dict[str, Any]] = None
) -> Union[pd.DataFrame, None]:
    """Process data with type hints."""
    pass
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Test both normal and edge cases

```python
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
    
    def test_invalid_year_error_case(self):
        """Test error handling for invalid year."""
        with pytest.raises(ValueError):
            day_of_year_to_date(-1, [1.0])
```

### Test Coverage

- Aim for >90% test coverage
- Check coverage with: `pytest --cov=cequalw2 --cov-report=html`
- Focus on testing public APIs and critical functionality

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_datetime.py

# Run with coverage
pytest --cov=cequalw2

# Run performance tests
pytest tests/ -m performance
```

## Documentation

### Docstring Standards

Use Google-style docstrings for all public functions:

```python
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
```

### README and Documentation Updates

- Update README.md for new features
- Add examples to docs/EXAMPLES.md
- Update API documentation in docs/API.md
- Ensure all examples in documentation work correctly

## Submitting Changes

### Pull Request Process

1. **Ensure code quality**
   ```bash
   # Run all checks before submitting
   black cequalw2/
   isort cequalw2/
   flake8 cequalw2/
   pytest tests/
   ```

2. **Update documentation**
   - Add docstrings to new functions
   - Update relevant documentation files
   - Add examples if appropriate

3. **Write clear commit messages**
   ```bash
   # Good commit messages
   git commit -m "Add support for reading NPT files with custom headers"
   git commit -m "Fix date conversion bug for leap years"
   git commit -m "Improve performance of large file reading by 30%"
   
   # Avoid vague messages
   git commit -m "Fix bug"
   git commit -m "Update code"
   ```

4. **Create pull request**
   - Use the pull request template
   - Provide clear description of changes
   - Reference any related issues
   - Include screenshots for UI changes

### Pull Request Template

```markdown
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
```

### Review Process

1. **Automated checks**: All CI checks must pass
2. **Code review**: At least one maintainer review required
3. **Testing**: Verify tests pass and coverage is maintained
4. **Documentation**: Ensure documentation is updated

### After Your PR is Merged

```bash
# Clean up your local repository
git checkout main
git pull upstream main
git branch -d feature/your-feature-name
```

## Issue Reporting

### Bug Reports

Use the bug report template and include:

- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Relevant code snippets or error messages

### Feature Requests

For new features, provide:

- Clear description of the proposed feature
- Use case and motivation
- Proposed API or interface (if applicable)
- Any implementation considerations

## Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes for significant contributions
- Project documentation where appropriate

## Getting Help

- Join discussions in GitHub issues
- Ask questions in pull request comments
- Contact maintainers for complex questions

## Release Process

For maintainers:

1. Update version in `setup.py` and `__init__.py`
2. Update CHANGELOG.md
3. Create release tag
4. Update documentation
5. Announce release

Thank you for contributing to the CE-QUAL-W2 Python library!