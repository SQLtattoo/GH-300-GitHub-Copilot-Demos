"""Shared pytest fixtures and the per-module coverage gate for Budget Buddy.

Coverage is enforced per module (not as an average): every source module must
reach at least ``MODULE_COVERAGE_THRESHOLD`` percent line coverage or the test
session fails.
"""

from pathlib import Path
from typing import Dict, List, Tuple

import pytest


Transaction = Dict[str, object]

# Minimum line coverage required for EACH source module (not the average).
MODULE_COVERAGE_THRESHOLD = 80.0


@pytest.fixture
def sample_transactions() -> List[Transaction]:
    """Return a small, predictable set of income and expense transactions."""
    return [
        {"date": "2024-01-05", "merchant": "Employer", "category": "Salary", "amount": 3000.0, "type": "income"},
        {"date": "2024-01-06", "merchant": "Grocer", "category": "Groceries", "amount": 200.0, "type": "expense"},
        {"date": "2024-01-07", "merchant": "Cafe", "category": "Dining", "amount": 50.0, "type": "expense"},
        {"date": "2024-01-08", "merchant": "Utility Co", "category": "Utilities", "amount": 150.0, "type": "expense"},
    ]


def _is_project_source(path: Path, rootpath: Path) -> bool:
    """Return True when a measured file is one of our source modules."""
    try:
        relative = path.relative_to(rootpath)
    except ValueError:
        return False

    parts = relative.parts
    if not parts or not parts[-1].endswith(".py"):
        return False
    if parts[0] in {"tests", ".venv"}:
        return False
    if "site-packages" in parts:
        return False
    return True


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus) -> None:
    """Fail the session if any source module falls below the per-module gate."""
    config = session.config
    cov_plugin = config.pluginmanager.get_plugin("_cov")
    if cov_plugin is None:
        return

    controller = getattr(cov_plugin, "cov_controller", None)
    cov = getattr(controller, "cov", None) if controller is not None else None
    if cov is None:
        return

    rootpath = Path(config.rootpath)
    coverage_data = cov.get_data()

    below_threshold: List[Tuple[str, float]] = []
    for filename in coverage_data.measured_files():
        path = Path(filename)
        if not _is_project_source(path, rootpath):
            continue
        try:
            _, statements, _, missing, _ = cov.analysis2(filename)
        except Exception:  # pragma: no cover - defensive against odd files
            continue

        total = len(statements)
        if total == 0:
            continue

        percent = (total - len(missing)) / total * 100
        if percent < MODULE_COVERAGE_THRESHOLD:
            below_threshold.append((str(path.relative_to(rootpath)), percent))

    if below_threshold:
        below_threshold.sort()
        session.exitstatus = 1
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        if reporter is not None:
            reporter.write_line("")
            reporter.write_line(
                f"FAIL per-module coverage gate not met "
                f"(minimum {MODULE_COVERAGE_THRESHOLD:.0f}% per module):",
                red=True,
            )
            for name, percent in below_threshold:
                reporter.write_line(f"  {name}: {percent:.0f}%", red=True)
