# GitHub Copilot Demo - Quick Reference

## 🚀 Getting Started

### Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Run Tests
```powershell
# All tests
python test_runner.py

# Specific test file
python -m pytest test_calculator.py -v

# With coverage
pytest --cov=. --cov-report=html
```

## 🎯 Key Demo Files

| File | Purpose |
|------|---------|
| calculator.py | Basic arithmetic with bugs and TODOs |
| data_processor.py | Data operations with performance issues |
| file_handler.py | File I/O with security vulnerabilities |
| test_*.py | Test files for each module |

## 💡 Copilot Commands

### In Editor
- **Accept suggestion**: Tab
- **Alternative suggestions**: Ctrl + Enter
- **Next suggestion**: Alt + ]
- **Previous suggestion**: Alt + [
- **Dismiss suggestion**: Esc

### Chat Commands
- /explain - Explain selected code
- /fix - Fix problems in selected code
- /tests - Generate tests for selected code
- /doc - Add documentation
- /optimize - Improve performance

### Inline Chat
- **Open inline chat**: Ctrl + I
- **Quick fixes**: Select code → Ctrl + .

## 🐛 Intentional Issues to Showcase

### calculator.py
- Line ~62: verage() - Empty list bug
- Line ~68: Circle methods - Duplicate PI constant
- Line ~80: divide_numbers() - Missing error handling
- Line ~96: get_first_element() - No empty check
- Line ~102: ormat_name() - No None/whitespace handling

### data_processor.py
- Line ~33: count_words() - Edge case bug
- Line ~41: ind_duplicates_slow() - O(n²) performance
- Line ~57: calculate_expression() - Security risk (eval)
- Line ~64: get_last_n_items() - Edge cases not handled

### file_handler.py
- Line ~49: 
ead_file_unsafe() - Path traversal vulnerability
- Line ~58: count_lines() - No encoding specified
- Line ~66: ppend_to_file() - Missing error handling

## 📝 Demo Flow Checklist

- [ ] Part 1: Environment setup (5 min)
- [ ] Part 2: Code completion (15 min)
- [ ] Part 3: Bug detection (15 min)
- [ ] Part 4: Refactoring (10 min)
- [ ] Part 5: Test generation (15 min)
- [ ] Part 6: Documentation (10 min)
- [ ] Part 7: Security issues (10 min)
- [ ] Part 8: Variations (10 min)
- [ ] Part 9: Learning (5 min)
- [ ] Part 10: Validation (5 min)


## 🔧 Troubleshooting

### Copilot not suggesting?
- Check status bar icon
- Press Ctrl + Enter to force suggestions
- Verify extension is active

### Tests failing?
- Ensure venv is activated
- Check Python version (3.8+)
- Verify all dependencies installed

### Import errors?
- Activate virtual environment
- Reinstall requirements: pip install -r requirements-test.txt

