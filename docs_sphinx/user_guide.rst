User Guide
==========

This comprehensive guide covers all aspects of using the CE-QUAL-W2 Python Library.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Overview
--------

The CE-QUAL-W2 Python Library is designed to streamline the workflow for water quality modelers and researchers working with CE-QUAL-W2 output files. It provides tools for:

* Reading various file formats (CSV, NPT/OPT, Excel, SQLite, HDF5)
* Converting CE-QUAL-W2 date formats to Python datetime objects
* Creating publication-quality visualizations
* Performing statistical analysis and generating reports
* Exporting data in multiple formats

Core Concepts
-------------

File Types and Formats
~~~~~~~~~~~~~~~~~~~~~~~

CE-QUAL-W2 produces output in several formats:

**CSV Files**: Comma-separated values with day-of-year in the first column
**NPT/OPT Files**: Fixed-width format files for model output
**Excel Files**: Spreadsheet format for data exchange
**SQLite Databases**: Structured database storage for large datasets
**HDF5 Files**: High-performance format for scientific data

Date and Time Handling
~~~~~~~~~~~~~~~~~~~~~~

CE-QUAL-W2 uses a day-of-year format where:

* January 1 = 1.0
* January 1, 12:00 PM = 1.5
* December 31 = 365.0 (or 366.0 in leap years)

The library automatically converts these to Python datetime objects.

Data Structure
~~~~~~~~~~~~~~

The library returns pandas DataFrames with:

* **Index**: Datetime objects converted from day-of-year
* **Columns**: Water quality parameters (temperature, dissolved oxygen, etc.)
* **Values**: Numeric data from the model

File I/O Operations
-------------------

Reading Files
~~~~~~~~~~~~~

The main ``read()`` function automatically detects file format:

.. code-block:: python

    from cequalw2.fileio import read
    
    # Automatic format detection
    data = read('output.csv', year=2023, data_columns=['temp', 'do'])

Format-Specific Readers
~~~~~~~~~~~~~~~~~~~~~~~

For more control, use format-specific functions:

.. code-block:: python

    from cequalw2.fileio import read_csv, read_npt_opt, read_excel, read_sqlite
    
    # CSV files
    csv_data = read_csv('output.csv', data_columns=['temp'], skiprows=3)
    
    # Fixed-width files
    npt_data = read_npt_opt('output.npt', data_columns=['temp', 'do'])
    
    # Excel files
    excel_data = read_excel('data.xlsx', sheet_name='Results')
    
    # SQLite databases
    db_data = read_sqlite('results.db', table_name='output')

File Type Detection
~~~~~~~~~~~~~~~~~~~

The library uses several methods to detect file format:

1. **File Extension**: .csv, .npt, .opt, .xlsx, .db, .h5
2. **Content Analysis**: Examining file structure and delimiters
3. **User Specification**: Explicit file_type parameter

.. code-block:: python

    from cequalw2.fileio import FileType
    
    # Explicit format specification
    data = read('ambiguous_file.txt', 
                year=2023, 
                data_columns=['temp'],
                file_type=FileType.CSV)

Writing Files
~~~~~~~~~~~~~

Export data in various formats:

.. code-block:: python

    from cequalw2.analysis import write_csv
    from cequalw2.fileio import write_hdf
    
    # CE-QUAL-W2 CSV format
    write_csv(data, 'output.csv', year=2023)
    
    # HDF5 format
    write_hdf(data, group='results', outfile='data.h5')
    
    # Standard formats
    data.to_csv('standard.csv')
    data.to_excel('data.xlsx')

Date and Time Operations
------------------------

Basic Conversion
~~~~~~~~~~~~~~~~

Convert day-of-year values to datetime objects:

.. code-block:: python

    from cequalw2.utils import day_of_year_to_date
    
    # Single values
    dates = day_of_year_to_date(2023, [1.0, 91.5, 182.0])
    
    # Handle fractional days (time of day)
    noon_jan1 = day_of_year_to_date(2023, [1.5])[0]  # Jan 1, 12:00 PM

Leap Year Handling
~~~~~~~~~~~~~~~~~~

The library correctly handles leap years:

.. code-block:: python

    # Regular year (365 days)
    end_2023 = day_of_year_to_date(2023, [365.0])[0]
    
    # Leap year (366 days)
    end_2024 = day_of_year_to_date(2024, [366.0])[0]
    
    # February 29 in leap year
    feb29 = day_of_year_to_date(2024, [60.0])[0]

