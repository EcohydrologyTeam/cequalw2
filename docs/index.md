# CE-QUAL-W2 Python Library Documentation

Welcome to the documentation for the CE-QUAL-W2 Python library!

## Overview

The CE-QUAL-W2 Python library provides tools for reading, writing, and visualizing CE-QUAL-W2 model data. This library is designed to streamline the workflow for water quality modelers and researchers working with CE-QUAL-W2 output files.

## Documentation Structure

### Getting Started
- **[README](../README.md)** - Quick start guide and installation instructions
- **[Examples](EXAMPLES.md)** - Comprehensive usage examples and tutorials

### Reference
- **[API Reference](API.md)** - Complete API documentation for all modules
- **[Testing Guide](TESTING.md)** - Information about the test suite and how to run tests

### Development
- **[Contributing](../CONTRIBUTING.md)** - Guidelines for contributing to the project
- **[CLAUDE.md](../CLAUDE.md)** - Technical guidance for AI assistants working with this codebase

## Quick Navigation

### By Module

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **[cequalw2.fileio](API.md#cequalw2fileio)** | File I/O operations | `read()`, `read_csv()`, `read_sqlite()` |
| **[cequalw2.utils](API.md#cequalw2utils)** | Utility functions | `day_of_year_to_date()`, `round_time()` |
| **[cequalw2.visualization](API.md#cequalw2visualization)** | Plotting and charts | `plot()`, `multi_plot()`, `hv_plot()` |
| **[cequalw2.analysis](API.md#cequalw2analysis)** | Analysis tools | `generate_plots_report()`, `sql_query()` |

### By Task

| Task | Documentation | Examples |
|------|---------------|----------|
| **Reading files** | [API: fileio](API.md#cequalw2fileio) | [File I/O Examples](EXAMPLES.md#file-io-operations) |
| **Date conversion** | [API: utils](API.md#cequalw2utils) | [Date/Time Examples](EXAMPLES.md#datetime-handling) |
| **Creating plots** | [API: visualization](API.md#cequalw2visualization) | [Visualization Examples](EXAMPLES.md#data-visualization) |
| **Generating reports** | [API: analysis](API.md#cequalw2analysis) | [Analysis Examples](EXAMPLES.md#analysis-and-reporting) |
| **Running tests** | [Testing Guide](TESTING.md) | [Test Examples](TESTING.md#test-structure) |

## Installation

```bash
# Clone repository
git clone https://github.com/ecohydrology/cequalw2-Claude.git
cd cequalw2-Claude

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

## Quick Start

```python
from cequalw2.fileio import read
from cequalw2.utils import day_of_year_to_date
from cequalw2.visualization import plot

# Read CE-QUAL-W2 output
data = read('output.csv', year=2023, data_columns=['temp', 'do'])

# Create visualization
fig = plot(data, ylabel='Water Quality Parameters')
fig.savefig('water_quality.png')
```

## Key Features

### 🔄 File Format Support
- CSV files with automatic format detection
- Fixed-width NPT/OPT files
- SQLite databases
- Excel spreadsheets
- HDF5 files for large datasets

### 📅 Date/Time Handling
- Convert CE-QUAL-W2 day-of-year format to Python datetime
- Handle leap years correctly
- Time rounding utilities
- Flexible date range support

### 📊 Visualization
- Matplotlib-based plotting with CE-QUAL-W2 conventions
- Interactive plots using HoloViews and Bokeh
- Batch plotting from YAML control files
- Customizable color palettes and styling

### 📈 Analysis Tools
- Statistical analysis functions
- Report generation with embedded plots
- SQL query interface for databases
- Data export in multiple formats

## Version Information

- **Current Version**: 1.0.0
- **Python Support**: 3.7+
- **Key Dependencies**: pandas, matplotlib, seaborn, holoviews

## Support and Community

### Getting Help
- Check the [examples](EXAMPLES.md) for common use cases
- Review the [API documentation](API.md) for function details
- Search existing [GitHub issues](https://github.com/ecohydrology/cequalw2-Claude/issues)
- Create a new issue for bugs or feature requests

### Contributing
- Read the [Contributing Guide](../CONTRIBUTING.md)
- Follow the [coding standards](../CONTRIBUTING.md#coding-standards)
- Add tests for new functionality
- Update documentation for changes

### Testing
- Run tests with `pytest tests/`
- Check coverage with `pytest --cov=cequalw2`
- See [Testing Guide](TESTING.md) for details

## License

This project is licensed under the MIT License. See [LICENSE](../LICENSE) for details.

## Citation

If you use this library in your research, please cite:

```
Steissberg, T.E. (2023). CE-QUAL-W2 Python Library. 
Ecohydrology Team, ERDC, U.S. Army Corps of Engineers.
https://github.com/ecohydrology/cequalw2-Claude
```

---

*Documentation generated for CE-QUAL-W2 Python Library v1.0.0*