# GitHub Copilot – Project Guidelines

## ✅ Coding Style
- Follow the project’s linting rules (`.eslintrc.json` for JS/TS, `.pylintrc` for Python).
- Use **single quotes** for strings in JS/TS.
- Always terminate statements with `;` in JS/TS.
- Prefer `const` and `let` over `var`.

## ✅ Security Practices
- Never hardcode secrets or credentials.
- Validate all external input using `utils/validators`.
- For cookies:
  - `httpOnly: true`
  - `secure: true`
  - `sameSite: 'strict'`
  - Set `maxAge` appropriately.
- Use parameterized queries for database access.

## ✅ Testing Requirements
- Generate unit tests for all new code.
- Use **Jest** for JS/TS and **pytest** for Python.
- Minimum coverage: **90%**.
- Include edge cases and error handling in tests.

## ✅ Python Environment
- **Always activate the virtual environment before installing packages or executing code:**
  - Windows: `.\.venv\Scripts\Activate.ps1`
  - Linux/Mac: `source .venv/bin/activate`
- Install dependencies: `pip install -r requirements-test.txt`
- Run tests: `pytest`

## ✅ Internal Libraries & APIs
- Use `logger` for logging instead of `console.log`.
- Use `fetchWithAuth` for authenticated API calls.
- Avoid direct calls to external APIs without wrappers.

## ✅ Documentation
- Document all public functions with JSDoc (JS/TS) or docstrings (Python).
- Include usage examples for complex functions.
- Update README when adding new features.

## ✅ Performance & Quality
- Optimize loops and avoid unnecessary nested iterations.
- Use async/await for asynchronous operations.
- Ensure code passes CI/CD checks before merging.

## ✅ Every time you make a change update the CHANGELOG.md file
- Follow the format in the existing CHANGELOG.md file.

---

### Notes for Copilot:
- Apply these rules when generating code, tests, or documentation.
- Suggest fixes if existing code violates these guidelines.