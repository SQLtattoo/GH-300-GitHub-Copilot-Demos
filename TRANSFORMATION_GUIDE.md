# Transformation Guide

Budget Buddy is a demo-start application. The intended transformation is from a low-coverage, happy-path budget tracker into a more robust app using GitHub Copilot.

## Starter State

- App runs successfully from [main.py](main.py).
- Starter tests pass.
- Coverage is intentionally around 30%.
- Known issues are listed in [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md).

## Target State

- 90%+ coverage.
- Clear validation errors.
- Path traversal blocked.
- CSV errors are understandable.
- Slow O(n^2) processing is refactored.
- New features have tests and docs.
- CHANGELOG is updated.

## Recommended Transformation Order

1. Generate calculator edge-case tests.
2. Fix calculator bugs.
3. Generate file-handler security tests.
4. Fix path traversal.
5. Add CSV malformed-row tests.
6. Refactor transaction processing performance issues.
7. Add missing feature TODOs with tests.
8. Raise coverage threshold to 90.
9. Update documentation and changelog.
10. Generate PR summary.

## Teaching Point

The value is not just the final code. The value is showing Copilot participating in the whole engineering loop: understand, plan, edit, test, debug, harden, document, and summarize.