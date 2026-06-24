# GitHub Copilot Project Instructions

This repository is a GH-300 demo lab for a small Python budget tracker named Budget Buddy.

## Demo Intent
- The starter state is intentionally incomplete.
- Keep the app runnable on the happy path.
- Keep starter coverage around 30% until the trainer begins the coverage demo.
- The workshop goal is to use Copilot to reach 90%+ coverage.
- Bugs, TODOs, security gaps, and performance issues are teaching material.

## Coding Guidelines
- Use Python type hints for public functions.
- Use clear `ValueError` messages for invalid user data.
- Use `logger` from [logger.py](logger.py) instead of `print()` in app code.
- Keep changes small and focused.
- Prefer standard library features over extra dependencies.

## Testing Guidelines
- Use pytest.
- Add tests with fixtures where useful.
- Include happy-path, edge-case, and error-path tests.
- Add security tests for path traversal fixes.
- When the trainer requests the final state, raise coverage to 90%+.

## Documentation Guidelines
- Update [CHANGELOG.md](CHANGELOG.md) for meaningful changes.
- Update [README.md](README.md) when behavior or commands change.
- Keep [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) accurate if adding or removing demo issues.