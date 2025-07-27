Quick Start Guide
=================

This guide will get you up and running with the CE-QUAL-W2 Python Library in just a few minutes.

Basic Usage
-----------

Import and Read Data
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pandas as pd
    from cequalw2.fileio import read
    from cequalw2.utils import day_of_year_to_date
    from cequalw2.visualization import plot

    # Read CE-QUAL-W2 output file
    data = read('output.csv', year=2023, data_columns=['temp', 'do'])
    
    # Display basic information
    print(f"Data shape: {data.shape}")
    print(f"Columns: {data.columns.tolist()}")
    print(f"Date range: {data.index.min()} to {data.index.max()}")

Create Your First Plot
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Create a simple plot
    fig = plot(data, ylabel='Water Quality Parameters')
    fig.savefig('water_quality.png', dpi=300, bbox_inches='tight')
    
    # Show the plot
    fig.show()

Working with Dates
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Convert CE-QUAL-W2 day-of-year to datetime
    day_values = [1.0, 91.5, 182.0, 273.5, 365.0]
    dates = day_of_year_to_date(2023, day_values)
    
    for day, date in zip(day_values, dates):
        print(f"Day {day:6.1f} -> {date.strftime('%Y-%m-%d %H:%M')}")

Common File Formats
-------------------

CSV Files
~~~~~~~~~

.. code-block:: python

    # Read CSV with automatic format detection
    data = read('temperature_output.csv', year=2023, data_columns=['temperature'])
    
    # Or specify parameters explicitly
    from cequalw2.fileio import read_csv
    data = read_csv('output.csv', 
                    data_columns=['temp', 'do'], 
                    skiprows=3)

