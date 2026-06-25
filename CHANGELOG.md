# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Added a "top merchants" section to the budget report: `TransactionProcessor.top_merchants` ranks expense merchants by total spending, wired into `build_report` and the `main` report output. Added happy-path and edge-case tests.
- Added `BudgetFileHandler.write_transactions_csv` to export transactions to a CSV file, preserving the same headers used by `read_transactions_csv`. Added roundtrip, header, and empty-list tests.
- Revamped the repository into **Budget Buddy**, a working Personal Budget & Expense Tracker demo app for GH-300 delivery.
- Expanded the pytest suite to ~99% coverage with focused tests for `DataTable`, the logger, the `main` entry point, and edge cases across the calculator, transaction processor, and file handler.
- Added sample transaction data in [data/sample_transactions.csv](data/sample_transactions.csv).
- Added a sparse starter pytest suite designed to begin around 30% coverage.
- Added [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for trainer delivery flow.
- Added [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) documenting deliberate bugs, TODOs, security gaps, and performance issues.
- Added reusable Copilot prompt files under [.github/prompts](.github/prompts).

### Changed
- Replaced arithmetic-only calculator examples with budget calculation helpers.
- Replaced generic data processing examples with transaction processing helpers.
- Replaced generic file examples with CSV/JSON budget data loading helpers.
- Updated pytest configuration to use a demo-start `30%` coverage threshold.
- Refreshed README, quick reference, setup script, reset script, and Copilot instructions for the app-centered demo flow.
- Refactored `TransactionProcessor.find_duplicate_transactions` from O(n^2) pairwise comparison to a one-pass O(n) signature-count approach, preserving output. Added behavior-locking tests.

### Intentional Demo Gaps
- Coverage is intentionally low at the start of the demo.
- Several TODOs and bugs are intentionally present for Copilot-assisted implementation.
- File handling intentionally includes a path traversal risk for security review demos.
- Transaction processing intentionally includes O(n^2) logic for refactoring demos.