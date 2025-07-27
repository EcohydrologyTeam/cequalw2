# Usage Examples

This document provides comprehensive examples for using the CE-QUAL-W2 Python library.

## Table of Contents

- [Basic Usage](#basic-usage)
- [File I/O Operations](#file-io-operations)
- [Date/Time Handling](#datetime-handling)
- [Data Visualization](#data-visualization)
- [Analysis and Reporting](#analysis-and-reporting)
- [Advanced Examples](#advanced-examples)

## Basic Usage

### Quick Start Example

```python
import pandas as pd
from cequalw2.fileio import read
from cequalw2.utils import day_of_year_to_date
from cequalw2.visualization import plot

# Read model output
data = read('temperature_output.csv', year=2023, data_columns=['temp', 'do'])

# Create visualization
fig = plot(data, ylabel='Values', title='Water Quality Time Series')
fig.savefig('water_quality.png', dpi=300, bbox_inches='tight')

print(f"Data shape: {data.shape}")
print(f"Date range: {data.index.min()} to {data.index.max()}")
```

## File I/O Operations

### Reading Different File Formats

#### CSV Files

```python
from cequalw2.fileio import read, read_csv

# Auto-detect CSV format
data = read('output.csv', year=2023, data_columns=['temperature', 'dissolved_oxygen'])

# Direct CSV reading
data = read_csv('output.csv', data_columns=['temperature', 'dissolved_oxygen'], skiprows=3)

# Custom header rows
data = read('data.csv', year=2023, data_columns=['flow'], skiprows=5)
```

#### Fixed-Width Files (NPT/OPT)

```python
from cequalw2.fileio import read, read_npt_opt, FileType

# Auto-detect fixed-width format
data = read('output.npt', year=2023, data_columns=['temp', 'do'])

# Explicitly specify format
data = read('output.opt', year=2023, data_columns=['temp', 'do'], 
            file_type=FileType.FIXED_WIDTH)

# Direct fixed-width reading
data = read_npt_opt('output.npt', data_columns=['temp', 'do'])
```

#### Excel Files

```python
from cequalw2.fileio import read_excel

# Read Excel file
data = read_excel('model_output.xlsx', skiprows=2)

# Read specific sheet
data = read_excel('model_output.xlsx', sheet_name='Results')
```

#### SQLite Databases

```python
from cequalw2.fileio import read_sqlite
from cequalw2.analysis import sql_query

# Read entire first table
data = read_sqlite('model_results.db')

# Custom SQL query
query = """
SELECT Date, Temperature, Dissolved_Oxygen 
FROM results 
WHERE Temperature > 20.0 
ORDER BY Date
"""
filtered_data = sql_query('model_results.db', query)
```

#### HDF5 Files

```python
from cequalw2.fileio import write_hdf, read_hdf
import pandas as pd

# Write data to HDF5
df = pd.DataFrame({'temp': [15, 16, 17], 'do': [8, 7.5, 7]})
write_hdf(df, group='water_quality', outfile='data.h5')

# Read data from HDF5
data = read_hdf(group='water_quality', infile='data.h5', 
                variables=['temp', 'do'])
```

### Batch File Processing

```python
import glob
from cequalw2.fileio import read
import pandas as pd

# Process multiple files
data_files = glob.glob('model_output_*.csv')
all_data = []

for file in data_files:
    df = read(file, year=2023, data_columns=['temp', 'do'])
    df['source_file'] = file
    all_data.append(df)

# Combine all data
combined_data = pd.concat(all_data, ignore_index=True)
```

## Date/Time Handling

### Basic Date Conversion

```python
from cequalw2.utils import day_of_year_to_date, round_time
import datetime

# Convert single day-of-year value
dates = day_of_year_to_date(2023, [91.5])  # April 1, 2023 at noon
print(dates[0])  # 2023-04-01 12:00:00

# Convert multiple values
day_values = [1.0, 32.5, 60.25, 91.0, 121.5, 152.0, 182.5, 213.0, 244.0, 274.5, 305.0, 335.5]
dates = day_of_year_to_date(2023, day_values)

for doy, date in zip(day_values, dates):
    print(f"Day {doy:6.2f} -> {date.strftime('%Y-%m-%d %H:%M')}")
```

### Working with Leap Years

```python
from cequalw2.utils import day_of_year_to_date

# Regular year (365 days)
regular_year_end = day_of_year_to_date(2023, [365.0])[0]
print(f"2023 ends: {regular_year_end}")

# Leap year (366 days)
leap_year_end = day_of_year_to_date(2024, [366.0])[0]
print(f"2024 ends: {leap_year_end}")

# February 29 in leap year
feb29 = day_of_year_to_date(2024, [60.0])[0]
print(f"Feb 29, 2024: {feb29}")
```

### Time Rounding

```python
from cequalw2.utils import round_time
import datetime

# Round to nearest hour
dt = datetime.datetime(2023, 6, 15, 14, 37, 23)
rounded_hour = round_time(dt, round_to=3600)  # 3600 seconds = 1 hour
print(f"Original: {dt}")
print(f"Rounded:  {rounded_hour}")

# Round to nearest 15 minutes
rounded_15min = round_time(dt, round_to=900)  # 900 seconds = 15 minutes
print(f"15min:    {rounded_15min}")
```

### DataFrame Index Conversion

```python
import pandas as pd
from cequalw2.utils import day_of_year_to_date

# Create sample data with day-of-year index
df = pd.DataFrame({
    'day_of_year': [1.0, 32.5, 60.25, 91.0, 121.5],
    'temperature': [4.2, 6.8, 12.1, 18.5, 22.3],
    'dissolved_oxygen': [12.1, 11.8, 10.2, 8.9, 7.8]
})

# Convert day-of-year to datetime index
df['datetime'] = day_of_year_to_date(2023, df['day_of_year'].tolist())
df.set_index('datetime', inplace=True)
df.drop('day_of_year', axis=1, inplace=True)

print(df)
```

## Data Visualization

### Basic Plotting

```python
from cequalw2.visualization import plot, multi_plot, simple_plot
import pandas as pd

# Sample data
df = pd.DataFrame({
    'temperature': [15.2, 15.5, 16.1, 16.8, 17.2, 18.1, 19.2],
    'dissolved_oxygen': [8.5, 8.3, 8.1, 7.9, 7.7, 7.4, 7.1],
    'ph': [7.8, 7.9, 8.0, 8.1, 8.0, 7.9, 7.8]
}, index=pd.date_range('2023-01-01', periods=7, freq='D'))

# Single plot with all variables
fig = plot(df, ylabel='Concentration', title='Water Quality Parameters')
fig.savefig('all_parameters.png')

# Separate subplots
fig = multi_plot(df, 
                 ylabels=['Temperature (°C)', 'DO (mg/L)', 'pH'],
                 title='Water Quality Time Series')
fig.savefig('subplots.png')

# Single variable plot
fig = simple_plot(df['temperature'], 
                  ylabel='Temperature (°C)',
                  title='Temperature Over Time')
```

### Custom Styling

```python
from cequalw2.visualization import plot, k2, rainbow, everest

# Use built-in color palettes
fig = plot(df, colors=k2, ylabel='Values', title='K2 Color Palette')
fig = plot(df, colors=rainbow, ylabel='Values', title='Rainbow Palette')
fig = plot(df, colors=everest, ylabel='Values', title='Everest Palette')

# Custom styling
fig = plot(df, 
           colors=['red', 'blue', 'green'],
           style='--',
           figsize=(12, 8),
           ylabel='Water Quality Parameters')

# Seaborn palette
fig = multi_plot(df, palette='viridis', figsize=(15, 12))
```

### Interactive Plots with HoloViews

```python
from cequalw2.visualization import hv_plot
import holoviews as hv

# Create interactive plot
curves, tooltips = hv_plot(df, width=1200, height=400)

# Display first curve
display(curves['temperature'])

# Combine multiple curves
overlay = hv.Overlay([curves[col] for col in df.columns])
display(overlay)
```

### Batch Plotting from Control File

```python
from cequalw2.visualization import plot_all_files
from cequalw2.fileio import write_plot_control
import pandas as pd

# Create plot control configuration
plot_control = pd.DataFrame({
    'Filename': ['temp.csv', 'do.csv', 'flow.csv'],
    'Columns': [['temperature'], ['dissolved_oxygen'], ['flow_rate']],
    'Labels': [['Temperature (°C)'], ['DO (mg/L)'], ['Flow (m³/s)']],
    'PlotType': ['combined', 'combined', 'subplots']
})

# Write control file
write_plot_control(plot_control, 'plot_control.yaml')

# Generate all plots
plot_all_files('plot_control.yaml', 
               model_path='/path/to/model/output',
               year=2023,
               filetype='png',
               VERBOSE=True)
```

## Analysis and Reporting

### Statistical Analysis

```python
import pandas as pd
import numpy as np

# Load data
df = read('water_quality.csv', year=2023, data_columns=['temp', 'do', 'ph'])

# Basic statistics
print("Descriptive Statistics:")
print(df.describe())

# Monthly aggregation
monthly_stats = df.resample('M').agg({
    'temp': ['mean', 'min', 'max', 'std'],
    'do': ['mean', 'min', 'max'],
    'ph': ['mean', 'std']
})

print("\nMonthly Statistics:")
print(monthly_stats)

# Correlation analysis
correlation_matrix = df.corr()
print("\nCorrelation Matrix:")
print(correlation_matrix)
```

### Report Generation

```python
from cequalw2.analysis import generate_plots_report
from cequalw2.fileio import read_plot_control

# Read plot configuration
control_df = read_plot_control('plot_control.yaml')

# Generate comprehensive report
generate_plots_report(
    control_df, 
    model_path='/path/to/model/output',
    outfile='model_report.md',
    title='CE-QUAL-W2 Model Results Summary',
    subtitle='Water Quality Analysis for Lake Example',
    file_type='png',
    pdf_report=False
)

# Generate PDF report (requires pandoc)
generate_plots_report(
    control_df,
    model_path='/path/to/model/output', 
    outfile='model_report_pdf.md',
    title='Model Results',
    pdf_report=True
)
```

### Data Export

```python
from cequalw2.analysis import write_csv
from cequalw2.fileio import write_hdf

# Export to CE-QUAL-W2 CSV format
write_csv(df, 'exported_data.csv', year=2023, 
          header='CE-QUAL-W2 Export\nGenerated by Python Library\n')

# Export to HDF5
write_hdf(df, group='processed_data', outfile='results.h5')

# Export to Excel with multiple sheets
with pd.ExcelWriter('model_results.xlsx') as writer:
    df.to_excel(writer, sheet_name='Raw Data')
    monthly_stats.to_excel(writer, sheet_name='Monthly Statistics')
    correlation_matrix.to_excel(writer, sheet_name='Correlations')
```

## Advanced Examples

### Data Quality Checking

```python
import numpy as np

def check_data_quality(df):
    """Perform data quality checks"""
    issues = []
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        issues.append(f"Missing values: {missing[missing > 0].to_dict()}")
    
    # Check for negative temperatures (physical impossibility in Celsius)
    if 'temperature' in df.columns:
        neg_temp = (df['temperature'] < -50).sum()
        if neg_temp > 0:
            issues.append(f"Suspicious temperatures: {neg_temp} values < -50°C")
    
    # Check for unrealistic DO values
    if 'dissolved_oxygen' in df.columns:
        high_do = (df['dissolved_oxygen'] > 20).sum()
        neg_do = (df['dissolved_oxygen'] < 0).sum()
        if high_do > 0:
            issues.append(f"High DO values: {high_do} values > 20 mg/L")
        if neg_do > 0:
            issues.append(f"Negative DO values: {neg_do} values < 0")
    
    return issues

# Check data quality
quality_issues = check_data_quality(df)
if quality_issues:
    print("Data Quality Issues Found:")
    for issue in quality_issues:
        print(f"  - {issue}")
else:
    print("Data quality check passed!")
```

### Custom File Readers

```python
def read_custom_format(filepath, year, column_mapping):
    """
    Read custom CE-QUAL-W2 format with flexible column mapping
    """
    # Read raw data
    raw_data = pd.read_csv(filepath, skiprows=4, header=None)
    
    # Apply column mapping
    raw_data.columns = ['day_of_year'] + list(column_mapping.keys())
    
    # Convert day-of-year to datetime
    dates = day_of_year_to_date(year, raw_data['day_of_year'].tolist())
    raw_data.index = dates
    raw_data.drop('day_of_year', axis=1, inplace=True)
    
    # Rename columns to standard names
    raw_data.rename(columns=column_mapping, inplace=True)
    
    return raw_data

# Usage
column_map = {
    'col1': 'temperature',
    'col2': 'dissolved_oxygen', 
    'col3': 'ph'
}

custom_data = read_custom_format('custom_output.txt', 2023, column_map)
```

### Performance Optimization

```python
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

def process_file_chunk(file_list):
    """Process a chunk of files in parallel"""
    results = []
    for filepath in file_list:
        df = read(filepath, year=2023, data_columns=['temp', 'do'])
        # Perform analysis
        monthly_avg = df.resample('M').mean()
        results.append({
            'file': filepath,
            'data': monthly_avg
        })
    return results

def parallel_processing(file_list, n_cores=None):
    """Process multiple files in parallel"""
    if n_cores is None:
        n_cores = mp.cpu_count()
    
    # Split files into chunks
    chunk_size = len(file_list) // n_cores
    chunks = [file_list[i:i + chunk_size] for i in range(0, len(file_list), chunk_size)]
    
    # Process in parallel
    with ProcessPoolExecutor(max_workers=n_cores) as executor:
        results = list(executor.map(process_file_chunk, chunks))
    
    # Flatten results
    all_results = []
    for chunk_result in results:
        all_results.extend(chunk_result)
    
    return all_results

# Usage
file_list = ['output_1.csv', 'output_2.csv', 'output_3.csv']
start_time = time.time()
results = parallel_processing(file_list)
end_time = time.time()

print(f"Processed {len(file_list)} files in {end_time - start_time:.2f} seconds")
```

### Integration with Other Libraries

```python
# Integration with scikit-learn for ML analysis
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Prepare data for ML
features = df[['temperature', 'dissolved_oxygen', 'ph']].dropna()

# Principal Component Analysis
pca = PCA(n_components=2)
pca_result = pca.fit_transform(features)

# Clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(features)

# Visualize results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# PCA plot
ax1.scatter(pca_result[:, 0], pca_result[:, 1], c=clusters, cmap='viridis')
ax1.set_title('PCA of Water Quality Parameters')
ax1.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
ax1.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')

# Time series with clusters
ax2.scatter(df.index, df['temperature'], c=clusters, cmap='viridis')
ax2.set_title('Temperature Time Series with Clusters')
ax2.set_xlabel('Date')
ax2.set_ylabel('Temperature (°C)')

plt.tight_layout()
plt.savefig('ml_analysis.png')
```

These examples demonstrate the full range of capabilities of the CE-QUAL-W2 Python library, from basic file operations to advanced analysis and visualization techniques.