---
name: run-coverage
description: Run the Budget Buddy test suite with a coverage report. Use when asked to run tests, check coverage, see the coverage report, or verify the coverage gate before or after making changes.
---

# Skill: Run Test Coverage

This skill runs the Budget Buddy pytest suite and prints a coverage report so you
can see which lines are not yet tested.

## How to run it

Run the script for the current platform from this skill's directory:

- On Linux or macOS (including the GitHub Copilot cloud agent), run
  `run-coverage.sh`.
- On Windows (local VS Code agent mode), run `run-coverage.ps1`.

Each script:

1. Selects the project virtual environment (`.venv`) if present, otherwise falls
   back to the system `python`.
2. Runs `pytest` with `--cov=. --cov-report=term-missing`.

> Note: this skill does not pre-approve the `shell` tool, so Copilot will ask for
> confirmation before running the script. To skip that prompt in a trusted demo,
> add `allowed-tools: shell` to the frontmatter above. Only do this if you trust
> the skill and its scripts.

## Interpreting the result

- The `Missing` column lists line numbers with no test coverage. These are good
  candidates for new tests.
- The run fails if total coverage is below the gate in `pytest.ini`. During the
  demo this gate is raised from 30 to 90.

## After running

Summarize the current coverage percentage and call out the modules with the most
uncovered lines.
