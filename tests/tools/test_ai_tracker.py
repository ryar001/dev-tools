
import pytest
import subprocess
import os
from pathlib import Path

# Path to the script under test
# Assuming tests/tools/test_ai_tracker.py location
SCRIPT_PATH = Path(__file__).parents[2] / "src" / "tools" / "ai-tracker.sh"

@pytest.fixture
def mock_apps_dir(tmp_path):
    """Creates a directory with mock executables for gemini and ruff."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    
    # Mock gemini
    gemini_path = bin_dir / "gemini"
    gemini_content = """#!/bin/bash
# Read stdin to consume it (simulating reading prompt)
while read -r line; do :; done

echo "==SUMMARY_START=="
echo "This is a mock summary."
echo "- Updated things."
echo "==SUMMARY_END=="
echo "==COMMIT_MSG_START=="
echo "feat: mock commit"
echo ""
echo "This is a mock body."
echo "==COMMIT_MSG_END=="
"""
    gemini_path.write_text(gemini_content)
    gemini_path.chmod(0o755)

    # Mock ruff (always passes by default)
    ruff_path = bin_dir / "ruff"
    ruff_content = """#!/bin/bash
exit 0
"""
    ruff_path.write_text(ruff_content)
    ruff_path.chmod(0o755)
    
    return bin_dir

@pytest.fixture
def mock_ruff_fail(mock_apps_dir):
    """Updates mock ruff to fail."""
    ruff_path = mock_apps_dir / "ruff"
    ruff_content = """#!/bin/bash
