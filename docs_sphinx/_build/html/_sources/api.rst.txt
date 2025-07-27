API Reference
=============

This section contains the complete API documentation for all modules in the CE-QUAL-W2 Python Library.

.. currentmodule:: cequalw2

Main Package
------------

.. automodule:: cequalw2
   :members:
   :undoc-members:
   :show-inheritance:

File I/O Module (cequalw2.fileio)
----------------------------------

The fileio module provides functions for reading and writing various file formats used by CE-QUAL-W2.

.. automodule:: cequalw2.fileio
   :members:
   :undoc-members:
   :show-inheritance:

Core Reading Functions
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.fileio.read

.. autofunction:: cequalw2.fileio.read_csv

.. autofunction:: cequalw2.fileio.read_npt_opt

.. autofunction:: cequalw2.fileio.read_excel

.. autofunction:: cequalw2.fileio.read_sqlite

.. autofunction:: cequalw2.fileio.read_hdf

Writing Functions
~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.fileio.write_hdf

Control File Functions
~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.fileio.read_plot_control

.. autofunction:: cequalw2.fileio.write_plot_control

Utility Classes
~~~~~~~~~~~~~~~

.. autoclass:: cequalw2.fileio.FileType
   :members:
   :undoc-members:

Utilities Module (cequalw2.utils)
---------------------------------

The utils module contains utility functions for date/time conversion and other common operations.

.. automodule:: cequalw2.utils
   :members:
   :undoc-members:
   :show-inheritance:

Date and Time Functions
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.utils.day_of_year_to_date

.. autofunction:: cequalw2.utils.round_time

Visualization Module (cequalw2.visualization)
----------------------------------------------

The visualization module provides plotting functions for creating charts and graphs from CE-QUAL-W2 data.

.. automodule:: cequalw2.visualization
   :members:
   :undoc-members:
   :show-inheritance:

Basic Plotting Functions
~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.visualization.plot

.. autofunction:: cequalw2.visualization.simple_plot

.. autofunction:: cequalw2.visualization.multi_plot

Interactive Plotting
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.visualization.hv_plot

Batch Plotting
~~~~~~~~~~~~~~

.. autofunction:: cequalw2.visualization.plot_all_files

Color Palettes
~~~~~~~~~~~~~~

Built-in color palettes for consistent styling:

.. autodata:: cequalw2.visualization.k2
   :annotation: = K2 color palette

.. autodata:: cequalw2.visualization.rainbow
   :annotation: = Rainbow color palette

.. autodata:: cequalw2.visualization.everest
   :annotation: = Everest color palette

Analysis Module (cequalw2.analysis)
------------------------------------

The analysis module provides functions for statistical analysis, report generation, and data export.

.. automodule:: cequalw2.analysis
   :members:
   :undoc-members:
   :show-inheritance:

Report Generation
~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.analysis.generate_plots_report

Database Operations
~~~~~~~~~~~~~~~~~~~

.. autofunction:: cequalw2.analysis.sql_query

Data Export
~~~~~~~~~~~

.. autofunction:: cequalw2.analysis.write_csv

Function Details
----------------

cequalw2.fileio.read
~~~~~~~~~~~~~~~~~~~~

.. function:: read(filepath, year=None, data_columns=None, skiprows=3, file_type=None)

   Read CE-QUAL-W2 output files with automatic format detection.

   This is the main function for reading CE-QUAL-W2 data files. It automatically
   detects the file format and calls the appropriate reader function.

   :param str filepath: Path to the input file
   :param int year: Start year for date conversion (required for most formats)
   :param list data_columns: List of column names to extract from the file
   :param int skiprows: Number of header rows to skip (default: 3)
   :param FileType file_type: Explicitly specify file format (optional)
   :returns: DataFrame with datetime index and specified columns
   :rtype: pandas.DataFrame
   :raises FileNotFoundError: If the input file doesn't exist
   :raises ValueError: If required parameters are missing

   **Example:**

   .. code-block:: python

      from cequalw2.fileio import read
      
      # Read CSV file with automatic detection
      data = read('output.csv', year=2023, data_columns=['temp', 'do'])
      
      # Explicitly specify format
      data = read('data.txt', year=2023, data_columns=['temp'], 
                  file_type=FileType.FIXED_WIDTH)

