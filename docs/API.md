# CE-QUAL-W2 Python Library API Reference

## Table of Contents

- [cequalw2.fileio](#cequalw2fileio)
- [cequalw2.utils](#cequalw2utils)
- [cequalw2.visualization](#cequalw2visualization)
- [cequalw2.analysis](#cequalw2analysis)

---

## cequalw2.fileio

File input/output operations for CE-QUAL-W2 data files.

### Classes

#### `FileType`
```python
class FileType(Enum):
    UNKNOWN = 0
    FIXED_WIDTH = 1
    CSV = 2
```
Enumeration for file type identification.

### Functions

#### `read(infile: str, year: int, data_columns: List[str], **kwargs) -> pd.DataFrame`
Universal file reader with automatic format detection.

**Parameters:**
- `infile` (str): Path to the input file
- `year` (int): Start year of the simulation
- `data_columns` (List[str]): Names of data columns to read
- `**kwargs`:
  - `skiprows` (int, default=3): Number of header rows to skip
  - `file_type` (FileType, optional): Explicitly specify file type

**Returns:**
- `pd.DataFrame`: Time series data with datetime index

**Example:**
```python
df = read('temperature.csv', 2023, ['temp', 'do'])
```

#### `read_csv(infile: str, data_columns: List[str], skiprows: int = 3) -> pd.DataFrame`
Read CE-QUAL-W2 time series in CSV format.

**Parameters:**
- `infile` (str): Path to CSV file
- `data_columns` (List[str]): Column names
- `skiprows` (int): Header rows to skip

**Returns:**
- `pd.DataFrame`: Data with day-of-year index

#### `read_npt_opt(infile: str, data_columns: List[str], skiprows: int = 3) -> pd.DataFrame`
Read CE-QUAL-W2 fixed-width format files (*.npt, *.opt).

**Parameters:**
- `infile` (str): Path to NPT/OPT file
- `data_columns` (List[str]): Column names
- `skiprows` (int): Header rows to skip

**Returns:**
- `pd.DataFrame`: Data with day-of-year index

#### `read_sqlite(file_path: str) -> pd.DataFrame`
Read SQLite database containing CE-QUAL-W2 output.

**Parameters:**
- `file_path` (str): Path to SQLite database

**Returns:**
- `pd.DataFrame`: First table from database with datetime index

#### `read_excel(file_path: str, **kwargs) -> pd.DataFrame`
Read Excel file containing CE-QUAL-W2 data.

**Parameters:**
- `file_path` (str): Path to Excel file
- `**kwargs`: Additional pandas read_excel parameters

**Returns:**
- `pd.DataFrame`: Data with datetime index

#### `write_hdf(df: pd.DataFrame, group: str, outfile: str, overwrite=True)`
Write DataFrame to HDF5 format.

**Parameters:**
- `df` (pd.DataFrame): Data to write
- `group` (str): HDF5 group name
- `outfile` (str): Output file path
- `overwrite` (bool): Whether to overwrite existing data

#### `read_hdf(group: str, infile: str, variables: List[str]) -> pd.DataFrame`
Read time series from HDF5 file.

**Parameters:**
- `group` (str): HDF5 group name
- `infile` (str): Input file path
- `variables` (List[str]): Variable names to read

**Returns:**
- `pd.DataFrame`: Time series data

#### `get_header_row_number(file_path: str) -> int`
Determine header row number based on filename.

**Parameters:**
- `file_path` (str): File path

**Returns:**
- `int`: Header row number (0 for TSR files, 2 for others)

#### `split_fixed_width_line(line: str, field_width: int) -> List[str]`
Split a line into fixed-width segments.

**Parameters:**
- `line` (str): Line to split
- `field_width` (int): Width of each field

**Returns:**
- `List[str]`: List of segments

---

## cequalw2.utils

Utility functions for CE-QUAL-W2 data processing.

### Functions

#### `day_of_year_to_date(year: int, day_of_year_list: List[float]) -> List[datetime]`
Convert CE-QUAL-W2 day-of-year values to datetime objects.

**Parameters:**
- `year` (int): Year for conversion
- `day_of_year_list` (List[float]): List of day-of-year values (1.0 = Jan 1, 32.5 = Feb 1 at noon)

**Returns:**
- `List[datetime]`: List of datetime objects

**Example:**
```python
dates = day_of_year_to_date(2023, [1.0, 91.5, 182.0])
# Returns: [Jan 1 2023, Apr 1 2023 12:00, Jul 1 2023]
```

#### `day_of_year_to_datetime(year: int, day_of_year_list: List[int]) -> List[datetime]`
Alias for `day_of_year_to_date()`.

#### `round_time(date_time: datetime = None, round_to: int = 60) -> datetime`
Round datetime to nearest specified interval.

**Parameters:**
- `date_time` (datetime, optional): Input datetime (defaults to now)
- `round_to` (int): Seconds to round to (default 60)

**Returns:**
- `datetime`: Rounded datetime

#### `convert_to_datetime(year: int, days: List[int]) -> List[datetime]`
Convert day numbers to datetime objects.

**Parameters:**
- `year` (int): Year for conversion
- `days` (List[int]): Day numbers (1-365/366)

**Returns:**
- `List[datetime]`: List of datetime objects

---

## cequalw2.visualization

Visualization tools for CE-QUAL-W2 data.

### Constants

#### Color Palettes
```python
rainbow = ['#3366CC', '#0099C6', '#109618', '#FCE030', '#FF9900', '#DC3912']
everest = ['#3366CC', '#DC4020', '#10AA18', '#0099C6', '#FCE030', '#FF9900']
k2 = (...)  # 8-color palette
```

#### Other Constants
- `DEG_C_ALT`: Degree Celsius symbol
- `DEFAULT_COLOR`: Default line color (#4488ee)

### Functions

#### `plot(df: pd.DataFrame, **kwargs) -> plt.Figure`
Create a single plot with all variables.

**Parameters:**
- `df` (pd.DataFrame): Data to plot
- `**kwargs`:
  - `fig` (plt.Figure): Existing figure
  - `ax` (plt.Axes): Existing axes
  - `legend_values` (List[str]): Custom legend labels
  - `fig_size` (tuple): Figure size (width, height)
  - `style` (str): Line style (default '-')
  - `colors`: Color specification
  - `ylabel` (str): Y-axis label

**Returns:**
- `plt.Figure`: Matplotlib figure

**Example:**
```python
fig = plot(df, ylabel='Temperature (°C)', colors=k2)
```

#### `multi_plot(df: pd.DataFrame, **kwargs) -> plt.Figure`
Create subplots for each variable.

**Parameters:**
- `df` (pd.DataFrame): Data to plot
- `**kwargs`:
  - `figsize` (tuple): Figure size (default (15, 30))
  - `title` (str): Plot title
  - `xlabel` (str): X-axis label
  - `ylabels` (List[str]): Y-axis labels for each subplot
  - `colors`: Color specification
  - `style` (str): Line style
  - `palette` (str): Seaborn color palette

**Returns:**
- `plt.Figure`: Matplotlib figure with subplots

#### `simple_plot(series: pd.Series, **kwargs) -> plt.Figure`
Basic plotting for single series.

**Parameters:**
- `series` (pd.Series): Data to plot
- `**kwargs`:
  - `title` (str): Plot title
  - `ylabel` (str): Y-axis label
  - `colors` (List[str]): Colors to use
  - `figsize` (tuple): Figure size
  - `style` (str): Line style
  - `palette` (str): Color palette

**Returns:**
- `plt.Figure`: Matplotlib figure

#### `plot_all_files(plot_control_yaml: str, model_path: str, year: int, filetype: str = 'png', VERBOSE: bool = False)`
Batch plotting from YAML control file.

**Parameters:**
- `plot_control_yaml` (str): Path to YAML control file
- `model_path` (str): Path to model output directory
- `year` (int): Simulation start year
- `filetype` (str): Output image format
- `VERBOSE` (bool): Print progress messages

#### `hv_plot(df: pd.DataFrame, width=1200, height=600, **kwargs) -> tuple`
Create interactive HoloViews plot.

**Parameters:**
- `df` (pd.DataFrame): Data to plot
- `width` (int): Plot width
- `height` (int): Plot height
- `**kwargs`: Additional styling options

**Returns:**
- `tuple`: (curves_dict, tooltips_dict)

#### `get_colors(df: pd.DataFrame, palette: str, min_colors: int = 6) -> List[str]`
Get color list from seaborn palette.

**Parameters:**
- `df` (pd.DataFrame): DataFrame (used for column count)
- `palette` (str): Seaborn palette name
- `min_colors` (int): Minimum colors to return

**Returns:**
- `List[str]`: List of color values

---

## cequalw2.analysis

Analysis and reporting tools.

### Functions

#### `generate_plots_report(*args, **kwargs) -> None`
Generate markdown report with embedded plots.

**Parameters:**
- `*args` (required in order):
  1. `control_df` (pd.DataFrame): Plot control dataframe
  2. `model_path` (str): Path to model directory
  3. `outfile` (str): Output report path
- `**kwargs`:
  - `title` (str): Report title
  - `subtitle` (str): Report subtitle
  - `file_type` (str): Image format (default 'png')
  - `yaml` (str): Additional YAML content
  - `pdf_report` (bool): Generate PDF using pandoc

**Example:**
```python
generate_plots_report(control_df, '/model/path', 'report.md',
                      title='Model Results', file_type='png')
```

#### `sql_query(database_name: str, query: str) -> pd.DataFrame`
Execute SQL query on SQLite database.

**Parameters:**
- `database_name` (str): Database file path
- `query` (str): SQL query string

**Returns:**
- `pd.DataFrame`: Query results with datetime index

#### `read_sql(database: str, table: str, index_is_datetime=True) -> pd.DataFrame`
Read entire table from SQLite database.

**Parameters:**
- `database` (str): Database file path
- `table` (str): Table name
- `index_is_datetime` (bool): Convert index to datetime

**Returns:**
- `pd.DataFrame`: Table contents

#### `write_csv(df: pd.DataFrame, outfile: str, year: int, header: str = None, float_format='%.3f')`
Write DataFrame to CE-QUAL-W2 CSV format.

**Parameters:**
- `df` (pd.DataFrame): Data with datetime index
- `outfile` (str): Output file path
- `year` (int): Year for Julian day calculation
- `header` (str): Optional header text
- `float_format` (str): Float formatting string

**Notes:**
- Converts datetime index to CE-QUAL-W2 Julian day format
- Adds JDAY column as first column
- Default header is "$\n\n"

---

## Error Handling

Most functions will raise:
- `FileNotFoundError`: When input files don't exist
- `ValueError`: For invalid parameters or data format issues
- `IOError`: For file reading/writing errors
- `ImportError`: If required dependencies are missing

## Type Hints

All functions include type hints for parameters and return values, compatible with Python 3.7+.