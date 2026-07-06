# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Fixed
- Hardened [file_handler.py](file_handler.py) with safe path resolution to block absolute paths and directory traversal outside the configured base directory for CSV/JSON reads and JSON writes.
- Added a security regression test in [tests/test_file_handler.py](tests/test_file_handler.py) to verify traversal attempts are rejected.
- Fixed cross-platform absolute path detection in [file_handler.py](file_handler.py) so Windows-style absolute paths are rejected even when tests run on Linux/macOS.
- Fixed [data_processor.py](data_processor.py) `top_merchants()` to ignore blank merchant names and treat `amount=None` as zero instead of raising `TypeError`.

### Added
- Added a **top merchants** section to the monthly report: `TransactionProcessor.top_merchants()` in [data_processor.py](data_processor.py) ranks expense merchants by total spend, wired into `build_report()` and the console output in [main.py](main.py), with tests in [tests/test_data_processor.py](tests/test_data_processor.py) and [tests/test_main.py](tests/test_main.py).
- Re-established the pytest setup with a **per-module** coverage gate: [pytest.ini](pytest.ini) plus a [tests/conftest.py](tests/conftest.py) hook that fails the session unless every source module reaches at least 80% line coverage (enforced per module, not on the average).
- Added per-module test files under [tests/](tests) covering the calculator, transaction processor, file handler, logger, data table, and main app (64 tests; all source modules at 98-100%).
- Revamped the repository into **Budget Buddy**, a working Personal Budget & Expense Tracker demo app for GH-300 delivery.
- Added sample transaction data in [data/sample_transactions.csv](data/sample_transactions.csv).
- Added a sparse starter pytest suite designed to begin around 30% coverage.
- Added [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for trainer delivery flow.
- Added [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) documenting deliberate bugs, TODOs, security gaps, and performance issues.
- Added reusable Copilot prompt files under [.github/prompts](.github/prompts).

### Changed
- Replaced arithmetic-only calculator examples with budget calculation helpers.
- Replaced generic data processing examples with transaction processing helpers.
- Replaced generic file examples with CSV/JSON budget data loading helpers.
- Updated pytest configuration to enforce an 80% per-module coverage gate.
- Refreshed README, quick reference, setup script, reset script, and Copilot instructions for the app-centered demo flow.

### Intentional Demo Gaps
- Coverage is intentionally low at the start of the demo.
- Several TODOs and bugs are intentionally present for Copilot-assisted implementation.
- File handling intentionally includes a path traversal risk for security review demos.
- Transaction processing intentionally includes O(n^2) logic for refactoring demos.