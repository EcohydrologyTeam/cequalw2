# CE-QUAL-W2 Python Library

A Python library for reading, writing, and visualizing CE-QUAL-W2 model data.

## Overview

CE-QUAL-W2 is a two-dimensional, vertically-averaged, hydrodynamic and water quality model used for simulating water movement, temperature, and concentrations of various chemical constituents in lakes, reservoirs, estuaries, and rivers. This Python library provides tools to work with CE-QUAL-W2 input and output files.

## Features

- **File I/O**: Read various CE-QUAL-W2 file formats (CSV, fixed-width, SQLite, HDF5, Excel)
- **Date/Time Utilities**: Convert CE-QUAL-W2 day-of-year format to Python datetime objects
- **Visualization**: Create plots and visualizations of model results using matplotlib, seaborn, and holoviews
- **Analysis**: Statistical analysis and report generation tools
- **Flexible**: Automatic file type detection and multiple output format support

## Installation

### From Source (Development Mode)

```bash
git clone https://github.com/ecohydrology/cequalw2-Claude.git
cd cequalw2-Claude
pip install -e .
```

### Install Dependencies Only

```bash
pip install -r requirements.txt
```

### Development Dependencies

```bash
pip install -r requirements-dev.txt
```

## Quick Start

```python
import pandas as pd
from cequalw2.fileio import read, FileType
from cequalw2.utils import day_of_year_to_date
from cequalw2.visualization import plot, multi_plot

# Read CE-QUAL-W2 output file
data = read('output.csv', year=2023, data_columns=['temp', 'do'])

# Convert day-of-year to datetime
dates = day_of_year_to_date(2023, [1.0, 32.5, 91.0])

# Create visualization
fig = plot(data, ylabel='Temperature (°C)')
```

## Module Structure

### `cequalw2.fileio`
File input/output operations for various formats.

- `read()` - Universal file reader with automatic format detection
- `read_csv()` - Read CSV format files
- `read_npt_opt()` - Read fixed-width NPT/OPT files
- `read_sqlite()` - Read SQLite database files
- `read_excel()` - Read Excel files
- `write_hdf()` - Write data to HDF5 format
- `read_hdf()` - Read data from HDF5 format

### `cequalw2.utils`
Utility functions for data processing.

- `day_of_year_to_date()` - Convert CE-QUAL-W2 day-of-year to datetime
- `day_of_year_to_datetime()` - Alias for above
- `round_time()` - Round datetime to nearest interval
- `convert_to_datetime()` - Convert day numbers to datetime objects

### `cequalw2.visualization`
Plotting and visualization tools.

- `plot()` - Create single plot with all variables
- `multi_plot()` - Create subplots for each variable
- `simple_plot()` - Basic plotting for single series
- `plot_all_files()` - Batch plotting from YAML control file
- `hv_plot()` - Interactive plots using HoloViews
- Color palettes: `rainbow`, `everest`, `k2`

### `cequalw2.analysis`
Analysis and reporting tools.

- `generate_plots_report()` - Generate markdown report with plots
- `sql_query()` - Query time series from SQLite
- `write_csv()` - Write data to CE-QUAL-W2 CSV format

## Examples

### Reading Different File Formats

```python
from cequalw2.fileio import read, FileType

# Auto-detect format from extension
data = read('temperature.csv', year=2023, data_columns=['temp'])

# Explicitly specify format
data = read('output.npt', year=2023, data_columns=['temp', 'do'], 
            file_type=FileType.FIXED_WIDTH)

# Read with custom header rows
data = read('data.csv', year=2023, data_columns=['flow'], skiprows=5)
```

### Date/Time Conversion

```python
from cequalw2.utils import day_of_year_to_date

# Convert single value
dates = day_of_year_to_date(2023, [91.5])  # Returns April 1, 2023 at 12:00

# Convert multiple values
day_values = [1.0, 32.5, 60.25, 91.0, 121.5]
dates = day_of_year_to_date(2023, day_values)

# Handle leap years
leap_dates = day_of_year_to_date(2024, [366.0])  # December 31, 2024
```

### Creating Visualizations

```python
from cequalw2.visualization import plot, multi_plot
import pandas as pd

# Sample data
df = pd.DataFrame({
    'temperature': [15.2, 15.5, 16.1, 16.8, 17.2],
    'dissolved_oxygen': [8.5, 8.3, 8.1, 7.9, 7.7]
})

# Single plot with all variables
fig = plot(df, ylabel='Value', title='Water Quality Parameters')

# Separate subplot for each variable
fig = multi_plot(df, ylabels=['Temperature (°C)', 'DO (mg/L)'])

# Custom styling
fig = plot(df, colors='viridis', style='--', figsize=(12, 6))
```

### Working with SQLite Databases

```python
from cequalw2.fileio import read_sqlite
from cequalw2.analysis import sql_query

# Read entire table
df = read_sqlite('model_output.db')

# Custom SQL query
query = "SELECT Date, Temperature FROM results WHERE Temperature > 20"
df = sql_query('model_output.db', query)
```

### Generating Reports

```python
from cequalw2.analysis import generate_plots_report
from cequalw2.fileio import read_plot_control

# Read plot control file
control_df = read_plot_control('plot_control.yaml')

# Generate markdown report with all plots
generate_plots_report(control_df, '/path/to/model', 'report.md',
                      title='Model Results Summary',
                      file_type='png')
```

## Testing

The library includes a comprehensive test suite using pytest.

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_datetime.py

# Run with coverage
pytest tests/ --cov=cequalw2
```

### Test Structure

- `test_datetime.py` - Tests for date/time conversion functions
- `test_io.py` - Tests for file I/O operations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Format code
black cequalw2/

# Check code quality
flake8 cequalw2/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Todd E. Steissberg, PhD, PE**  
Water Quality and Contaminant Modeling Branch  
Environmental Laboratory
Engineer Research and Development Center (ERDC)  
U.S. Army Corps of Engineers

## Acknowledgments

- CE-QUAL-W2 model developers at Portland State University
- Contributors to the scientific Python ecosystem (NumPy, Pandas, Matplotlib, etc.)

## Citation

If you use this library in your research, please cite:

```
Steissberg, T.E. (2025). CE-QUAL-W2 Python Library. Environmental Laboratory, Engineer Research and Development Center, U.S. Army Corps of Engineers.
```