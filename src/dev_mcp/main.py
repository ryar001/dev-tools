import asyncio
import os
from pathlib import Path
from typing import Optional, Literal
import argparse
import importlib.resources
from fastmcp import FastMCP
import inspect

# Initialize a standalone MCP server for development tools
mcp = FastMCP("Dev Tools")


async def _run_script(script_path: str, args: list[str], cwd: Path) -> str:
    """
    Core implementation for running a script.
    """
    command = [script_path] + args

    try:
        # Check if script exists and is executable
        if not os.path.exists(script_path):
            return f"Error: Script not found at {script_path}"

        if not os.access(script_path, os.X_OK):
            # Try to make it executable
            try:
                os.chmod(script_path, 0o755)
            except Exception as e:
                return f"Error: Script is not executable and chmod failed: {e}"

        # Prepare environment with /opt/homebrew/bin in PATH
        env = os.environ.copy()
        current_path = env.get("PATH", "")
        if "/opt/homebrew/bin" not in current_path:
            env["PATH"] = f"/opt/homebrew/bin:{current_path}"

        # Execute the script
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env,
        )

        stdout, stderr = await process.communicate()

        output = ""
        if stdout:
            output += f"STDOUT:\n{stdout.decode()}\n"
        if stderr:
            output += f"STDERR:\n{stderr.decode()}\n"

        if process.returncode != 0:
            return f"Command failed with return code {process.returncode}:\n{output}"

        return f"Success:\n{output}"

    except Exception as e:
        return f"Error running script {script_path}: {str(e)}"


async def _run_ai_tracker_impl(
    force: bool = False,
    version_bump: Literal["major", "minor", "patch", "none"] = "patch",
    commit_hash: Optional[str] = None,
) -> str:
    """
    Core implementation for running the ai-tracker.sh script.
    """
    tool_name = "ai-tracker.sh"
    with importlib.resources.as_file(
        importlib.resources.files("tools").joinpath(tool_name)
    ) as script_path:
        # Construct command arguments
        args = []

        if force:
            args.append("force")

        if commit_hash:
            args.extend(["-r", commit_hash])

        if version_bump:
            args.extend(["-v", version_bump])

        return await _run_script(
            script_path=str(script_path),
            args=args,
            # We need to run this in the project root
            cwd=Path.cwd(),
        )


@mcp.tool()
async def run_ai_tracker(
    force: bool = False,
    version_bump: Literal["major", "minor", "patch", "none"] = "patch",
    commit_hash: Optional[str] = None,
) -> str:
    """
    Run the ai-tracker.sh script to track changes, generate AI summaries, and commit.

    Args:
        force: Ignore AI-detected errors and proceed with commit (default: False).
        version_bump: How to bump the version (default: "patch").
        commit_hash: Optional commit hash to generate diff from.
    """
    return await _run_ai_tracker_impl(
        force=force, version_bump=version_bump, commit_hash=commit_hash
    )


def main():
    """Run a dev tool from the command line."""

    async def async_main():
        parser = argparse.ArgumentParser(description="Run a dev tool.")
        subparsers = parser.add_subparsers(dest="tool_name", required=True, help="Available tools")

        tools = await mcp.get_tools()
        for tool_name, tool_object in tools.items():
            tool_func = tool_object.fn
            doc = tool_func.__doc__ or f"Run {tool_name}"
            help_text = doc.strip().split("\n")[0]
            tool_parser = subparsers.add_parser(
                tool_name,
                help=help_text,
                description=doc,
                formatter_class=argparse.RawDescriptionHelpFormatter,
            )
            sig = inspect.signature(tool_func)

            for param in sig.parameters.values():
                arg_name = f"--{param.name.replace('_', '-')}"
                kwargs = {"dest": param.name}

                annotation = param.annotation
                origin = getattr(annotation, "__origin__", None)

                if origin is Literal:
                    kwargs["choices"] = annotation.__args__

                if annotation is bool and param.default is False:
                    kwargs["action"] = "store_true"
                else:
                    # Good enough for now for non-bools
                    kwargs["type"] = str

                if param.default is not inspect.Parameter.empty:
                    kwargs["default"] = param.default
                    kwargs["help"] = f"Default: {param.default}"
                else:
                    kwargs["required"] = True

                # Don't add 'type' for boolean flags
                if "action" in kwargs and "type" in kwargs:
                    del kwargs["type"]

                tool_parser.add_argument(arg_name, **kwargs)

        args = parser.parse_args()
        tool_to_run = tools[args.tool_name].fn

        tool_args = vars(args)
        del tool_args["tool_name"]

        if inspect.iscoroutinefunction(tool_to_run):
            result = await tool_to_run(**tool_args)
        else:
            result = tool_to_run(**tool_args)

        print(result)

    asyncio.run(async_main())

if __name__ == "__main__":
    main()