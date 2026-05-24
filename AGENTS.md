# AGENTS.md

## Overview
**timegrep** is a single-file Python utility that performs binary searches through log files to extract a time range. Installed as a console script; no complex build, test, or multi-file architecture.

## Critical Facts

### Language & Environment
- **Python 3.14+** (pinned in `.python-version`)
- Single executable script: `timegrep` (no package, no external dependencies)
- Distribution via PyPI using setuptools
- **Unit tests**: 51 tests in `tests/` directory (pytest-based)

### Code Structure
- Entry point: `timegrep` (#!/usr/bin/env python3 shebang)
- No separate modules, imports, or external dependencies
- ~413 lines; supports 5 log formats (W3C Extended, Syslog, NSCA Common, Bind8, Nginx Error)
- Key functions: `detect_date_format()`, `make_date_str()`, `getdata()`, `main()`

### Linting & Validation
- **Pylint** via pre-commit (`.pre-commit-config.yaml`):
  - Max line length: 80 chars
  - Disabled rules: F0401, W0141, W0611, W0110, W0703, W0142, C0103, E0401, R0912, R0915, R0801, W0201
  - Enforces PascalCase module naming
- **Commit validation**: Commitlint enforces conventional commits (type, scope, body formatting)
- Run locally: `pre-commit run --all-files` or `pylint --max-line-length=80 timegrep`

### CI/CD
- GitHub Actions only on PRs to `master` (`.github/workflows/build.yml`)
- Only runs Pylint reporter (no tests, no coverage)
- Release automation via semantic-release (see `release.config.js`)

### Testing
- **Framework**: pytest (51 tests, all passing)
- **Test structure**: `tests/` directory with 3 test modules:
  - `test_detection.py` — regex format detection (14 tests)
  - `test_date_conversion.py` — date/time parsing (17 tests)
  - `test_validation.py` — argument validation (20 tests)
- **Test data**: Uses fixtures from `tests/conftest.py`
- **Run tests locally**: 
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install pytest
  pytest tests/ -v
  ```
- **Pylint on tests**: Must comply with 80-char limit
  ```bash
  pylint --max-line-length=80 tests/
  ```

### Common Pitfalls
- **Timestamp format detection**: regex list is hardcoded in `timegrep`; custom formats require `--log-regexp` flag and an external file
- **Line length constraint**: 80-char max strictly enforced; pylint will catch violations pre-commit
- **File I/O assumptions**: assumes log files are properly sorted by timestamp; binary search will fail on unsorted logs
- **Test isolation**: tests use mock implementations of core functions rather than importing timegrep (script has module-level code that runs at import)

### Bug Fixes (Recent)
**Critical file handle and integer division bugs fixed:**
- **File handle lifecycle** (lines 330-340): Changed from context manager (`with` block) to explicit `open()` call. File now stays open for entire binary search algorithm, then explicitly closed at end. Fixes crash: "ValueError: I/O operation on closed file"
- **Integer division** (line 365): Changed `/` to `//` for integer division. Python 3 float division was causing precision loss in binary search seek positions
- **Variable consistency** (lines 383-388): Changed `date_format` to `detected_date_format` for consistent format detection. Ensures all `getdata()` calls use the same detected format
- **All 51 unit tests pass**: Fixes verified to maintain backward compatibility and correct behavior

### How to Run
```bash
# Install from PyPI
pip install timegrep

# Local usage (after checkout)
./timegrep --help
./timegrep --start-time 14:30 --end-time 15:45 /path/to/logfile

# Run pylint locally
pylint --max-line-length=80 timegrep
```

### Release Process
- Commits follow conventional commit format (enforced by commitlint pre-commit hook)
- semantic-release handles versioning and PyPI uploads on merge to master
- Version is read from `setup.cfg` and updated by semantic-release
