# GitHub Copilot Demo - Setup Script
# This script sets up the complete environment for the demo

param(
    [switch]$SkipTests,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Colors for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Step {
    param([string]$Message)
    Write-ColorOutput "`n▶ $Message" "Cyan"
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "  ✓ $Message" "Green"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "  ✗ $Message" "Red"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "  ⚠ $Message" "Yellow"
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "  ℹ $Message" "Gray"
}

# Header
Clear-Host
Write-ColorOutput "═══════════════════════════════════════════════════════════" "Cyan"
Write-ColorOutput "  GitHub Copilot Demo - Environment Setup" "Cyan"
Write-ColorOutput "═══════════════════════════════════════════════════════════" "Cyan"
Write-Host ""

# Check prerequisites
Write-Step "Checking Prerequisites"

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Success "Python found: $pythonVersion"
    
    # Extract version number
    if ($pythonVersion -match 'Python (\d+)\.(\d+)\.(\d+)') {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Error "Python 3.8 or higher is required"
            exit 1
        }
    }
} catch {
    Write-Error "Python is not installed or not in PATH"
    Write-Info "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
}

# Check pip
try {
    $pipVersion = python -m pip --version 2>&1
    Write-Success "pip found: $pipVersion"
} catch {
    Write-Error "pip is not available"
    exit 1
}

# Check VS Code (optional)
try {
    $codeVersion = code --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "VS Code found"
    }
} catch {
    Write-Warning "VS Code not found in PATH (optional)"
}

# Virtual Environment Setup
Write-Step "Setting Up Virtual Environment"

$venvPath = ".venv"

if (Test-Path $venvPath) {
    if ($Force) {
        Write-Warning "Removing existing virtual environment..."
        Remove-Item -Recurse -Force $venvPath
    } else {
        Write-Warning "Virtual environment already exists"
        $response = Read-Host "Do you want to recreate it? (y/N)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Write-Info "Removing existing virtual environment..."
            Remove-Item -Recurse -Force $venvPath
        } else {
            Write-Info "Using existing virtual environment"
        }
    }
}

if (-not (Test-Path $venvPath)) {
    Write-Info "Creating virtual environment..."
    python -m venv $venvPath
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        exit 1
    }
    Write-Success "Virtual environment created: $venvPath"
} else {
    Write-Success "Virtual environment ready: $venvPath"
}

# Activate virtual environment
Write-Step "Activating Virtual Environment"

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"

if (-not (Test-Path $activateScript)) {
    Write-Error "Activation script not found: $activateScript"
    exit 1
}

Write-Info "Activating virtual environment..."
& $activateScript

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to activate virtual environment"
    exit 1
}

Write-Success "Virtual environment activated"

# Verify we're in venv
$pythonPath = (Get-Command python).Source
if ($pythonPath -notlike "*$venvPath*") {
    Write-Warning "Python is not running from virtual environment"
    Write-Info "Python path: $pythonPath"
} else {
    Write-Success "Confirmed running in virtual environment"
}

# Upgrade pip
Write-Step "Upgrading pip"

Write-Info "Upgrading pip to latest version..."
python -m pip install --upgrade pip --quiet

if ($LASTEXITCODE -eq 0) {
    $pipVersion = python -m pip --version
    Write-Success "pip upgraded: $pipVersion"
} else {
    Write-Warning "Failed to upgrade pip (continuing anyway)"
}

# Install dependencies
Write-Step "Installing Dependencies"

# Check for requirements files
$requirementsFiles = @()

if (Test-Path "requirements.txt") {
    $requirementsFiles += "requirements.txt"
}

if (Test-Path "requirements-test.txt") {
    $requirementsFiles += "requirements-test.txt"
}

if ($requirementsFiles.Count -eq 0) {
    Write-Info "No requirements files found, installing basic packages..."
    
    $basicPackages = @("pytest", "coverage", "pytest-cov")
    
    foreach ($package in $basicPackages) {
        Write-Info "Installing $package..."
        python -m pip install $package --quiet
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$package installed"
        } else {
            Write-Warning "Failed to install $package"
        }
    }
} else {
    foreach ($reqFile in $requirementsFiles) {
        Write-Info "Installing from $reqFile..."
        python -m pip install -r $reqFile --quiet
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Dependencies from $reqFile installed"
        } else {
            Write-Error "Failed to install dependencies from $reqFile"
            exit 1
        }
    }
}

# List installed packages
Write-Step "Installed Packages"
Write-Info "Current environment packages:"
python -m pip list

# Verify project structure
Write-Step "Verifying Project Structure"

$requiredFiles = @(
    "calculator.py",
    "data_processor.py",
    "file_handler.py",
    "test_calculator.py",
    "test_data_processor.py",
    "test_file_handler.py",
    "test_runner.py"
)

$allPresent = $true
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Success "$file found"
    } else {
        Write-Warning "$file not found"
        $allPresent = $false
    }
}

if (-not $allPresent) {
    Write-Warning "Some project files are missing"
    Write-Info "The demo may not work correctly"
}

# Run tests (optional)
if (-not $SkipTests) {
    Write-Step "Running Tests"
    
    Write-Info "Running test suite to verify setup..."
    python test_runner.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "All tests passed! Setup is complete and working."
    } else {
        Write-Warning "Some tests failed. The environment is set up, but there may be issues."
        Write-Info "This is expected if you haven't fixed the intentional bugs yet!"
    }
} else {
    Write-Info "Skipping tests (use -SkipTests:$false to run them)"
}

# Create VS Code settings
Write-Step "Configuring VS Code"

