"""
Tests for argument validation regexes.
Tests time format and date format validation.
"""
import re
import pytest


# Time validation regex from timegrep
TIME_VALIDATION_PATTERN = (
    r'(^[2][0-3]|[0-1][0-9]):[0-5][0-9](:[0-5][0-9])?$'
)

# Date validation pattern (YYYY-mm-dd)
DATE_VALIDATION_PATTERN = (
    r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$'
)


class TestTimeValidation:
    """Test time format validation."""

    def test_valid_time_hh_mm(self):
        """Test valid time format hh:mm."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("14:30") is not None
        assert pattern.match("00:00") is not None
        assert pattern.match("23:59") is not None

    def test_valid_time_hh_mm_ss(self):
        """Test valid time format hh:mm:ss."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("14:30:45") is not None
        assert pattern.match("00:00:00") is not None
        assert pattern.match("23:59:59") is not None

    def test_invalid_time_bad_hour(self):
        """Test invalid hour values."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("24:00") is None
        assert pattern.match("25:30") is None
        assert pattern.match("-1:30") is None

    def test_invalid_time_bad_minute(self):
        """Test invalid minute values."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("14:60") is None
        assert pattern.match("14:70") is None
        assert pattern.match("14:-1") is None

    def test_invalid_time_bad_second(self):
        """Test invalid second values."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("14:30:60") is None
        assert pattern.match("14:30:70") is None
        assert pattern.match("14:30:-1") is None

    def test_invalid_time_missing_colon(self):
        """Test time missing colons."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("1430") is None
        assert pattern.match("143045") is None

    def test_invalid_time_extra_colons(self):
        """Test time with too many colons."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("14:30:45:00") is None
        assert pattern.match("::14:30") is None

    def test_edge_case_times(self):
        """Test edge case times."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        # Midnight
        assert pattern.match("00:00") is not None
        assert pattern.match("00:00:00") is not None
        # One second before midnight
        assert pattern.match("23:59:59") is not None
        # Noon
        assert pattern.match("12:00:00") is not None

    def test_midnight_hour_boundary(self):
        """Test hour boundary (0-23 valid, 24+ invalid)."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        # 20:xx is valid (2 followed by 0-3)
        assert pattern.match("20:00") is not None
        assert pattern.match("23:00") is not None
        # 24:xx is invalid
        assert pattern.match("24:00") is None

    def test_no_leading_spaces(self):
        """Test time with leading spaces is invalid."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match(" 14:30") is None
        assert pattern.match("  14:30:45") is None

    def test_no_trailing_spaces(self):
        """Test time with trailing spaces is invalid."""
        pattern = re.compile(TIME_VALIDATION_PATTERN)
        assert pattern.match("14:30 ") is None
        assert pattern.match("14:30:45 ") is None


class TestDateValidation:
    """Test date format validation."""

    def test_valid_date_format(self):
        """Test valid date format YYYY-mm-dd."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        assert pattern.match("2025-05-24") is not None
        assert pattern.match("2000-01-01") is not None
        assert pattern.match("1970-12-31") is not None

    def test_invalid_date_no_separators(self):
        """Test date without separators is invalid."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        assert pattern.match("20250524") is None
        assert pattern.match("25-05-24") is None

    def test_invalid_date_wrong_separators(self):
        """Test date with wrong separators is invalid."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        assert pattern.match("2025/05/24") is None
        assert pattern.match("2025.05.24") is None
        assert pattern.match("24-05-2025") is None

    def test_invalid_date_missing_parts(self):
        """Test date with missing parts is invalid."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        assert pattern.match("2025-05") is None
        assert pattern.match("05-24") is None
        assert pattern.match("2025") is None

    def test_invalid_date_extra_parts(self):
        """Test date with extra parts is invalid."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        assert pattern.match("2025-05-24-01") is None

    def test_edge_case_dates(self):
        """Test edge case dates."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        # Jan 1
        assert pattern.match("2025-01-01") is not None
        # Dec 31
        assert pattern.match("2025-12-31") is not None

    def test_invalid_month(self):
        """Test invalid month values."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        # Month regex allows 00-19, invalid 20+
        assert pattern.match("2025-20-15") is None
        assert pattern.match("2025-99-15") is None

    def test_invalid_day(self):
        """Test invalid day values."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        # Day regex allows 00-39, invalid 40+
        assert pattern.match("2025-05-40") is None

    def test_leading_zeros_required(self):
        """Test leading zeros are required in month/day."""
        pattern = re.compile(DATE_VALIDATION_PATTERN)
        assert pattern.match("2025-5-24") is None
        assert pattern.match("2025-05-4") is None
        assert pattern.match("2025-5-4") is None
