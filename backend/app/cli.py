"""Shortcut commands exposed via `uv run <name>` (see [project.scripts] in pyproject.toml)."""

import subprocess
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent

def dev() -> None:
    """Run the FastAPI development server with auto-reload."""
    subprocess.run(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload"], check=True
    )


def test() -> None:
    """Run the test suite."""
    subprocess.run([sys.executable, "-m", "pytest"], check=True)


def migrate() -> None:
    """Apply database migrations up to the latest revision."""
    subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        check=True,
        cwd=BACKEND_DIR,
    )


def make_migrations() -> None:
    """Generate a new migration script. Usage: uv run make-migrations "message"."""
    if len(sys.argv) < 2:
        print('Usage: uv run make-migrations "describe your change"', file=sys.stderr)
        raise SystemExit(1)
    message = sys.argv[1]
    subprocess.run(
        [sys.executable, "-m", "alembic", "revision", "--autogenerate", "-m", message],
        check=True,
                cwd=BACKEND_DIR,
    )