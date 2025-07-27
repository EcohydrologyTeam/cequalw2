import pytest
import datetime
from cequalw2.utils import day_of_year_to_date


class TestDateTimeUtils:
    def test_day_of_year_to_date_single_value(self):
        """Test conversion of a single day-of-year value"""
        result = day_of_year_to_date(2023, [1.5])
        expected = [datetime.datetime(2023, 1, 1, 12, 0)]
        assert result == expected

    def test_day_of_year_to_date_multiple_values(self):
        """Test conversion of multiple day-of-year values"""
        result = day_of_year_to_date(2023, [1.0, 32.5, 365.0])
        expected = [
            datetime.datetime(2023, 1, 1, 0, 0),
            datetime.datetime(2023, 2, 1, 12, 0),
            datetime.datetime(2023, 12, 31, 0, 0)
        ]
        assert result == expected

    def test_day_of_year_to_date_leap_year(self):
        """Test conversion in a leap year"""
        result = day_of_year_to_date(2024, [366.0])
        expected = [datetime.datetime(2024, 12, 31, 0, 0)]
        assert result == expected

    def test_day_of_year_to_date_empty_list(self):
        """Test conversion with empty list"""
        result = day_of_year_to_date(2023, [])
        assert result == []