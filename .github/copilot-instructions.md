# GitHub Copilot Demo Starter Kit – Instructions for AI Agents

## 🎯 Project Purpose

This is a **training/demo repository** intentionally containing bugs, security vulnerabilities, and incomplete implementations to showcase GitHub Copilot's capabilities. Use this context when:
- Fixing bugs (they're intentional teaching moments)
- Addressing security issues (e.g., `eval()`, path traversal)
- Completing TODO comments

**For Presenters**: The `main` branch has complete tests (227+). Run `.\reset_for_demo.ps1` before demos to create minimal test stubs for demonstrating Copilot's test generation. The script backs up original tests automatically.

## 🏗️ Architecture & Components

### Core Modules (Intentionally Flawed for Demos)
- **[calculator.py](../calculator.py)** - Arithmetic operations with empty list bugs, missing error handling, and TODOs
- **[data_processor.py](../data_processor.py)** - Data manipulation with O(n²) performance issues, `eval()` injection vulnerability
- **[file_handler.py](../file_handler.py)** - File I/O with path traversal vulnerabilities and encoding issues
- **[data_table.py](../data_table.py)** - Generic table component with sorting, pagination, search (framework-agnostic)
- **[logger.py](../logger.py)** - Centralized logging system (production-ready reference)
- **[main.py](../main.py)** - Demo orchestration showing all modules working together

### Test Suite Structure
- **tests/** - Comprehensive tests achieving 90%+ coverage (per [pytest.ini](../pytest.ini))
  - `conftest.py` - Shared fixtures (e.g., `calculator` fixture)
  - `test_*.py` - Module-specific tests organized by test classes (e.g., `TestBasicOperations`)
  - Security tests validate fixes for intentional vulnerabilities

## 🔧 Developer Workflows

### Environment Setup (CRITICAL - Always Run First)
```powershell
# Automated setup (preferred)
.\setup_demo.ps1

# Manual activation before ANY Python command
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac

# Install dependencies
pip install -r requirements-test.txt
```

### Testing Commands
```powershell
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_calculator.py

# Run tests by marker
pytest -m security         # Security-related tests
pytest -m "not slow"       # Skip slow tests

# Coverage report
pytest --cov=. --cov-report=html
```

### Key Files for Demo Flow
1. **[README.md](../README.md)** - Demo capabilities, setup instructions, model selection guide
2. **[TRANSFORMATION_GUIDE.md](../TRANSFORMATION_GUIDE.md)** - Step-by-step journey from buggy to production code
3. **[CHANGELOG.md](../CHANGELOG.md)** - MUST UPDATE on every change (Keep a Changelog format)
4. **[modelDecisionTree.md](../modelDecisionTree.md)** - Copilot model selection guidance for presenters

## 📝 Coding Conventions

### Python Style
- **Type hints required** - All function signatures must include types
- **Docstrings format** - Google style with Args, Returns, Raises, Examples sections
- **Error handling** - Use descriptive `ValueError` messages, validate inputs explicitly
- **Logging** - Import and use `logger` from [logger.py](../logger.py), never `print()`

### Examples from Codebase
```python
# ✅ Good - From calculator.py
def divide(self, a: float, b: float) -> float:
    """Divide a by b and return the result."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    result = a / b
    self.history.append(f"divide({a}, {b}) = {result}")
    return result

# ✅ Good - From data_processor.py (security fix)
def calculate_expression(self, expression: str) -> float:
    """Safe arithmetic parser using AST (no eval)."""
    try:
        node = ast.parse(expression, mode='eval').body
        return self._eval_expr(node)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")
```

### Security Patterns
- **Never use `eval()`** - Replace with `ast.parse()` + safe evaluation (see [data_processor.py](../data_processor.py#L200-220))
- **Path traversal validation** - Use `os.path.commonpath()` to validate paths (see [file_handler.py](../file_handler.py#L150-170))
- **Input validation** - Check for None, empty strings, invalid types before processing

## 🧪 Testing Requirements

### Coverage & Structure
- **Minimum coverage: 90%** (enforced by [pytest.ini](../pytest.ini#L23))
- **Test organization** - Group related tests in classes (e.g., `TestBasicOperations`, `TestSecurityFeatures`)
- **Fixtures** - Define shared objects in [tests/conftest.py](../tests/conftest.py)

### Test Patterns from Codebase
```python
# Parametrized tests for edge cases
@pytest.mark.parametrize("input,expected", [
    ("", ValueError),
    (None, ValueError),
    ("   ", ValueError)
])
def test_edge_cases(calculator, input, expected):
    with pytest.raises(expected):
        calculator.validate_input(input)

# Security test markers
@pytest.mark.security
def test_eval_injection_prevented(processor):
    """Ensure eval() vulnerability is fixed."""
    with pytest.raises(ValueError):
        processor.calculate_expression("__import__('os').system('ls')")
```

## 🎓 Demo-Specific Guidance

### When Fixing Intentional Bugs
1. Check [TRANSFORMATION_GUIDE.md](../TRANSFORMATION_GUIDE.md) for context on what the bug demonstrates
2. Document the fix in [CHANGELOG.md](../CHANGELOG.md) using Keep a Changelog format
3. Add tests proving the bug is fixed (especially for security issues)

### When Completing TODOs
TODOs are teaching moments - generate:
- Complete implementation with type hints
- Comprehensive docstring
- Operation history logging (for Calculator class)
- Unit tests in corresponding `tests/test_*.py` file

### Common Demo Operations
```python
# Adding operation history (Calculator pattern)
result = a + b
self.history.append(f"operation({a}, {b}) = {result}")

# Incrementing processed count (DataProcessor pattern)
self.processed_count += 1

# Using centralized logger
from logger import logger
logger.info("Processing started")
```

## 📊 Project Metrics
- **Test suite**: 227+ comprehensive tests (per README)
- **Coverage target**: 90%+ with `--cov-fail-under=90`
- **Test execution**: Use pytest-xdist for parallel runs
- **Documentation**: Every public method requires docstring

## 🚫 What NOT to Do
- Don't fix bugs without checking if they're intentional teaching examples
- Don't use generic security advice - implement specific patterns from this codebase
- Don't skip CHANGELOG.md updates (required for all changes)
- Don't run Python commands without activating `.venv` first
- Don't use `print()` - always use `logger` from [logger.py](../logger.py)

## 📚 Key References
- [README.md](../README.md) - Capabilities, setup, demo flow
- [TRANSFORMATION_GUIDE.md](../TRANSFORMATION_GUIDE.md) - Complete evolution from buggy to production
- [QUICK_REFERENCE.md](../QUICK_REFERENCE.md) - Auto-generated command cheatsheet
- [pytest.ini](../pytest.ini) - Test configuration, markers, coverage settings
