"""Root entry point for local development.

Run locally:
    uv run python main.py

Or via the installed script:
    uv run fema-oversight-server
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from fema_oversight.app import main  # noqa: E402

if __name__ == "__main__":
    main()
