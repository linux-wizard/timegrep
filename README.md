# timegrep.py

by Dennis Williamson 20100113
in response to http://serverfault.com/questions/101744/fast-extraction-of-a-time-range-from-syslog-logfile

Improvements by Fabrice FACORAT 20110914

---

## Overview

Perform a binary search through a log file to find a range of times
and print the corresponding lines

**Supported Log Formats:**
- W3C Extended: `%Y-%m-%d %H:%M:%S`
- Syslog: `%b %d %H:%M:%S`
- NSCA Common/Apache: `host rfc931 username [%d/%b/%Y:%H:%M:%S +TZ]`
- Bind8: `%d-%b-%Y %H:%M:%S.`
- Nginx Error logs: `%Y/%m/%d %H:%M:%S`

**Requires Python 3.8+**

---

## Installation

```bash
pip install timegrep
```

---

## Usage

### Basic Usage

Extract log entries for a specific time range on today's date:

```bash
timegrep --start-time 14:30 --end-time 15:45 /var/log/apache2/access.log
```

### Common Examples

**Extract logs from a specific date:**
```bash
timegrep --date 2025-05-24 --start-time 14:30 --end-time 15:45 /var/log/syslog
```

**Extract all logs from 2:00 PM onwards (to end of day):**
```bash
timegrep --start-time 14:00 /var/log/nginx/error.log
```

**Extract all logs up to 3:30 PM (from start of day):**
```bash
timegrep --end-time 15:30 /var/log/auth.log
```

**Extract logs with seconds precision:**
```bash
timegrep --start-time 14:30:45 --end-time 15:30:15 /var/log/app.log
```

### Command-Line Options

**Time and Date Arguments:**
- `--start-time HH:MM[:SS]` — Start time for log extraction
- `--end-time HH:MM[:SS]` — End time for log extraction
- At least one of `--start-time` or `--end-time` is required
- `-d, --date YYYY-MM-DD` — Extract from a specific date (default: today)

**Output Options:**
- `-l, --long` — Include longest possible time range
- `-s, --short` — Include shortest possible time range

**Advanced Options:**
- `-L, --log-regexp FILE` — Use custom log format definitions from file
- `-D, --debug LEVEL` — Enable debug output (0=none, 1=some, 2=more)

---

## Future Enhancements

- Make sure it works if seek falls in middle of first or last line
- Improve handling of lines at exact search boundaries
- Support unsorted log files (currently requires sorted timestamps)

---

## Development & Contributing

### Prerequisites

To contribute to timegrep, you'll need:
- **Python 3.8 or higher** (verify with `python3 --version`)
- **Git** (for cloning the repo and pre-commit hooks)
- **pip** (Python package installer, included with Python 3.8+)

### Setting Up Your Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/linux-wizard/timegrep.git
   cd timegrep
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install pytest pylint pre-commit
   ```

4. **Install pre-commit hooks** (recommended):
   ```bash
   pre-commit install
   ```
   This ensures linting and commit message validation run automatically
   before each commit.

### Running Tests

timegrep includes a comprehensive test suite with **51 tests** covering:
- Format detection (regex matching for 5 log formats)
- Date/time parsing and conversion
- Argument validation (time and date formats)

**Run all tests**:
```bash
pytest tests/ -v
```

**Run specific test module**:
```bash
pytest tests/test_detection.py -v     # Format detection tests
pytest tests/test_date_conversion.py -v  # Date parsing tests
pytest tests/test_validation.py -v       # Validation tests
```

**Run tests with coverage summary**:
```bash
pytest tests/ --tb=short
```

All tests should pass before submitting a pull request.

### Code Quality & Linting

timegrep enforces strict code quality standards via **Pylint** with a
**maximum line length of 80 characters**.

**Run pylint on your changes**:
```bash
pylint --max-line-length=80 timegrep
```

**Run pylint on test files**:
```bash
pylint --max-line-length=80 tests/
```

**Expected score**: Aim for **10.00/10** (or as close as possible).

Configuration details are in `.pre-commit-config.yaml`. Key rules:
- Max line length: 80 characters (strictly enforced)
- Module naming style: PascalCase
- Disabled rules: F0401, W0141, W0611, W0110, W0703, W0142, C0103,
  E0401, R0912, R0915, R0801, W0201

### Git Hooks & Commit Conventions

This project uses **pre-commit hooks** to validate code automatically:

1. **Pylint**: Checks code style and 80-character line limit
2. **Commitlint**: Enforces conventional commit messages
3. **File checks**: End-of-file fixes, JSON/YAML validation, etc.

**Conventional commit format**:
```
type(scope): subject

Body (optional)

Footer (optional)
```

**Valid types**: `build`, `chore`, `ci`, `docs`, `feat`, `fix`, `perf`,
`refactor`, `revert`, `style`, `test`

**Example**:
```
feat(detection): add support for custom log formats

Allows users to provide custom regex patterns via --log-regexp flag.

LXWD-5
```

### Development Workflow

Follow this workflow when contributing:

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** to `timegrep` (or add tests to `tests/`)

3. **Run tests** to ensure nothing broke:
   ```bash
   pytest tests/ -v
   ```

4. **Lint your code** to meet quality standards:
   ```bash
   pylint --max-line-length=80 timegrep
   pylint --max-line-length=80 tests/
   ```

5. **Stage and commit** (pre-commit hooks will run):
   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

6. **Fix any hook failures** if linting or commit message validation
   fails, then commit again.

7. **Push and open a PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Important Notes for Contributors

- **No external dependencies**: timegrep is designed as a single-file
  script with no pip dependencies. Keep it that way.

- **Log file assumptions**: timegrep assumes log files are sorted by
  timestamp. The binary search algorithm will fail on unsorted logs.

- **Testing strategy**: Tests use pure function implementations (not
  timegrep script imports) to avoid module-level execution issues.
  See `tests/conftest.py` for test fixtures.

- **Line length**: The 80-character limit is strictly enforced by both
  pre-commit hooks and CI. This includes docstrings and comments.

- **Format detection**: The 5 supported log format regexes are hardcoded
  in `timegrep`. For custom formats, users provide regexes via the
  `--log-regexp` flag.

### Getting Help

- **Technical details**: See `AGENTS.md` for architecture and design
  notes aimed at developers.
- **Issue tracker**: Check GitHub Issues for known problems or open a
  new issue.
- **Discussions**: Use GitHub Discussions for questions or ideas.

---
