#!/usr/bin/env python
"""
Basic usage example for the cequalw2 library
"""

import pandas as pd
from cequalw2.fileio import read, FileType
from cequalw2.utils import day_of_year_to_date
from cequalw2.visualization import plot, multi_plot


def main():
    """
    Example of basic cequalw2 library usage
    """
    
    # Example 1: Reading a CE-QUAL-W2 output file
    print("Example 1: Reading CE-QUAL-W2 data")
    print("-" * 40)
    
    # Note: Replace with actual file path
    # data = read('path/to/your/output.csv', year=2023, data_columns=['temp', 'do'], file_type=FileType.CSV)
    
    # Example 2: Converting day-of-year to datetime
    print("\nExample 2: Converting CE-QUAL-W2 day-of-year to datetime")
    print("-" * 40)
    
    year = 2023
    day_of_year_values = [1.0, 32.5, 60.25, 91.0, 121.5]
    
    dates = day_of_year_to_date(year, day_of_year_values)
    
    for doy, date in zip(day_of_year_values, dates):
        print(f"Day {doy:6.2f} -> {date}")
    
    # Example 3: Creating a sample dataframe
    print("\nExample 3: Working with CE-QUAL-W2 data")
    print("-" * 40)
    
    # Create sample data
    sample_data = pd.DataFrame({
        'JDAY': [1.0, 2.0, 3.0, 4.0, 5.0],
        'Temperature': [15.2, 15.5, 16.1, 16.8, 17.2],
        'Dissolved_Oxygen': [8.5, 8.3, 8.1, 7.9, 7.7]
    })
    
    print("Sample data:")
    print(sample_data)
    
    # Convert JDAY to datetime
    sample_data['DateTime'] = day_of_year_to_date(2023, sample_data['JDAY'].tolist())
    
    print("\nData with datetime:")
    print(sample_data[['DateTime', 'Temperature', 'Dissolved_Oxygen']])


if __name__ == "__main__":
    main()