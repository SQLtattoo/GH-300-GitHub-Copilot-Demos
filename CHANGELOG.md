# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Revamped the repository into **Budget Buddy**, a working Personal Budget & Expense Tracker demo app for GH-300 delivery.
- Added sample transaction data in [data/sample_transactions.csv](data/sample_transactions.csv).
- Added a sparse starter pytest suite designed to begin around 30% coverage.
- Added [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for trainer delivery flow.
- Added [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) documenting deliberate bugs, TODOs, security gaps, and performance issues.
- Added reusable Copilot prompt files under [.github/prompts](.github/prompts).
- Added a broader pytest suite under [tests](tests) covering calculator, processor, file handling, table utilities, logger setup, and report construction.

### Changed
- Replaced arithmetic-only calculator examples with budget calculation helpers.
- Replaced generic data processing examples with transaction processing helpers.
- Replaced generic file examples with CSV/JSON budget data loading helpers.
- Updated pytest configuration to use a demo-start `30%` coverage threshold.
- Expanded calculator tests with additional edge-case and history-behavior coverage.
- Expanded `largest_expense` tests in [tests/test_data_processor.py](tests/test_data_processor.py) to cover mixed transaction types and numeric string amounts.
- Refreshed README, quick reference, setup script, reset script, and Copilot instructions for the app-centered demo flow.
- Hardened file path handling in [file_handler.py](file_handler.py) to block path traversal and absolute-path file access.
- Refactored duplicate detection in [data_processor.py](data_processor.py) from nested-loop matching to key-based aggregation while preserving output behavior.
- Expanded transaction processor tests to lock duplicate-detection behavior.
- Raised local source-module coverage to above 80% (94% in the latest run).

### Intentional Demo Gaps
- Coverage is intentionally low at the start of the demo.
- Several TODOs and bugs are intentionally present for Copilot-assisted implementation.
- Transaction processing intentionally includes O(n^2) logic for refactoring demos.