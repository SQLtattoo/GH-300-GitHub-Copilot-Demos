# Runs the Budget Buddy test suite with a coverage report.
$ErrorActionPreference = "Stop"

if (Test-Path ".\.venv\Scripts\python.exe") {
    $python = ".\.venv\Scripts\python.exe"
}
else {
    $python = "python"
}

& $python -m pytest --cov=. --cov-report=term-missing
