#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
REQUIREMENTS_STAMP="$VENV_DIR/.requirements-installed"

if [[ ! -x "$PYTHON_BIN" ]]; then
    if command -v python3 >/dev/null 2>&1; then
        SYSTEM_PYTHON="python3"
    elif command -v python >/dev/null 2>&1; then
        SYSTEM_PYTHON="python"
    else
        echo "Python is required, but neither python3 nor python was found." >&2
        exit 1
    fi

    echo "Creating virtual environment in .venv..."
    "$SYSTEM_PYTHON" -m venv "$VENV_DIR"
fi

if [[ ! -f "$REQUIREMENTS_STAMP" || "$REQUIREMENTS_FILE" -nt "$REQUIREMENTS_STAMP" ]]; then
    echo "Installing requirements..."
    "$PYTHON_BIN" -m pip install --upgrade pip
    "$PYTHON_BIN" -m pip install -r "$REQUIREMENTS_FILE"
    touch "$REQUIREMENTS_STAMP"
fi

cd "$PROJECT_DIR"
exec "$PYTHON_BIN" "$PROJECT_DIR/main.py"
