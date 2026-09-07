# Budget Buddy - GitHub Copilot Demo Lab

Budget Buddy is a small Python budget tracker designed for Microsoft GH-300 demonstrations. The current tree is the completed reference state, with defensive validation, the workshop features implemented, and a 90% coverage gate.

The goal is to show Copilot as more than autocomplete: codebase explanation, inline edits, agent mode, test generation, debugging, security review, refactoring, documentation, and PR-style summaries.

## Current Demo State

- Runnable app: `python main.py`
- Comprehensive pytest suite
- Current coverage gate: 90%
- Resolved starter issues: documented in [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md)
- Trainer flow: documented in [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

## Quick Start

```powershell
.\setup_demo.ps1
.\.venv\Scripts\Activate.ps1
python main.py
pytest
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## What The App Does

Budget Buddy reads sample transactions from [data/sample_transactions.csv](data/sample_transactions.csv), exports them to `data/exported_transactions.csv`, builds a simple monthly budget report, and logs:

- income
- expenses
- remaining budget
- net cash flow
- savings rate
- largest expense
- spending by category
- top three merchants by total spending
- a paginated transaction table
- the CSV export destination

## Main Files

| File | Purpose |
| --- | --- |
| [main.py](main.py) | Runnable demo app and report orchestration |
| [calculator.py](calculator.py) | Budget calculations with guarded edge cases |
| [data_processor.py](data_processor.py) | Validated transaction filtering, grouping, sorting, and summaries |
| [file_handler.py](file_handler.py) | Confined and validated CSV/JSON file I/O |
| [data_table.py](data_table.py) | Generic table helper used by the app |
| [logger.py](logger.py) | Centralized logging utility |
| [tests](tests) | Focused tests enforcing the 90% coverage gate |

## Demo Flow (GH-300 modules)

The trainer flow in [DEMO_SCRIPT.md](DEMO_SCRIPT.md) is aligned to the five
course modules:

1. **Module 1 — Introduction:** run `setup_demo.ps1` and `python main.py` to frame the use case.
2. **Module 2 — Exploring Features:** Chat, Inline Chat, CLI, and prompts with context (security review of file handling).
3. **Module 3 — Developer Use Cases:** generate, transform, optimize, document, and a DevOps beat (Dockerfile + CI).
4. **Module 4 — Building Unit Tests:** the coverage journey from ~30% to 90%+.
5. **Module 5 — Advanced Capabilities:** Agent Mode, `AGENT.md`, Skills, MCP, and PR review/summary.

## Useful Copilot Prompts

Reusable prompts live in [.github/prompts](.github/prompts):

- `generate-tests.prompt.md`
- `security-review.prompt.md`
- `refactor-performance.prompt.md`
- `agent-feature.prompt.md`
- `devops-snippet.prompt.md`
- `pr-summary.prompt.md`

## Agent Customization Assets

Module 5 showcases how Copilot follows project-level guidance:

- [AGENT.md](AGENT.md) — operating manual for agents in this repo.
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — repo-wide rules.
- [.github/skills](.github/skills) — task playbooks (`SKILL.md`), e.g. adding a budget report section.

## Validation Commands

```powershell
python main.py
pytest
pytest --cov=. --cov-report=term-missing
```

The current reference state already enforces 90%. Use [reset_for_demo.ps1](reset_for_demo.ps1) before presenting the starter-to-completed coverage journey.

## Trainer Notes

Use [reset_for_demo.ps1](reset_for_demo.ps1) to restore the intentionally incomplete workshop state. The current completed state remains a training application rather than a production financial system.