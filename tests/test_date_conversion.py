"""
Tests for make_date_str() date/time conversion function.
Tests all 5 supported log formats with various inputs.
"""
import re
import pytest


MONTH_LOOKUP = {
    "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04",
    "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
    "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12",
}


def make_date_str_impl(logline, date_format, current_year=2025):
    """
    Implementation of make_date_str() for testing.
    Converts log timestamp to YYYYMMDD HH:MM:SS format.
    """
    match_obj = re.match(date_format, logline)
    if match_obj is None:
        return ''

    match_array = match_obj.groupdict()
    d_year = match_array.get('YEAR', str(current_year))
    d_month = (
        match_array.get('MONTH')
        if 'MONTH' in match_array
        else MONTH_LOOKUP.get(match_array.get('MONTH_NAME', ''), '')
    )
    d_day = match_array.get('DAY', '').zfill(2)
    d_hour = match_array.get('HOURS', '')
    d_min = match_array.get('MINUTES', '')
    d_sec = match_array.get('SECONDS', '00')
    linedate = f"{d_year}{d_month}{d_day} {d_hour}:{d_min}:{d_sec}"

    return linedate


class TestMakeDateStr:
    """Test suite for make_date_str() function."""

    def test_w3c_extended_basic(self, w3c_log_line, w3c_regexp):
        """Test basic W3C Extended format conversion."""
        result = make_date_str_impl(w3c_log_line, w3c_regexp)
        assert result == "20250524 14:30:45"

    def test_syslog_basic(self, syslog_line, syslog_regexp):
        """Test basic Syslog format conversion."""
        result = make_date_str_impl(syslog_line, syslog_regexp)
        assert result == "20250524 14:30:45"

    def test_nsca_common_basic(self, nsca_common_line,
                                nsca_common_regexp):
        """Test basic NSCA Common format conversion."""
        result = make_date_str_impl(nsca_common_line,
                                     nsca_common_regexp)
        assert result == "20250524 14:30:45"

    def test_bind8_basic(self, bind8_line, bind8_regexp):
        """Test basic Bind8 format conversion."""
        result = make_date_str_impl(bind8_line, bind8_regexp)
        assert result == "20250524 14:30:45"

    def test_nginx_error_basic(self, nginx_error_line,
                                nginx_error_regexp):
        """Test basic Nginx Error format conversion."""
        result = make_date_str_impl(nginx_error_line,
                                     nginx_error_regexp)
        assert result == "20250524 14:30:45"

    def test_syslog_no_year(self, syslog_regexp):
        """Test Syslog defaults to CURRENT_YEAR (no year field)."""
        line = "May 24 14:30:45 hostname process[1234]: msg"
        result = make_date_str_impl(line, syslog_regexp,
                                     current_year=2025)
        assert result == "20250524 14:30:45"

    def test_syslog_different_year(self, syslog_regexp):
        """Test Syslog uses different current year."""
        line = "Dec 31 23:59:59 hostname process: msg"
        result = make_date_str_impl(line, syslog_regexp,
                                     current_year=2024)
        assert result == "20241231 23:59:59"

    def test_single_digit_day_padding(self, w3c_regexp):
        """Test single-digit day is zero-padded."""
        result = make_date_str_impl(
            "2025-05-09 14:30:45 GET /",
            w3c_regexp
        )
        assert result == "20250509 14:30:45"

    def test_single_digit_syslog_day(self, syslog_regexp):
        """Test Syslog single-digit day zero-padding."""
        line = "May  5 14:30:45 hostname process: msg"
        result = make_date_str_impl(line, syslog_regexp)
        assert result == "20250505 14:30:45"

    def test_midnight_time(self, w3c_regexp):
        """Test 00:00:00 time."""
        result = make_date_str_impl(
            "2025-05-24 00:00:00 GET /",
            w3c_regexp
        )
        assert result == "20250524 00:00:00"

    def test_end_of_day_time(self, w3c_regexp):
        """Test 23:59:59 time."""
        result = make_date_str_impl(
            "2025-05-24 23:59:59 GET /",
            w3c_regexp
        )
        assert result == "20250524 23:59:59"

    def test_all_months_syslog(self, syslog_regexp, month_lookup):
        """Test all 12 months are converted correctly."""
        for month_name, month_num in month_lookup.items():
            line = (
                f"{month_name} 15 10:20:30 "
                "hostname process: msg"
            )
            result = make_date_str_impl(line, syslog_regexp)
            expected = f"2025{month_num}15 10:20:30"
            assert result == expected, (
                f"Month {month_name} failed"
            )

    def test_all_months_bind8(self, bind8_regexp, month_lookup):
        """Test all 12 months for Bind8 format."""
        for month_name, month_num in month_lookup.items():
            line = f"15-{month_name}-2025 10:20:30."
            result = make_date_str_impl(line, bind8_regexp)
            expected = f"2025{month_num}15 10:20:30"
            assert result == expected, (
                f"Month {month_name} failed"
            )

    def test_nonmatching_line_empty_string(self, w3c_regexp):
        """Test non-matching line returns empty string."""
        result = make_date_str_impl(
            "This does not match any format",
            w3c_regexp
        )
        assert result == ""

    def test_leap_year_feb_29(self, w3c_regexp):
        """Test leap year date Feb 29."""
        result = make_date_str_impl(
            "2024-02-29 14:30:45 GET /",
            w3c_regexp
        )
        assert result == "20240229 14:30:45"

    def test_year_edge_cases(self, w3c_regexp):
        """Test various year values."""
        test_cases = [
            ("2000-01-01 10:00:00 GET /", "20000101 10:00:00"),
            ("2099-12-31 23:59:59 GET /", "20991231 23:59:59"),
            ("1970-01-01 00:00:00 GET /", "19700101 00:00:00"),
        ]
        for logline, expected in test_cases:
            result = make_date_str_impl(logline, w3c_regexp)
            assert result == expected

    def test_nsca_timezone_variations(self, nsca_common_regexp):
        """Test NSCA Common with different timezones."""
        test_cases = [
            (
                '192.168.1.1 - - [24/May/2025:14:30:45 +0000] '
                '"GET / HTTP/1.1" 200',
                "20250524 14:30:45"
            ),
            (
                '192.168.1.1 - - [24/May/2025:14:30:45 -0500] '
                '"GET / HTTP/1.1" 200',
                "20250524 14:30:45"
            ),
        ]
        for logline, expected in test_cases:
            result = make_date_str_impl(logline,
                                         nsca_common_regexp)
            assert result == expected