Fixed-Width Files (NPT/OPT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Read CE-QUAL-W2 NPT/OPT files
    data = read('output.npt', year=2023, data_columns=['temp', 'do'])

Excel Files
~~~~~~~~~~~

.. code-block:: python

    from cequalw2.fileio import read_excel
    
    # Read Excel file
    data = read_excel('model_output.xlsx', skiprows=2)

SQLite Database
~~~~~~~~~~~~~~~

.. code-block:: python

    from cequalw2.fileio import read_sqlite
    
    # Read from database
    data = read_sqlite('model_results.db')

Visualization Examples
----------------------

Single Plot
~~~~~~~~~~~

.. code-block:: python

    from cequalw2.visualization import plot, simple_plot
    
    # Plot all variables together
    fig = plot(data, ylabel='Values', title='Water Quality Time Series')
    
    # Plot single variable
    fig = simple_plot(data['temperature'], 
                      ylabel='Temperature (°C)', 
                      title='Temperature Over Time')

Multiple Subplots
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from cequalw2.visualization import multi_plot
    
    # Create subplots for each variable
    fig = multi_plot(data, 
                     ylabels=['Temperature (°C)', 'DO (mg/L)'],
                     title='Water Quality Parameters')

Custom Colors
~~~~~~~~~~~~~

.. code-block:: python

    from cequalw2.visualization import plot, k2, rainbow
    
    # Use built-in color palettes
    fig = plot(data, colors=k2, ylabel='Values')
    fig = plot(data, colors=rainbow, ylabel='Values')
    
    # Custom colors
    fig = plot(data, colors=['red', 'blue'], ylabel='Values')

Interactive Plots
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from cequalw2.visualization import hv_plot
    import holoviews as hv
    
    # Create interactive plot
    curves, tooltips = hv_plot(data, width=1200, height=400)
    
    # Display individual curves
    display(curves['temperature'])
    
    # Combine multiple curves
    overlay = hv.Overlay(list(curves.values()))
    display(overlay)

Data Analysis
-------------

Basic Statistics
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Descriptive statistics
    print(data.describe())
    
    # Monthly aggregation
    monthly_stats = data.resample('M').agg({
        'temperature': ['mean', 'min', 'max'],
        'do': ['mean', 'std']
    })
    print(monthly_stats)

Correlation Analysis
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Correlation matrix
    correlation = data.corr()
    print(correlation)
    
    # Plot correlation matrix
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
    plt.title('Parameter Correlation Matrix')
    plt.tight_layout()
    plt.savefig('correlation_matrix.png')

Data Export
-----------

Export to CSV
~~~~~~~~~~~~~

.. code-block:: python

    from cequalw2.analysis import write_csv
    
    # Export in CE-QUAL-W2 format
    write_csv(data, 'exported_data.csv', year=2023)

Export to HDF5
~~~~~~~~~~~~~~

.. code-block:: python

    from cequalw2.fileio import write_hdf
    
    # Export to HDF5 format
    write_hdf(data, group='water_quality', outfile='results.h5')

Export to Excel
~~~~~~~~~~~~~~~

.. code-block:: python

    # Export to Excel with multiple sheets
    with pd.ExcelWriter('results.xlsx') as writer:
        data.to_excel(writer, sheet_name='Raw Data')
        data.describe().to_excel(writer, sheet_name='Statistics')

Working with Multiple Files
---------------------------

Batch Processing
~~~~~~~~~~~~~~~~

.. code-block:: python

    import glob
    
    # Process multiple files
    file_list = glob.glob('model_output_*.csv')
    combined_data = []
    
    for filepath in file_list:
        df = read(filepath, year=2023, data_columns=['temp', 'do'])
        df['source'] = filepath
        combined_data.append(df)
    
    # Combine all data
    all_data = pd.concat(combined_data, ignore_index=True)

Parallel Processing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from concurrent.futures import ProcessPoolExecutor
    import multiprocessing as mp
    
    def process_file(filepath):
        return read(filepath, year=2023, data_columns=['temp', 'do'])
    
    # Process files in parallel
    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        results = list(executor.map(process_file, file_list))

Report Generation
-----------------

Create Analysis Report
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from cequalw2.analysis import generate_plots_report
    from cequalw2.fileio import read_plot_control
    
    # Read plot configuration
    control_df = read_plot_control('plot_control.yaml')
    
    # Generate report
    generate_plots_report(
        control_df,
        model_path='/path/to/model/output',
        outfile='model_report.md',
        title='Model Results Summary'
    )

Advanced Features
-----------------

Custom File Readers
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def read_custom_format(filepath, year):
        """Read custom CE-QUAL-W2 format"""
        # Read raw data with custom logic
        raw_data = pd.read_csv(filepath, skiprows=4, header=None)
        
        # Convert day-of-year to datetime
        dates = day_of_year_to_date(year, raw_data.iloc[:, 0].tolist())
        
        # Create DataFrame with datetime index
        df = pd.DataFrame(raw_data.iloc[:, 1:].values, 
                         index=dates,
                         columns=['temperature', 'dissolved_oxygen'])
        return df

SQL Queries
~~~~~~~~~~~

.. code-block:: python

    from cequalw2.analysis import sql_query
    
    # Custom SQL query on database
    query = """
    SELECT Date, Temperature, Dissolved_Oxygen 
    FROM results 
    WHERE Temperature > 20.0 
    ORDER BY Date
    """
    filtered_data = sql_query('model_results.db', query)

Next Steps
----------

Now that you've learned the basics, explore these advanced topics:

1. **Detailed API Reference**: Check the :doc:`api` for complete function documentation
2. **Advanced Examples**: See :doc:`user_guide` for comprehensive examples
3. **Data Visualization**: Learn more plotting techniques in the visualization module
4. **Performance Optimization**: Techniques for handling large datasets
5. **Integration**: Combine with other scientific Python libraries

Getting Help
------------

* **Documentation**: Full API documentation and examples
* **Examples**: Check the ``examples/`` directory in the repository
* **Issues**: Report bugs or request features on `GitHub <https://github.com/ecohydrology/cequalw2-Claude/issues>`_
* **Community**: Join discussions in GitHub issues and pull requests

Common Pitfalls
---------------

1. **Date Format**: Ensure your CE-QUAL-W2 files use day-of-year format starting from 1.0
2. **Column Names**: Use the exact column names from your data files
3. **File Paths**: Use absolute paths or ensure files are in the current working directory
4. **Memory Usage**: For large files, consider processing in chunks or using HDF5 format
5. **Missing Dependencies**: Install optional dependencies for full functionality

Tips for Success
----------------

1. **Start Simple**: Begin with basic file reading and plotting
2. **Check Data Quality**: Always inspect your data before analysis
3. **Use Virtual Environments**: Avoid package conflicts
4. **Save Your Work**: Export processed data in efficient formats
5. **Document Your Process**: Use Jupyter notebooks for reproducible analysis