$vscodeDir = ".vscode"
$settingsFile = Join-Path $vscodeDir "settings.json"

if (-not (Test-Path $vscodeDir)) {
    Write-Info "Creating .vscode directory..."
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

if (-not (Test-Path $settingsFile) -or $Force) {
    Write-Info "Creating VS Code settings..."
    
    $settings = @{
        "python.defaultInterpreterPath" = "./.venv/Scripts/python.exe"
        "python.terminal.activateEnvironment" = $true
        "python.terminal.activateEnvInCurrentTerminal" = $true
        "python.testing.unittestEnabled" = $true
        "python.testing.unittestArgs" = @("-v", "-s", ".", "-p", "test_*.py")
        "python.testing.pytestEnabled" = $false
        "editor.formatOnSave" = $false
        "files.autoSave" = "off"
    } | ConvertTo-Json -Depth 10
    
    $settings | Out-File -FilePath $settingsFile -Encoding utf8
    Write-Success "VS Code settings created: $settingsFile"
} else {
    Write-Success "VS Code settings already exist: $settingsFile"
}

# Create quick reference
Write-Step "Creating Quick Reference"

$quickRefPath = "QUICK_REFERENCE.md"
$quickRefContent = @"
# GitHub Copilot Demo - Quick Reference

## 🚀 Getting Started

### Activate Virtual Environment
``````powershell
.\.venv\Scripts\Activate.ps1
``````

### Run Tests
``````powershell
# All tests
python test_runner.py

# Specific test file
python -m pytest test_calculator.py -v

# With coverage
pytest --cov=. --cov-report=html
``````

## 🎯 Key Demo Files

| File | Purpose |
|------|---------|
| calculator.py | Basic arithmetic with bugs and TODOs |
| data_processor.py | Data operations with performance issues |
| file_handler.py | File I/O with security vulnerabilities |
| test_*.py | Test files for each module |

## 💡 Copilot Commands

### In Editor
- **Accept suggestion**: `Tab`
- **Alternative suggestions**: `Ctrl + Enter`
- **Next suggestion**: `Alt + ]`
- **Previous suggestion**: `Alt + [`
- **Dismiss suggestion**: `Esc`

### Chat Commands
- `/explain` - Explain selected code
- `/fix` - Fix problems in selected code
- `/tests` - Generate tests for selected code
- `/doc` - Add documentation
- `/optimize` - Improve performance

### Inline Chat
- **Open inline chat**: `Ctrl + I`
- **Quick fixes**: Select code → `Ctrl + .`

## 🐛 Intentional Issues to Showcase

### calculator.py
- Line ~62: `average()` - Empty list bug
- Line ~68: Circle methods - Duplicate PI constant
- Line ~80: `divide_numbers()` - Missing error handling
- Line ~96: `get_first_element()` - No empty check
- Line ~102: `format_name()` - No None/whitespace handling

### data_processor.py
- Line ~33: `count_words()` - Edge case bug
- Line ~41: `find_duplicates_slow()` - O(n²) performance
- Line ~57: `calculate_expression()` - Security risk (eval)
- Line ~64: `get_last_n_items()` - Edge cases not handled

### file_handler.py
- Line ~49: `read_file_unsafe()` - Path traversal vulnerability
- Line ~58: `count_lines()` - No encoding specified
- Line ~66: `append_to_file()` - Missing error handling

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

## 🎓 Trainer Tips

1. **Start simple**: Begin with basic completion
2. **Show failures**: Demonstrate when Copilot needs guidance
3. **Be interactive**: Ask audience for suggestions
4. **Use real scenarios**: Emphasize practical applications
5. **Pause for questions**: After each major section

## 🔧 Troubleshooting

### Copilot not suggesting?
- Check status bar icon
- Press `Ctrl + Enter` to force suggestions
- Verify extension is active

### Tests failing?
- Ensure venv is activated
- Check Python version (3.8+)
- Verify all dependencies installed

### Import errors?
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements-test.txt`

## 📊 Success Metrics

After demo, participants should understand:
- ✅ How to use Copilot for code completion
- ✅ How to detect and fix bugs
- ✅ How to generate tests
- ✅ How to refactor code
- ✅ How to identify security issues
- ✅ How to improve documentation

---

"@

$quickRefContent | Out-File -FilePath $quickRefPath -Encoding utf8
Write-Success "Quick reference created: $quickRefPath"

# Summary
Write-Host ""
Write-ColorOutput "═══════════════════════════════════════════════════════════" "Green"
Write-ColorOutput "  Setup Complete!" "Green"
Write-ColorOutput "═══════════════════════════════════════════════════════════" "Green"
Write-Host ""

Write-ColorOutput "✓ Virtual environment: $venvPath" "Green"
Write-ColorOutput "✓ Dependencies installed" "Green"
Write-ColorOutput "✓ VS Code configured" "Green"
Write-ColorOutput "✓ Quick reference created" "Green"
Write-Host ""

Write-ColorOutput "Next Steps:" "Cyan"
Write-Host "  1. Open VS Code: code ."
Write-Host "  2. Review QUICK_REFERENCE.md for guidance"
Write-Host "  3. Start demonstrating GitHub Copilot!"
Write-Host ""

Write-ColorOutput "Quick Commands:" "Yellow"
Write-Host "  Run all tests:        pytest"
Write-Host "  Run specific test:    pytest tests/test_calculator.py -v"
Write-Host "  Run with coverage:    pytest --cov=. --cov-report=html"
Write-Host ""

Write-ColorOutput "Happy Demoing! 🚀" "Cyan"
