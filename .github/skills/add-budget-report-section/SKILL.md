---
name: add-budget-report-section
description: Add a new section to the Budget Buddy monthly report. Use when asked to add, extend, or include a new metric, breakdown, or summary (for example "top merchants", "weekly spend", or "category trend") in the report produced by main.py.
---

# Skill: Add a Budget Report Section

Follow these steps to add a new section to the Budget Buddy report consistently.

## 1. Understand the report flow

- The report is assembled in `main.py` (`build_report()` and
  `show_transactions()`).
- Numeric logic belongs in `calculator.py` (`BudgetCalculator`).
- Transaction shaping (grouping, sorting, summaries) belongs in
  `data_processor.py` (`TransactionProcessor`).

## 2. Implement the logic in the right module

- Add a focused method to `BudgetCalculator` or `TransactionProcessor`.
- Keep it small, add type hints, and guard edge cases (empty input, zero income,
  zero expenses).

## 3. Wire it into the report

- Call the new method from `build_report()` in `main.py`.
- Emit output through `logger` from `logger.py`. Do not use `print`.
- If the section is tabular, reuse `DataTable` and `ColumnDefinition` from
  `data_table.py`.

## 4. Add tests

- Add pytest tests under `tests/` covering the happy path and at least one
  edge case.
- Run `pytest` and confirm the coverage gate in `pytest.ini` still
  passes.

## 5. Update docs

- Note the new section in `README.md` under "What The App Does".
- Add an entry to `CHANGELOG.md`.

## 6. Report back

Summarize the files changed, tests added, test results, and any remaining risks.
