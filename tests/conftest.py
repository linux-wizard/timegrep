"""
Shared pytest fixtures and configuration for timegrep tests.
"""
import io
import sys
from unittest.mock import patch

import pytest


# Sample log lines for each format
W3C_EXTENDED_LOG = (
    "2025-05-24 14:30:45 GET /index.html 200"
)
SYSLOG_LOG = "May 24 14:30:45 hostname process[1234]: message"
NSCA_COMMON_LOG = (
    '192.168.1.1 - user [24/May/2025:14:30:45 +0000] '
    '"GET /index.html HTTP/1.1" 200'
)
BIND8_LOG = "24-May-2025 14:30:45.123 query response:"
NGINX_ERROR_LOG = "2025/05/24 14:30:45 [error] 1234#0: *1 error"


@pytest.fixture
def mock_debug_level():
    """Mock the global DEBUG_LEVEL to prevent debug output."""
    with patch('__main__.DEBUG_LEVEL', 0):
        yield


@pytest.fixture
def mock_current_year():
    """Mock CURRENT_YEAR to 2025 for consistent testing."""
    with patch('__main__.CURRENT_YEAR', 2025):
        yield


@pytest.fixture
def w3c_log_line():
    """Sample W3C Extended log line."""
    return W3C_EXTENDED_LOG


@pytest.fixture
def syslog_line():
    """Sample Syslog line."""
    return SYSLOG_LOG


@pytest.fixture
def nsca_common_line():
    """Sample NSCA Common/Apache log line."""
    return NSCA_COMMON_LOG


@pytest.fixture
def bind8_line():
    """Sample Bind8 log line."""
    return BIND8_LOG


@pytest.fixture
def nginx_error_line():
    """Sample Nginx Error log line."""
    return NGINX_ERROR_LOG


@pytest.fixture
def w3c_regexp():
    """W3C Extended log format regexp."""
    return (
        r"(?P<YEAR>[0-9]{4})\-(?P<MONTH>[0-9]{2})\-"
        r"(?P<DAY>[0-9]{2}) (?P<HOURS>[0-9]{2}):"
        r"(?P<MINUTES>[0-9]{2}):(?P<SECONDS>[0-9]{2})"
    )


@pytest.fixture
def syslog_regexp():
    """Syslog log format regexp."""
    return (
        r"(?P<MONTH_NAME>[a-zA-Z]{3}) {1,2}"
        r"(?P<DAY>[0-9]{1,2}) (?P<HOURS>[0-9]{2}):"
        r"(?P<MINUTES>[0-9]{2}):(?P<SECONDS>[0-9]{2})"
    )


@pytest.fixture
def nsca_common_regexp():
    """NSCA Common log format regexp."""
    return (
        r"(?P<origin>\d+\.\d+\.\d+\.\d+) (?P<identd>-|\w*) "
        r"(?P<auth>-|\w*) \[(?P<DAY>[0-9]{1,2})/"
        r"(?P<MONTH_NAME>[a-zA-Z]{3})/(?P<YEAR>[0-9]{4}):"
        r"(?P<HOURS>[0-9]{2}):(?P<MINUTES>[0-9]{2}):"
        r"(?P<SECONDS>[0-9]{2}) (?P<tz>[\-\+]?\d\d\d\d)\]"
    )


@pytest.fixture
def bind8_regexp():
    """Bind8 log format regexp."""
    return (
        r"(?P<DAY>[0-9]{1,2})\-(?P<MONTH_NAME>[a-zA-Z]{3})\-"
        r"(?P<YEAR>[0-9]{4}) (?P<HOURS>[0-9]{2}):"
        r"(?P<MINUTES>[0-9]{2}):(?P<SECONDS>[0-9]{2})\."
    )


@pytest.fixture
def nginx_error_regexp():
    """Nginx Error log format regexp."""
    return (
        r"(?P<YEAR>[0-9]{4})/(?P<MONTH>[0-9]{2})/(?P<DAY>[0-9]{2}) "
        r"(?P<HOURS>[0-9]{2}):(?P<MINUTES>[0-9]{2}):"
        r"(?P<SECONDS>[0-9]{2})"
    )


@pytest.fixture
def month_lookup():
    """Month name to number lookup."""
    return {
        "Jan": "01", "Feb": "02", "Mar": "03",
        "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09",
        "Oct": "10", "Nov": "11", "Dec": "12",
    }
