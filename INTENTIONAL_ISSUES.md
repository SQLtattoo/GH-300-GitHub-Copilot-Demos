# Intentional Issues

The current tree is the completed reference state. The starter-state issues used by the GH-300 exercises have been resolved and are retained here as a completion record.

## Resolved Issues

| Area | Resolution |
| --- | --- |
| Calculator edge cases | Empty averages, zero expenses, and zero income return `0.0`; forecast day ranges are validated. |
| Transaction validation | Missing fields, blank values, negative or non-numeric amounts, and unknown transaction types are rejected. |
| File security | Every read and write is confined to the configured base path. |
| Malformed input | CSV and JSON transaction data receive contextual validation errors. |
| Processing performance | Expense category grouping and duplicate detection use linear-time passes. |
| Missing features | Forecasting, budget checks, sorting, spending alerts, merchant summaries, and CSV export are implemented. |
| Data table boundaries | Invalid pagination and sort definitions are rejected; zero and missing values sort safely. |

## Coverage Status

The test suite covers calculator edge cases, transaction processing, malformed and unsafe file input, report construction, table behavior, and logging. The enforced project coverage gate is 90%.