Time Rounding
~~~~~~~~~~~~~

Round datetime objects to specific intervals:

.. code-block:: python

    from cequalw2.utils import round_time
    import datetime
    
    dt = datetime.datetime(2023, 6, 15, 14, 37, 23)
    
    # Round to nearest hour
    rounded_hour = round_time(dt, round_to=3600)
    
    # Round to nearest 15 minutes
    rounded_15min = round_time(dt, round_to=900)

Working with DataFrames
~~~~~~~~~~~~~~~~~~~~~~~

Convert existing DataFrame columns:

.. code-block:: python

    import pandas as pd
    
    # DataFrame with day-of-year column
    df = pd.DataFrame({
        'day_of_year': [1.0, 32.5, 60.25, 91.0],
        'temperature': [4.2, 6.8, 12.1, 18.5]
    })
    
    # Convert to datetime index
    dates = day_of_year_to_date(2023, df['day_of_year'].tolist())
    df.index = dates
    df.drop('day_of_year', axis=1, inplace=True)

Data Visualization
------------------

Basic Plotting
~~~~~~~~~~~~~~

Create simple line plots:

.. code-block:: python

    from cequalw2.visualization import plot, simple_plot
    
    # Plot all variables
    fig = plot(data, ylabel='Water Quality Parameters')
    
    # Single variable
    fig = simple_plot(data['temperature'], ylabel='Temperature (°C)')

Multiple Subplots
~~~~~~~~~~~~~~~~~

Create separate subplots for each variable:

.. code-block:: python

    from cequalw2.visualization import multi_plot
    
    fig = multi_plot(data, 
                     ylabels=['Temperature (°C)', 'DO (mg/L)'],
                     title='Water Quality Time Series')

Color Palettes
~~~~~~~~~~~~~~

Use built-in or custom color schemes:

.. code-block:: python

    from cequalw2.visualization import k2, rainbow, everest
    
    # Built-in palettes
    fig = plot(data, colors=k2)
    fig = plot(data, colors=rainbow)
    fig = plot(data, colors=everest)
    
    # Custom colors
    fig = plot(data, colors=['red', 'blue', 'green'])
    
    # Seaborn palettes
    fig = multi_plot(data, palette='viridis')

Interactive Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~

Create interactive plots with HoloViews:

.. code-block:: python

    from cequalw2.visualization import hv_plot
    import holoviews as hv
    
    # Create interactive curves
    curves, tooltips = hv_plot(data, width=1200, height=400)
    
    # Display individual curves
    curves['temperature']
    
    # Combine multiple curves
    overlay = hv.Overlay(list(curves.values()))

Batch Plotting
~~~~~~~~~~~~~~

Generate multiple plots from configuration:

.. code-block:: python

    from cequalw2.visualization import plot_all_files
    from cequalw2.fileio import write_plot_control
    import pandas as pd
    
    # Create plot configuration
    config = pd.DataFrame({
        'Filename': ['temp.csv', 'do.csv'],
        'Columns': [['temperature'], ['dissolved_oxygen']],
        'Labels': [['Temperature (°C)'], ['DO (mg/L)']],
        'PlotType': ['combined', 'subplots']
    })
    
    # Save configuration
    write_plot_control(config, 'plot_config.yaml')
    
    # Generate all plots
    plot_all_files('plot_config.yaml', 
                   model_path='/path/to/data',
                   year=2023)

Advanced Visualization
~~~~~~~~~~~~~~~~~~~~~~

Customize plot appearance:

.. code-block:: python

    # Advanced styling
    fig = plot(data, 
               figsize=(15, 10),
               style='--',
               linewidth=2,
               alpha=0.8,
               grid=True,
               title='Custom Styled Plot')
    
    # Save with high quality
    fig.savefig('high_quality.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white')

Data Analysis and Statistics
----------------------------

Descriptive Statistics
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Basic statistics
    print(data.describe())
    
    # Custom statistics
    stats = data.agg({
        'temperature': ['mean', 'std', 'min', 'max'],
        'do': ['mean', 'median', 'std']
    })

Temporal Analysis
~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Resample to different frequencies
    daily_avg = data.resample('D').mean()
    weekly_avg = data.resample('W').mean()
    monthly_avg = data.resample('M').mean()
    
    # Seasonal analysis
    data['month'] = data.index.month
    seasonal = data.groupby('month').agg(['mean', 'std'])

