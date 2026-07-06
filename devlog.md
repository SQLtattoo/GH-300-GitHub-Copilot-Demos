# Development Log

This log captures notable work performed during the Budget Buddy walkthrough branch.

## 2026-07-06

### Branch

- `demo/budget-buddy-walkthrough`

### Security Review

- Reviewed [file_handler.py](file_handler.py) for path traversal and unsafe file access risks.
- Added safe path resolution for file reads and writes through `BudgetFileHandler._resolve_safe_path()`.
- Added a pytest security regression test for JSON path traversal attempts.
- Updated [CHANGELOG.md](CHANGELOG.md) and [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) after resolving the JSON path validation starter issue.

### Architecture Documentation

- Added [architecture.md](architecture.md) to explain the Budget Buddy application architecture, runtime flow, main components, data model, report shape, tests, and known demo gaps.
- Added [architecture.mmd](architecture.mmd) as a standalone Mermaid architecture diagram source.
- Linked the standalone Mermaid diagram from [architecture.md](architecture.md).

### Validation

- Ran the full pytest suite after the security fix.
- Result: `9 passed`, coverage `34.95%`, coverage gate satisfied.

### Open Demo Work

- Improve malformed CSV row errors.
- Add tests for calculator edge cases.
- Refactor inefficient transaction grouping and duplicate detection.
- Continue raising coverage toward the workshop target.