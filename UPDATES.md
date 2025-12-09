Docs:
  README.md:
    - Added comprehensive documentation for Dev Tools MCP Server, including features (ai-tracker.sh), installation instructions, MCP server configuration, run_ai_tracker tool arguments, and development setup.
Tests:
  tests/dev_mcp/test_main.py:
    - Added unit tests for the `run_ai_tracker` command, covering CLI and `uvx` execution with `--help` and basic execution checks.
Build:
  pyproject.toml:
    - Updated project version from 0.0.1 to 0.6.0.

What's New (2025-12-09)
  src/dev_mcp/main.py
    main: Implemented default MCP server mode activation when main.py is executed without command-line arguments.
    _run_ai_tracker_impl: Added support for force, commit_hash, and version_bump arguments to be passed to ai-tracker.sh.
Refactor
  src/dev_mcp/main.py
    _run_ai_tracker_impl: Refined script location logic to robustly find ai-tracker.sh in both development (relative path) and installed (package resources) environments. Ensured execution from the project root (cwd=Path.cwd()).

### Dependency Update
- `uv.lock`: Updated `uv.lock` to version `0.5.2`.

What's New:
- pyproject.toml: Updated project version to 0.5.2.

What's New:
- src/dev_mcp/main.py: Added logic to conditionally start the `mcp` server when `--mcp-port` argument is present.

Warnings:
  No breakpoints detected.

What's New:
  - pyproject.toml:
    - Project version updated to 0.5.1.

What's New
- src/dev_mcp/main.py:
  - Added import for `typing` module.
  - Implemented automatic population of `argparse` choices for parameters with `typing.Literal` and `Optional[typing.Literal]` type hints.
  - Updated type hint for `version_bump` parameter to `Optional[Literal["major", "minor", "patch", "none"]]`.
  - Clarified description for `version_bump` parameter.

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
