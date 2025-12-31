# Demo Reset Script
# Removes completed tests to demonstrate GitHub Copilot test generation

Write-Host "🔄 Resetting repository for demo..." -ForegroundColor Cyan

# Create backup
$backupDir = "tests_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "📦 Creating backup in $backupDir..." -ForegroundColor Yellow
Copy-Item -Path "tests" -Destination $backupDir -Recurse

# Keep only conftest.py and minimal test stubs
$testFiles = @(
    "tests\test_calculator.py",
    "tests\test_data_processor.py",
    "tests\test_file_handler.py",
    "tests\test_data_table.py",
    "tests\test_logger.py"
)

# Create minimal test stubs
foreach ($testFile in $testFiles) {
    $moduleName = ($testFile -replace "tests\\test_", "" -replace ".py", "")
    
    $stubContent = @"
"""
Tests for $moduleName module.
Demo: Use GitHub Copilot to generate comprehensive tests.
"""

import pytest


# TODO: Generate tests using GitHub Copilot
# Tip: Use Ctrl+I and ask "Generate comprehensive tests for $moduleName"
# Or use /tests command in Copilot Chat


class TestBasicOperations:
    """Basic test class - use Copilot to generate test methods."""
    
    def test_placeholder(self):
        """Placeholder test - replace with real tests."""
        # Use Copilot to generate test for basic functionality
        pass


# Demo Scenarios:
# 1. Select a function in $moduleName.py
# 2. Use /tests command in Copilot Chat
# 3. Or use inline chat (Ctrl+I) to generate specific tests
# 4. Show parametrized tests for edge cases
# 5. Demonstrate mock generation for file operations

"@
    
    Set-Content -Path $testFile -Value $stubContent -Encoding UTF8
}

Write-Host "✅ Demo reset complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Run 'pytest' to see minimal test coverage"
Write-Host "  2. Open test files and use Copilot to generate tests"
Write-Host "  3. Demonstrate /tests command in Copilot Chat"
Write-Host ""
Write-Host "🔙 To restore: Copy from $backupDir back to tests/" -ForegroundColor Yellow
