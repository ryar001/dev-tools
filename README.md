# Dev Tools MCP Server

A standalone Model Context Protocol (MCP) server that provides development tools for your LLM workspace.

## Features

- **ai-tracker.sh**: An intelligent git commit tracker that analyzes your changes, generates AI summaries, and handles version bumping automatically.

## Installation

### Prerequisite

- [uv](https://github.com/astral-sh/uv) installed (recommended)
- Python 3.12+

### 1. Install to your LLM Client (e.g., Claude Desktop, Cursor)

To use this with your LLM, you need to add it to your MCP configuration file.

#### Locate your config file:
- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS)
- **Cursor**: `Depending on valid configuration, usually in project root or global settings`
- **Gemini**: `~/.config/gemini/gemini.json`

#### Add the server configuration:
- uvx will auto install the tool and required packages
```json
{
  "mcpServers": {
    "dev-tools": {
      "command": "uvx",
      "args": [
        "dev-mcp"
      ]
    }
  }
}
```



## Tools

### `run_ai_tracker`

Runs the implementation of the AI Tracker script which:
1.  Checks for git changes.
2.  Generates a summary of changes.
3.  Updates `UPDATES.md`.
4.  Bumps the version (patch by default, or major/minor if specified).
5.  Commits and tags the release.

**Arguments:**
- `force` (bool): Ignore AI-detected errors and force commit. (Default: `False`)
- `version_bump` (string): 'major', 'minor', 'patch', or 'none'. (Default: `None` - AI determines bump)
- `commit_hash` (string): Optional specific commit hash to process. (Default: `None`)

## Development

```bash
# Install dependencies
uv sync

# Run locally for testing
uv run dev-mcp --help
```
