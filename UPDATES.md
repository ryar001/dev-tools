New Features:
- `__version__.py`: Initial version file added.
- `dev_mcp.py`:
    - `run_ai_tracker` is now registered as an MCP tool with `force`, `version_bump`, and `commit_hash` parameters.
    - Added `main` function to provide a command-line interface for `dev-mcp`.

Enhancements:
- `dev_mcp.py`:
    - Imports for `argparse` and `FastMCP` added.
    - `_run_ai_tracker_impl` updated to use new parameters.

Configuration:
- `pyproject.toml`:
    - Project name and description added.
    - CLI entry point `dev-mcp = "dev_mcp:main"` defined.

Dependencies:
- `pyproject.toml`: `fastmcp`, `pip`, and `ruff` added as project dependencies.