echo "Syntax error found"
exit 1
"""
    ruff_path.write_text(ruff_content)
    ruff_path.chmod(0o755)
    return mock_apps_dir

@pytest.fixture
def git_repo(tmp_path):
    """Initializes a temp git repo."""
    cwd = os.getcwd()
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    os.chdir(repo_dir)
    
    # Initialize git
    subprocess.run(["git", "init", "--initial-branch=main"], check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
    
    # Initial commit to simulate existing state
    (repo_dir / "README.md").write_text("# Test Repo")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
    
    yield repo_dir
    
    os.chdir(cwd)

def run_tracker(args, env_overrides=None):
    """Helper to run the tracker script."""
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)
        
    cmd = [str(SCRIPT_PATH)] + args
    return subprocess.run(cmd, capture_output=True, text=True, env=env)

def test_not_in_git_repo(tmp_path, mock_apps_dir):
    """Should fail if not in a git repo."""
    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        res = run_tracker([], env_overrides={"PATH": f"{mock_apps_dir}:{os.environ['PATH']}"})
        assert res.returncode == 1
        assert "Not in a git repository" in res.stdout or "Not in a git repository" in res.stderr
    finally:
        os.chdir(cwd)

def test_no_changes(git_repo, mock_apps_dir):
    """Should exit if no staged changes."""
    # Ensure version file exists so it doesn't get created and staged
    (git_repo / "__version__.py").write_text('__version__ = "0.0.1"')
    subprocess.run(["git", "add", "__version__.py"], check=True)
    subprocess.run(["git", "commit", "-m", "add version"], check=True)

    # Don't modify anything
    
    # By default script looks at staged changes if no -r
    res = run_tracker([], env_overrides={"PATH": f"{mock_apps_dir}:{os.environ['PATH']}"})
    
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)

    assert res.returncode == 0
    assert "No relevant changes found" in res.stdout

def test_basic_flow_patch(git_repo, mock_apps_dir):
    """Test standard flow with staged changes."""
    # Create a new python file
    (git_repo / "src").mkdir()
    (git_repo / "src" / "test.py").write_text("print('hello')")
    subprocess.run(["git", "add", "."], check=True)
    
    res = run_tracker([], env_overrides={"PATH": f"{mock_apps_dir}:{os.environ['PATH']}"})
    
    # Debug output if fail
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)

    assert res.returncode == 0
    assert "Version will be updated" in res.stdout
    assert "Updated __version__.py" in res.stdout
    
    # Check version file
    version_file = git_repo / "__version__.py"
    assert version_file.exists()
    # Script behavior:
    # 1. Missing file -> creates 0.0.1
    # 2. Reads 0.0.1
    # 3. Patch bump -> 0.0.2
    assert '__version__ = "0.0.2"' in version_file.read_text()
    
    # Check UPDATES.md
    updates_file = git_repo / "UPDATES.md"
    assert updates_file.exists()
    assert "This is a mock summary" in updates_file.read_text()
    
    # Check git log
    log = subprocess.run(["git", "log", "-1", "--pretty=%s"], capture_output=True, text=True).stdout.strip()
    assert log == "feat: mock commit"
    
    # Check tag
    tags = subprocess.run(["git", "tag"], capture_output=True, text=True).stdout.strip()
    assert "v0.0.2" in tags

def test_pyproject_update(git_repo, mock_apps_dir):
    """Test pyproject.toml update logic."""
    # Setup __version__.py and pyproject.toml to match
    version_file = git_repo / "__version__.py"
    version_file.write_text('__version__ = "1.0.0"')
    
    pyproject = git_repo / "pyproject.toml"
    pyproject.write_text('[project]\nversion = "1.0.0"\nname="test"')
    
    subprocess.run(["git", "add", "pyproject.toml", "__version__.py"], check=True)
    subprocess.run(["git", "commit", "-m", "Add version files"], check=True)
    
    # Make a change to trigger the tracker
    (git_repo / "README.md").write_text("Changed")
    subprocess.run(["git", "add", "README.md"], check=True)
    
    res = run_tracker(["-v", "patch"], env_overrides={"PATH": f"{mock_apps_dir}:{os.environ['PATH']}"})
    assert res.returncode == 0
    
    # Check pyproject.toml updated to 1.0.1
    content = pyproject.read_text()
    assert 'version = "1.0.1"' in content
    assert '__version__ = "1.0.1"' in version_file.read_text()

def test_pyproject_update_preserves_formatting(git_repo, mock_apps_dir):
    """Test pyproject.toml update logic preserves indentation."""
    # Setup __version__.py and pyproject.toml to match
    version_file = git_repo / "__version__.py"
    version_file.write_text('__version__ = "1.0.0"')
    
    pyproject = git_repo / "pyproject.toml"
    # Note the indentation before version
    pyproject.write_text('[project]\n    version = "1.0.0"\nname="test"')
    
    subprocess.run(["git", "add", "pyproject.toml", "__version__.py"], check=True)
    subprocess.run(["git", "commit", "-m", "Add version files"], check=True)
    
    # Make a change
    (git_repo / "README.md").write_text("Changed")
    subprocess.run(["git", "add", "README.md"], check=True)
    
    res = run_tracker(["-v", "patch"], env_overrides={"PATH": f"{mock_apps_dir}:{os.environ['PATH']}"})
    assert res.returncode == 0
    
    # Check pyproject.toml updated to 1.0.1 AND indentation preserved
    content = pyproject.read_text()
    assert '    version = "1.0.1"' in content

def test_ruff_failure_no_force(git_repo, mock_ruff_fail):
    """Should fail if ruff fails and no force flag."""
    # Create python file to trigger ruff check
    (git_repo / "bad.py").write_text("this is bad syntax")
    subprocess.run(["git", "add", "."], check=True)
    
    res = run_tracker([], env_overrides={"PATH": f"{mock_ruff_fail}:{os.environ['PATH']}"})
    assert res.returncode == 1
    assert "Ruff found errors" in res.stderr

def test_ruff_failure_with_force(git_repo, mock_ruff_fail):
    """Should succeed if ruff fails but force flag is used."""
    # Create python file
    (git_repo / "bad.py").write_text("this is bad syntax")
    subprocess.run(["git", "add", "."], check=True)
    
    res = run_tracker(["force"], env_overrides={"PATH": f"{mock_ruff_fail}:{os.environ['PATH']}"})
    
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        
    assert res.returncode == 0
    assert "Force mode enabled" in res.stdout
    assert "Ruff found errors, but force mode is on" in res.stdout

def test_version_bump_options(git_repo, mock_apps_dir):
    """Test -v argument."""
    # Setup existing version
    version_file = git_repo / "__version__.py"
    version_file.write_text('__version__ = "1.0.0"')
    subprocess.run(["git", "add", "__version__.py"], check=True)
    subprocess.run(["git", "commit", "-m", "Ver"], check=True)
    
    # Change
    (git_repo / "README.md").write_text("Changed")
    subprocess.run(["git", "add", "README.md"], check=True)
    
    # Test major bump
    res = run_tracker(["-v", "major"], env_overrides={"PATH": f"{mock_apps_dir}:{os.environ['PATH']}"})
    assert res.returncode == 0
    assert '__version__ = "2.0.0"' in version_file.read_text()
    
