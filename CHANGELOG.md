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
- Added focused tests for calculator edge cases, transaction validation and features, secure file I/O, data-table behavior, report orchestration, and logging.
- Implemented transaction sorting, spending alerts, merchant summaries, forecasting, budget checks, and CSV export from the runnable app.
- Added a top-merchants section to the monthly budget report.

### Changed
- Simplified console logging to show report messages without timestamp, logger name, or level prefixes.
- Replaced arithmetic-only calculator examples with budget calculation helpers.
- Replaced generic data processing examples with transaction processing helpers.
- Optimized duplicate transaction detection from O(n^2) pairwise comparisons to O(n) average-time key counting.
- Replaced generic file examples with CSV/JSON budget data loading helpers.
- Completed the Python 3.13 Docker image and GitHub Actions pytest workflow.
- Updated pytest configuration to use a demo-start `30%` coverage threshold.
- Refreshed README, quick reference, setup script, reset script, and Copilot instructions for the app-centered demo flow.
- Guarded zero-value calculator operations and invalid forecast day ranges.
- Replaced expense category grouping with a single-pass aggregation.
- Added strict transaction validation and contextual malformed CSV/JSON errors.
- Confined all file reads and writes to the configured base path.
- Hardened data-table sorting, pagination validation, and state handling.
- Raised and satisfied the project coverage gate at 90%.

### Completed Reference State
- Resolved the intentional starter bugs, TODOs, security gap, and performance issue.
- Retained `reset_for_demo.ps1` and the trainer guidance for restoring the workshop starter state.