
import unittest
import subprocess
import os
import sys
from pathlib import Path

class TestDevTools(unittest.TestCase):
    def setUp(self):
        # Ensure we are in the project root
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.src_path = self.project_root / "src"
        os.chdir(self.project_root)

    def test_cli_run_ai_tracker_help(self):
        """Test the CLI version of running ai-tracker help (to avoid side effects)."""
        cmd = [sys.executable, "src/dev_mcp/main.py", "run_ai_tracker", "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"CLI help command failed: {result.stderr}")
        self.assertIn("usage:", result.stdout)
        self.assertIn("Run the ai-tracker.sh script", result.stdout)

    def test_cli_run_ai_tracker_execution(self):
        """Test the CLI version of running ai-tracker execution."""
        # We'll run it, but we expect it might say 'No relevant changes found' or similar.
        # We mainly checking for crash (exit code 0).
        cmd = [sys.executable, "src/dev_mcp/main.py", "run_ai_tracker"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # It might return non-zero if the script itself fails, but based on user output it returns 0 on success.
        if result.returncode != 0:
            print(f"\nCLI Execution Stdout: {result.stdout}")
            print(f"CLI Execution Stderr: {result.stderr}")
        
        self.assertEqual(result.returncode, 0, f"CLI command failed: {result.stderr}")
        self.assertIn("Success", result.stdout)

    def test_uvx_run_ai_tracker_help(self):
        """Test the UVX version of running ai-tracker help."""
        cmd = ["uvx", "--from", ".", "dev-mcp", "run_ai_tracker", "--help"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0, f"UVX help command failed: {result.stderr}")
        self.assertIn("usage:", result.stdout)

    def test_uvx_run_ai_tracker_execution(self):
        """Test the UVX version of running ai-tracker execution."""
        cmd = ["uvx", "--from", ".", "dev-mcp", "run_ai_tracker"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"\nUVX Execution Stdout: {result.stdout}")
            print(f"UVX Execution Stderr: {result.stderr}")

        self.assertEqual(result.returncode, 0, f"UVX command failed: {result.stderr}")
        self.assertIn("Success", result.stdout)

if __name__ == "__main__":
    unittest.main()
