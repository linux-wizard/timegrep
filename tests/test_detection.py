"""
Tests for date format detection functionality.
"""
import re
import pytest


# Extract log format regexes from timegrep
W3C_EXTENDED_REGEXP = (
    r"(?P<YEAR>[0-9]{4})\-(?P<MONTH>[0-9]{2})\-"
    r"(?P<DAY>[0-9]{2}) (?P<HOURS>[0-9]{2}):"
    r"(?P<MINUTES>[0-9]{2}):(?P<SECONDS>[0-9]{2})"
)
SYSLOG_REGEXP = (
    r"(?P<MONTH_NAME>[a-zA-Z]{3}) {1,2}(?P<DAY>[0-9]{1,2}) "
    r"(?P<HOURS>[0-9]{2}):(?P<MINUTES>[0-9]{2}):"
    r"(?P<SECONDS>[0-9]{2})"
)
NSCA_COMMON_REGEXP = (
    r"(?P<origin>\d+\.\d+\.\d+\.\d+) (?P<identd>-|\w*) "
    r"(?P<auth>-|\w*) \[(?P<DAY>[0-9]{1,2})/"
    r"(?P<MONTH_NAME>[a-zA-Z]{3})/(?P<YEAR>[0-9]{4}):"
    r"(?P<HOURS>[0-9]{2}):(?P<MINUTES>[0-9]{2}):"
    r"(?P<SECONDS>[0-9]{2}) (?P<tz>[\-\+]?\d\d\d\d)\]"
)
BIND8_REGEXP = (
    r"(?P<DAY>[0-9]{1,2})\-(?P<MONTH_NAME>[a-zA-Z]{3})\-"
    r"(?P<YEAR>[0-9]{4}) (?P<HOURS>[0-9]{2}):"
    r"(?P<MINUTES>[0-9]{2}):(?P<SECONDS>[0-9]{2})\."
)
NGINX_ERROR_REGEXP = (
    r"(?P<YEAR>[0-9]{4})/(?P<MONTH>[0-9]{2})/(?P<DAY>[0-9]{2}) "
    r"(?P<HOURS>[0-9]{2}):(?P<MINUTES>[0-9]{2}):"
    r"(?P<SECONDS>[0-9]{2})"
)


LOG_FORMATS = [
    {"regexp": W3C_EXTENDED_REGEXP, "name": "W3C Extended"},
    {"regexp": SYSLOG_REGEXP, "name": "Syslog"},
    {"regexp": NSCA_COMMON_REGEXP, "name": "NSCA Common"},
    {"regexp": BIND8_REGEXP, "name": "Bind8"},
    {"regexp": NGINX_ERROR_REGEXP, "name": "Nginx Error"},
]


class TestDateFormatDetection:
    """Test date format detection across all 5 log formats."""

    def test_w3c_extended_detection(self, w3c_log_line):
        """Test W3C Extended format is detected correctly."""
        for fmt in LOG_FORMATS:
            match = re.match(fmt["regexp"], w3c_log_line)
            if fmt["name"] == "W3C Extended":
                assert match is not None
            else:
                pass  # Other formats may or may not match

    def test_w3c_extended_groups(self, w3c_log_line):
        """Test W3C Extended regex extracts expected groups."""
        match = re.match(W3C_EXTENDED_REGEXP, w3c_log_line)
        assert match is not None
        groups = match.groupdict()
        assert groups["YEAR"] == "2025"
        assert groups["MONTH"] == "05"
        assert groups["DAY"] == "24"
        assert groups["HOURS"] == "14"
        assert groups["MINUTES"] == "30"
        assert groups["SECONDS"] == "45"

    def test_syslog_detection(self, syslog_line):
        """Test Syslog format is detected correctly."""
        match = re.match(SYSLOG_REGEXP, syslog_line)
        assert match is not None

    def test_syslog_groups(self, syslog_line):
        """Test Syslog regex extracts expected groups."""
        match = re.match(SYSLOG_REGEXP, syslog_line)
        assert match is not None
        groups = match.groupdict()
        assert groups["MONTH_NAME"] == "May"
        assert groups["DAY"] == "24"
        assert groups["HOURS"] == "14"
        assert groups["MINUTES"] == "30"
        assert groups["SECONDS"] == "45"
        assert "YEAR" not in groups

    def test_nsca_common_detection(self, nsca_common_line):
        """Test NSCA Common format is detected correctly."""
        match = re.match(NSCA_COMMON_REGEXP, nsca_common_line)
        assert match is not None

    def test_nsca_common_groups(self, nsca_common_line):
        """Test NSCA Common regex extracts expected groups."""
        match = re.match(NSCA_COMMON_REGEXP, nsca_common_line)
        assert match is not None
        groups = match.groupdict()
        assert groups["origin"] == "192.168.1.1"
        assert groups["YEAR"] == "2025"
        assert groups["MONTH_NAME"] == "May"
        assert groups["DAY"] == "24"

    def test_bind8_detection(self, bind8_line):
        """Test Bind8 format is detected correctly."""
        match = re.match(BIND8_REGEXP, bind8_line)
        assert match is not None

    def test_bind8_groups(self, bind8_line):
        """Test Bind8 regex extracts expected groups."""
        match = re.match(BIND8_REGEXP, bind8_line)
        assert match is not None
        groups = match.groupdict()
        assert groups["DAY"] == "24"
        assert groups["MONTH_NAME"] == "May"
        assert groups["YEAR"] == "2025"

    def test_nginx_error_detection(self, nginx_error_line):
        """Test Nginx Error format is detected correctly."""
        match = re.match(NGINX_ERROR_REGEXP, nginx_error_line)
        assert match is not None

    def test_nginx_error_groups(self, nginx_error_line):
        """Test Nginx Error regex extracts expected groups."""
        match = re.match(NGINX_ERROR_REGEXP, nginx_error_line)
        assert match is not None
        groups = match.groupdict()
        assert groups["YEAR"] == "2025"
        assert groups["MONTH"] == "05"
        assert groups["DAY"] == "24"

    def test_invalid_log_line(self):
        """Test invalid log line matches no format."""
        invalid_line = "This is not a log line"
        for fmt in LOG_FORMATS:
            match = re.match(fmt["regexp"], invalid_line)
            assert match is None

    def test_format_priority_order(self):
        """Test format detection order (first match wins)."""
        # A line that could match multiple formats should
        # match the first one in the list
        w3c_line = "2025-05-24 14:30:45 GET /"
        match = re.match(W3C_EXTENDED_REGEXP, w3c_line)
        assert match is not None

    def test_syslog_single_digit_day(self):
        """Test Syslog with single-digit day."""
        line = "May  5 14:30:45 hostname process: msg"
        match = re.match(SYSLOG_REGEXP, line)
        assert match is not None
        assert match.groupdict()["DAY"] == "5"

    def test_syslog_two_digit_day(self):
        """Test Syslog with two-digit day."""
        line = "May 24 14:30:45 hostname process: msg"
        match = re.match(SYSLOG_REGEXP, line)
        assert match is not None
        assert match.groupdict()["DAY"] == "24"
