"""Root entry point for local development.

Run locally:
    uv run python main.py

Or via the installed script:
    uv run fema-oversight-server
"""

from fema_oversight.app import main

if __name__ == "__main__":
    main()