Correlation Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Correlation matrix
    correlation = data.corr()
    
    # Visualize correlations
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='RdBu_r', center=0)
    plt.title('Parameter Correlations')

Quality Control
~~~~~~~~~~~~~~~

Check data quality and identify issues:

.. code-block:: python

    def quality_check(df):
        """Perform data quality assessment"""
        issues = []
        
        # Missing values
        missing = df.isnull().sum()
        if missing.any():
            issues.append(f"Missing values: {missing[missing > 0].to_dict()}")
        
        # Outliers (using IQR method)
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | 
                       (df[col] > (Q3 + 1.5 * IQR))).sum()
            if outliers > 0:
                issues.append(f"{col}: {outliers} potential outliers")
        
        return issues

Report Generation
-----------------

Automated Reports
~~~~~~~~~~~~~~~~~

Generate comprehensive analysis reports:

.. code-block:: python

    from cequalw2.analysis import generate_plots_report
    
    # Create detailed report
    generate_plots_report(
        plot_config,
        model_path='/path/to/data',
        outfile='comprehensive_report.md',
        title='Model Analysis Report',
        subtitle='Lake Example Study',
        pdf_report=True  # Requires pandoc
    )

Custom Reports
~~~~~~~~~~~~~~

Create custom analysis reports:

.. code-block:: python

    def create_summary_report(data, filename):
        """Create custom summary report"""
        with open(filename, 'w') as f:
            f.write("# Water Quality Analysis Report\n\n")
            
            # Basic info
            f.write(f"## Dataset Overview\n")
            f.write(f"* Records: {len(data)}\n")
            f.write(f"* Parameters: {len(data.columns)}\n")
            f.write(f"* Date range: {data.index.min()} to {data.index.max()}\n\n")
            
            # Statistics
            f.write("## Summary Statistics\n")
            f.write(data.describe().to_markdown())
            f.write("\n\n")
            
            # Correlations
            f.write("## Parameter Correlations\n")
            f.write(data.corr().round(3).to_markdown())

Database Operations
-------------------

SQLite Integration
~~~~~~~~~~~~~~~~~~

Work with SQLite databases:

.. code-block:: python

    from cequalw2.analysis import sql_query
    from cequalw2.fileio import read_sqlite
    
    # Read entire database
    data = read_sqlite('model.db')
    
    # Custom queries
    query = """
    SELECT Date, Temperature, Dissolved_Oxygen
    FROM results 
    WHERE Temperature BETWEEN 15 AND 25
    AND Dissolved_Oxygen > 5.0
    ORDER BY Date
    """
    filtered = sql_query('model.db', query)

Creating Databases
~~~~~~~~~~~~~~~~~~

Export data to SQLite:

.. code-block:: python

    import sqlite3
    import pandas as pd
    
    # Create database connection
    conn = sqlite3.connect('output.db')
    
    # Write DataFrame to database
    data.to_sql('water_quality', conn, if_exists='replace', index=True)
    
    # Close connection
    conn.close()

Performance Optimization
------------------------

Memory Management
~~~~~~~~~~~~~~~~~

For large datasets:

.. code-block:: python

    # Read in chunks for large files
    def read_large_file(filepath, year, chunksize=10000):
        chunks = []
        for chunk in pd.read_csv(filepath, chunksize=chunksize):
            # Process chunk
            processed_chunk = process_data(chunk, year)
            chunks.append(processed_chunk)
        return pd.concat(chunks, ignore_index=True)

Parallel Processing
~~~~~~~~~~~~~~~~~~~

Process multiple files in parallel:

.. code-block:: python

    from concurrent.futures import ProcessPoolExecutor
    import multiprocessing as mp
    
    def process_file_parallel(file_args):
        filepath, year, columns = file_args
        return read(filepath, year=year, data_columns=columns)
    
    # Prepare arguments
    file_args = [(f, 2023, ['temp', 'do']) for f in file_list]
    
    # Process in parallel
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        results = list(executor.map(process_file_parallel, file_args))

Efficient Storage
~~~~~~~~~~~~~~~~~

Use HDF5 for large datasets:

.. code-block:: python

    from cequalw2.fileio import write_hdf, read_hdf
    
    # Write compressed HDF5
    write_hdf(large_dataset, 
              group='data', 
              outfile='large_data.h5',
              compression='gzip')
    
    # Read specific variables only
    subset = read_hdf(group='data', 
                      infile='large_data.h5',
                      variables=['temperature'])

Integration with Other Libraries
--------------------------------

