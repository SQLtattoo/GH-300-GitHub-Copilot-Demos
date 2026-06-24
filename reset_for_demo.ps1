# Reset helper for Budget Buddy demos

Write-Host "Budget Buddy demo reset guidance" -ForegroundColor Cyan
Write-Host ""
Write-Host "This repo is already in the demo-start state." -ForegroundColor Green
Write-Host "If you generated tests or fixes during a demo, restore tracked files with:" -ForegroundColor Yellow
Write-Host "  git restore ." -ForegroundColor White
Write-Host ""
Write-Host "Then verify the baseline:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\python.exe main.py" -ForegroundColor White
Write-Host "  .\.venv\Scripts\python.exe -m pytest" -ForegroundColor White