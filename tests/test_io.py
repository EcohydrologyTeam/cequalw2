import pytest
import pandas as pd
from cequalw2.fileio import FileType, get_header_row_number, split_fixed_width_line


class TestIOReaders:
    def test_file_type_enum(self):
        """Test FileType enumeration values"""
        assert FileType.UNKNOWN.value == 0
        assert FileType.FIXED_WIDTH.value == 1
        assert FileType.CSV.value == 2

    def test_get_header_row_number_tsr_file(self):
        """Test header row number for TSR files"""
        assert get_header_row_number("/path/to/tsr_file.csv") == 0
        assert get_header_row_number("/path/to/TSR_FILE.csv") == 0
        assert get_header_row_number("/path/to/TsrData.txt") == 0

    def test_get_header_row_number_non_tsr_file(self):
        """Test header row number for non-TSR files"""
        assert get_header_row_number("/path/to/data_file.csv") == 2
        assert get_header_row_number("/path/to/output.txt") == 2
        assert get_header_row_number("/path/to/results.dat") == 2

    def test_split_fixed_width_line(self):
        """Test splitting fixed-width lines"""
        line = "ABC DEF GHI"
        result = split_fixed_width_line(line, 4)
        assert result == ["ABC ", "DEF ", "GHI"]

    def test_split_fixed_width_line_exact_width(self):
        """Test splitting when line length is exact multiple of field width"""
        line = "ABCDEFGH"
        result = split_fixed_width_line(line, 4)
        assert result == ["ABCD", "EFGH"]