Scientific Python Ecosystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Combine with other scientific libraries:

.. code-block:: python

    # NumPy for numerical operations
    import numpy as np
    
    # SciPy for advanced analysis
    from scipy import stats
    from scipy.signal import savgol_filter
    
    # Smooth data
    data['temp_smooth'] = savgol_filter(data['temperature'], 11, 3)
    
    # Statistical tests
    statistic, p_value = stats.normaltest(data['temperature'])

Machine Learning
~~~~~~~~~~~~~~~~

Integrate with scikit-learn:

.. code-block:: python

    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.cluster import KMeans
    
    # Prepare features
    features = data[['temperature', 'do', 'ph']].dropna()
    
    # Standardize
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Principal Component Analysis
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(features_scaled)
    
    # Clustering
    kmeans = KMeans(n_clusters=3)
    clusters = kmeans.fit_predict(features_scaled)

GIS Integration
~~~~~~~~~~~~~~~

Work with spatial data:

.. code-block:: python

    # With GeoPandas for spatial analysis
    import geopandas as gpd
    
    # Add spatial information
    data['latitude'] = 45.0  # Example coordinates
    data['longitude'] = -120.0
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        data, 
        geometry=gpd.points_from_xy(data.longitude, data.latitude)
    )

Best Practices
--------------

Code Organization
~~~~~~~~~~~~~~~~~

Structure your analysis code:

.. code-block:: python

    # config.py
    YEAR = 2023
    DATA_PATH = '/path/to/data'
    OUTPUT_PATH = '/path/to/output'
    COLUMNS = ['temperature', 'dissolved_oxygen', 'ph']
    
    # analysis.py
    from config import *
    from cequalw2.fileio import read
    from cequalw2.visualization import plot
    
    def load_data():
        return read(f'{DATA_PATH}/output.csv', year=YEAR, data_columns=COLUMNS)
    
    def create_plots(data):
        fig = plot(data, ylabel='Water Quality')
        fig.savefig(f'{OUTPUT_PATH}/water_quality.png')

Error Handling
~~~~~~~~~~~~~~

Implement robust error handling:

.. code-block:: python

    def safe_read_file(filepath, year, columns):
        """Safely read file with error handling"""
        try:
            data = read(filepath, year=year, data_columns=columns)
            return data
        except FileNotFoundError:
            print(f"Warning: File not found: {filepath}")
            return None
        except Exception as e:
            print(f"Error reading {filepath}: {str(e)}")
            return None

Documentation
~~~~~~~~~~~~~

Document your analysis:

.. code-block:: python

    def analyze_water_quality(data):
        """
        Perform comprehensive water quality analysis.
        
        Parameters:
        -----------
        data : pd.DataFrame
            Water quality data with datetime index
            
        Returns:
        --------
        dict : Analysis results including statistics and plots
        """
        results = {}
        
        # Calculate statistics
        results['stats'] = data.describe()
        
        # Generate plots
        results['figure'] = plot(data)
        
        return results

Testing
~~~~~~~

Write tests for your functions:

.. code-block:: python

    import pytest
    import pandas as pd
    from cequalw2.utils import day_of_year_to_date
    
    def test_date_conversion():
        """Test date conversion functionality"""
        dates = day_of_year_to_date(2023, [1.0, 365.0])
        assert len(dates) == 2
        assert dates[0].year == 2023
        assert dates[0].month == 1
        assert dates[0].day == 1

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Memory Errors with Large Files**

* Use chunked reading for very large files
* Process data in smaller segments
* Use HDF5 format for better performance

**Date Conversion Problems**

* Ensure day-of-year values are in correct range (1.0-365.0/366.0)
* Check for leap years when using day 366
* Verify time zone assumptions

**Plot Display Issues**

* Use ``fig.show()`` for interactive environments
* Set appropriate figure size with ``figsize`` parameter
* Check matplotlib backend configuration

**Import Errors**

* Verify all dependencies are installed
* Check virtual environment activation
* Update package versions if necessary

Getting Help
------------

When you encounter issues:

1. **Check the examples** in this documentation
2. **Read the API reference** for detailed function descriptions
3. **Search GitHub issues** for similar problems
4. **Create a new issue** with minimal reproducible example
5. **Include your environment details** (Python version, OS, package versions)

Contributing
------------

To contribute to the library:

1. **Fork the repository** on GitHub
2. **Create a feature branch** for your changes
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with clear description

See the :doc:`contributing` guide for detailed instructions.