cequalw2.utils.day_of_year_to_date
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: day_of_year_to_date(year, day_values)

   Convert CE-QUAL-W2 day-of-year values to Python datetime objects.

   CE-QUAL-W2 uses a day-of-year format where January 1 = 1.0, and fractional
   values represent time of day (e.g., 1.5 = January 1, 12:00 PM).

   :param int year: The year for date conversion
   :param list day_values: List of day-of-year values (1.0 to 365.0/366.0)
   :returns: List of datetime objects corresponding to the input values
   :rtype: list[datetime.datetime]
   :raises ValueError: If year is invalid or day values are out of range

   **Example:**

   .. code-block:: python

      from cequalw2.utils import day_of_year_to_date
      
      # Convert single day
      dates = day_of_year_to_date(2023, [1.0])  # [datetime(2023, 1, 1, 0, 0)]
      
      # Convert multiple days with times
      dates = day_of_year_to_date(2023, [1.0, 1.5, 32.25])
      # [datetime(2023, 1, 1, 0, 0), 
      #  datetime(2023, 1, 1, 12, 0),
      #  datetime(2023, 2, 1, 6, 0)]

cequalw2.visualization.plot
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: plot(data, ylabel=None, title=None, colors=None, style='-', figsize=(12, 8), grid=True, **kwargs)

   Create a line plot of time series data.

   This function creates a matplotlib figure with all columns plotted as separate
   lines on the same axes.

   :param pandas.DataFrame data: DataFrame with datetime index and numeric columns
   :param str ylabel: Y-axis label (optional)
   :param str title: Plot title (optional)
   :param list colors: List of colors for each line (optional)
   :param str style: Line style (default: '-')
   :param tuple figsize: Figure size in inches (default: (12, 8))
   :param bool grid: Whether to show grid lines (default: True)
   :param kwargs: Additional arguments passed to matplotlib.pyplot.plot()
   :returns: Matplotlib figure object
   :rtype: matplotlib.figure.Figure

   **Example:**

   .. code-block:: python

      from cequalw2.visualization import plot
      
      # Basic plot
      fig = plot(data, ylabel='Water Quality Parameters')
      
      # Custom styling
      fig = plot(data, 
                 ylabel='Temperature (°C)',
                 title='Temperature Time Series',
                 colors=['red', 'blue'],
                 style='--',
                 figsize=(15, 10))
      
      fig.savefig('temperature_plot.png')

cequalw2.analysis.generate_plots_report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: generate_plots_report(control_df, model_path, outfile, title="Model Results", subtitle="", file_type='png', pdf_report=False)

   Generate a comprehensive analysis report with embedded plots.

   This function creates a Markdown report with statistics, plots, and analysis
   based on a control DataFrame that specifies which files to process and how
   to plot them.

   :param pandas.DataFrame control_df: DataFrame with plot configuration
   :param str model_path: Path to directory containing model output files
   :param str outfile: Output filename for the report
   :param str title: Report title (default: "Model Results")
   :param str subtitle: Report subtitle (optional)
   :param str file_type: Image format for plots (default: 'png')
   :param bool pdf_report: Whether to generate PDF version (requires pandoc)
   :returns: None (writes files to disk)

   **Example:**

   .. code-block:: python

      import pandas as pd
      from cequalw2.analysis import generate_plots_report
      
      # Create control DataFrame
      control = pd.DataFrame({
          'Filename': ['temp.csv', 'do.csv'],
          'Columns': [['temperature'], ['dissolved_oxygen']],
          'Labels': [['Temperature (°C)'], ['DO (mg/L)']],
          'PlotType': ['combined', 'subplots']
      })
      
      # Generate report
      generate_plots_report(
          control,
          model_path='/path/to/model/output',
          outfile='analysis_report.md',
          title='Water Quality Analysis',
          pdf_report=True
      )

