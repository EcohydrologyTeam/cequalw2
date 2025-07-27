Installation
============

This guide covers the installation process for the CE-QUAL-W2 Python Library.

Requirements
------------

* Python 3.7 or higher
* pip package manager

Dependencies
------------

The library depends on the following Python packages:

Required Dependencies
~~~~~~~~~~~~~~~~~~~~~

* pandas >= 1.0.0 - Data manipulation and analysis
* numpy >= 1.18.0 - Numerical computing
* matplotlib >= 3.0.0 - Plotting and visualization
* seaborn >= 0.11.0 - Statistical data visualization

Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~

* holoviews >= 1.14.0 - Interactive visualizations
* bokeh >= 2.0.0 - Interactive plotting backend
* openpyxl >= 3.0.0 - Excel file support
* h5py >= 2.10.0 - HDF5 file support
* PyYAML >= 5.0.0 - YAML configuration file support
* pandoc - For PDF report generation

Installation Methods
--------------------

From Source (Recommended for Development)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you plan to modify the code or contribute to the project:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/ecohydrology/cequalw2-Claude.git
    cd cequalw2-Claude

    # Create virtual environment (recommended)
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

    # Install in development mode
    pip install -e .

    # Install development dependencies (optional)
    pip install -r requirements-dev.txt

From PyPI (When Available)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    pip install cequalw2

Virtual Environment Setup
--------------------------

It's recommended to use a virtual environment to avoid conflicts with other packages:

Using venv (Python 3.3+)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Create virtual environment
    python -m venv cequalw2_env

    # Activate virtual environment
    # On Linux/macOS:
    source cequalw2_env/bin/activate
    # On Windows:
    cequalw2_env\Scripts\activate

    # Install the library
    pip install cequalw2

Using conda
~~~~~~~~~~~

.. code-block:: bash

    # Create conda environment
    conda create -n cequalw2 python=3.9
    conda activate cequalw2

    # Install dependencies
    conda install pandas matplotlib seaborn numpy

    # Install the library
    pip install cequalw2

Verification
------------

To verify that the installation was successful:

.. code-block:: python

    import cequalw2
    print(f"CE-QUAL-W2 Python Library version: {cequalw2.__version__}")

    # Test basic functionality
    from cequalw2.utils import day_of_year_to_date
    dates = day_of_year_to_date(2023, [1.0, 91.5])
    print(f"Test successful: {dates}")

Installation Troubleshooting
-----------------------------

Common Issues
~~~~~~~~~~~~~

**Import Error: No module named 'cequalw2'**

* Ensure you've activated the correct virtual environment
* Try reinstalling: ``pip uninstall cequalw2 && pip install cequalw2``
* For development installation, use ``pip install -e .`` in the project directory

**Missing Dependencies**

If you encounter missing dependency errors:

.. code-block:: bash

    # Install all required dependencies
    pip install pandas numpy matplotlib seaborn

    # For optional features
    pip install holoviews bokeh openpyxl h5py PyYAML

**Permission Errors**

On some systems, you might need to use ``--user`` flag:

.. code-block:: bash

    pip install --user cequalw2

**Windows-specific Issues**

* Install Microsoft Visual C++ Build Tools if you encounter compilation errors
* Use Anaconda or Miniconda for easier dependency management on Windows

Platform-Specific Notes
------------------------

Windows
~~~~~~~

* Consider using Anaconda for easier package management
* Some plotting features may require additional configuration

macOS
~~~~~

* No special requirements beyond standard Python installation
* Homebrew Python is recommended over system Python

Linux
~~~~~

* Most distributions work out of the box
* May need to install python3-dev for some dependencies:

.. code-block:: bash

    # Ubuntu/Debian
    sudo apt-get install python3-dev

    # CentOS/RHEL
    sudo yum install python3-devel

Development Installation
------------------------

For contributors and developers:

.. code-block:: bash

    # Clone and enter directory
    git clone https://github.com/ecohydrology/cequalw2-Claude.git
    cd cequalw2-Claude

    # Install in development mode with all dependencies
    pip install -e ".[dev]"

    # Or install development requirements separately
    pip install -e .
    pip install -r requirements-dev.txt

    # Run tests to verify installation
    pytest tests/

    # Install pre-commit hooks (optional)
    pre-commit install

Docker Installation
-------------------

For containerized environments:

.. code-block:: dockerfile

    FROM python:3.9-slim

    WORKDIR /app

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        git \
        && rm -rf /var/lib/apt/lists/*

    # Install Python dependencies
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # Install CE-QUAL-W2 library
    RUN pip install cequalw2

    COPY . .

Updating
--------

To update to the latest version:

.. code-block:: bash

    # From PyPI
    pip install --upgrade cequalw2

    # From source (development)
    cd cequalw2-Claude
    git pull origin main
    pip install -e .

Getting Help
------------

If you encounter installation issues:

1. Check the `troubleshooting section <troubleshooting.html>`_
2. Search existing `GitHub issues <https://github.com/ecohydrology/cequalw2-Claude/issues>`_
3. Create a new issue with:
   * Your operating system and Python version
   * Complete error message
   * Steps you've already tried