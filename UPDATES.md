What's New:
  pyproject.toml:
    - Updated project version from "0.4.0" to "0.4.1".

2025-12-09

What's New
- AGENT.md: Added AI Coding Assistant Instructions.
- src/dev_mcp/main.py:
  - Introduced main CLI entry point for dev_mcp tools.
  - Implemented `_run_script` for executing shell scripts, handling permissions and environment.
  - Integrated `ai-tracker.sh` as a `mcp.tool()` via `run_ai_tracker` with arguments for force, version bump, and commit hash.
  - Implemented dynamic argparse for CLI tools.

Refactor
- .gitignore: Added ignore patterns for `.env` files and all dot files (`.*`).

Chore
- pyproject.toml: Updated project version to 0.1.4.
- uv.lock: Added new dependency lock file.

Configuration:
- pyproject.toml: Added configuration for `setuptools` to find packages within the `src` directory.

What's New
- pyproject.toml: Updated project version to 0.1.3.

Refactor:
- dev_mcp.py: Deleted legacy script.

What's New:
- pyproject.toml:
  - Configured project build system with setuptools.
  - Updated project version to 0.1.2.
  - Defined 'dev-mcp' console script entry point.
  - Included 'ai-tracker.sh' as package data.

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
