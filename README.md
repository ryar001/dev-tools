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

### 🤖 `run_ai_tracker`

**The intelligent autopilot for your git workflow.**

Stop manually writing changelogs and commit messages. This tool analyzes your code changes to handle the entire release process for you.

#### Workflow
1.  **🔍 Safety First**: Scans your Python files with `ruff` to catch syntax errors before committing.
2.  **🧠 AI Analysis**: Uses Gemini to analyze your `git diff`, understanding context and intent.
3.  **📝 Smart Summaries**: Automatically generates a categorized changelog and prepends it to `UPDATES.md`(will create if not exists).
4.  **🏷️ Auto-Versioning**: Intelligently determines the semantic version bump (Major, Minor, Patch) based on the nature of your changes.
5.  **💾 Commit & Tag**: Commits with a Conventional Commit message and creates a git tag (e.g., `v1.2.3`).


#### Arguments
| Argument | Type | Description | Default |
|----------|------|-------------|---------|
| `path` | `str` | Absolute path to your project root. | **Required** |
| `force` | `bool` | Bypass safety checks (e.g., ruff errors) and force the commit. | `False` |
| `version_bump` | `str` | Manually specify the version bump (`major`, `minor`, `patch`, `none`). If omitted, the AI decides. | `None` |
| `commit_hash` | `str` | Generate the diff from a specific commit hash instead of staged changes. | `None` |

## Development

```bash
# Install dependencies
uv sync

# Run locally for testing
uvx dev-mcp --help
```