Data Types and Constants
------------------------

FileType Enumeration
~~~~~~~~~~~~~~~~~~~~

.. class:: FileType

   Enumeration of supported file types for explicit format specification.

   .. attribute:: CSV
      
      Comma-separated values format

   .. attribute:: FIXED_WIDTH
      
      Fixed-width format (NPT/OPT files)

   .. attribute:: EXCEL
      
      Microsoft Excel format

   .. attribute:: SQLITE
      
      SQLite database format

   .. attribute:: HDF5
      
      HDF5 scientific data format

Color Palettes
~~~~~~~~~~~~~~

The visualization module includes several predefined color palettes:

.. data:: k2

   K2 color palette optimized for scientific visualization.
   
   Colors: ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

.. data:: rainbow

   Rainbow color palette with vibrant colors.
   
   Colors: ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']

.. data:: everest

   Everest color palette inspired by mountain landscapes.
   
   Colors: ['#1e3a8a', '#3b82f6', '#06b6d4', '#10b981', '#84cc16', '#eab308']

Error Handling
--------------

The library defines several custom exceptions for better error handling:

.. exception:: FileFormatError

   Raised when a file format cannot be determined or is not supported.

.. exception:: DateConversionError

   Raised when day-of-year values cannot be converted to valid dates.

.. exception:: DataValidationError

   Raised when input data fails validation checks.

Usage Patterns
--------------

Common Workflow
~~~~~~~~~~~~~~~

A typical analysis workflow follows this pattern:

.. code-block:: python

   from cequalw2.fileio import read
   from cequalw2.utils import day_of_year_to_date
   from cequalw2.visualization import plot
   from cequalw2.analysis import generate_plots_report
   
   # 1. Read data
   data = read('model_output.csv', year=2023, data_columns=['temp', 'do'])
   
   # 2. Basic analysis
   print(data.describe())
   
   # 3. Visualization
   fig = plot(data, ylabel='Water Quality Parameters')
   fig.savefig('results.png')
   
   # 4. Generate report
   control_df = create_control_configuration()
   generate_plots_report(control_df, 'model_output/', 'report.md')

Batch Processing
~~~~~~~~~~~~~~~~

For processing multiple files:

.. code-block:: python

   import glob
   from cequalw2.fileio import read
   
   # Process all CSV files in directory
   files = glob.glob('model_output_*.csv')
   all_data = []
   
   for filepath in files:
       data = read(filepath, year=2023, data_columns=['temp', 'do'])
       data['source'] = filepath
       all_data.append(data)
   
   # Combine all data
   combined = pd.concat(all_data, ignore_index=True)

Performance Considerations
--------------------------

Memory Usage
~~~~~~~~~~~~

For large files, consider:

* Using HDF5 format for better performance
* Reading only required columns with ``data_columns`` parameter
* Processing data in chunks for very large datasets

File Format Selection
~~~~~~~~~~~~~~~~~~~~~

Choose appropriate formats based on your needs:

* **CSV**: Good for small to medium datasets, human-readable
* **HDF5**: Best for large datasets, compressed storage
* **SQLite**: Good for structured queries and database operations
* **Excel**: Good for data exchange and reporting

Optimization Tips
~~~~~~~~~~~~~~~~~

* Use ``data_columns`` parameter to read only needed columns
* Specify ``file_type`` explicitly to skip format detection
* Use vectorized operations with pandas for data processing
* Consider parallel processing for multiple files

Version Compatibility
---------------------

This documentation covers version 1.0.0 of the CE-QUAL-W2 Python Library.

**Supported Python Versions**: 3.7+

**Required Dependencies**:

* pandas >= 1.0.0
* numpy >= 1.18.0
* matplotlib >= 3.0.0
* seaborn >= 0.11.0

**Optional Dependencies**:

* holoviews >= 1.14.0 (for interactive plots)
* bokeh >= 2.0.0 (interactive plotting backend)
* openpyxl >= 3.0.0 (Excel support)
* h5py >= 2.10.0 (HDF5 support)
* PyYAML >= 5.0.0 (YAML configuration support)