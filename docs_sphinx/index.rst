CE-QUAL-W2 Python Library Documentation
========================================

Welcome to the CE-QUAL-W2 Python Library documentation!

This library provides tools for reading, writing, and visualizing CE-QUAL-W2 model data. CE-QUAL-W2 is a two-dimensional, vertically-averaged, hydrodynamic and water quality model used for simulating water movement, temperature, and concentrations of various chemical constituents in lakes, reservoirs, estuaries, and rivers.

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   installation
   quickstart
   user_guide

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api
   
.. toctree::
   :maxdepth: 2
   :caption: Development:

   examples
   testing
   contributing

Features
--------

* **File I/O**: Read various CE-QUAL-W2 file formats (CSV, fixed-width, SQLite, HDF5, Excel)
* **Date/Time Utilities**: Convert CE-QUAL-W2 day-of-year format to Python datetime objects  
* **Visualization**: Create plots and visualizations using matplotlib, seaborn, and holoviews
* **Analysis**: Statistical analysis and report generation tools
* **Flexible**: Automatic file type detection and multiple output format support

Quick Start
-----------

.. code-block:: python

    import pandas as pd
    from cequalw2.fileio import read, FileType
    from cequalw2.utils import day_of_year_to_date
    from cequalw2.visualization import plot

    # Read CE-QUAL-W2 output file
    data = read('output.csv', year=2023, data_columns=['temp', 'do'])

    # Convert day-of-year to datetime
    dates = day_of_year_to_date(2023, [1.0, 32.5, 91.0])

    # Create visualization
    fig = plot(data, ylabel='Temperature (°C)')

Installation
------------

From source (development mode):

.. code-block:: bash

    git clone https://github.com/ecohydrology/cequalw2-Claude.git
    cd cequalw2-Claude
    pip install -e .

Dependencies:

.. code-block:: bash

    pip install -r requirements.txt

