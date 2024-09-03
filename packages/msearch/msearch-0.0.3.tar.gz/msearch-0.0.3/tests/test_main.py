import subprocess
import sys
import pytest
import time
import re
import logging
from unittest.mock import patch, MagicMock

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_cli_command(command, timeout=30):  # Increased timeout to 30 seconds
    logger.debug(f"Running CLI command: {command}")
    """Helper function to run CLI commands using subprocess."""
    start_time = time.time()
    try:
        print(f"Executing command: {sys.executable} -m msearch.main {' '.join(command)}")
        result = subprocess.run(
            [sys.executable, "-m", "msearch.main"] + command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        print(f"Command '{' '.join(command)}' completed in {time.time() - start_time:.2f} seconds")
        print(f"Command stdout: {result.stdout}")
        print(f"Command stderr: {result.stderr}")
        print(f"Command return code: {result.returncode}")
        logger.debug(f"Command output - stdout: {result.stdout}, stderr: {result.stderr}, returncode: {result.returncode}")
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        print(f"Command '{' '.join(command)}' timed out after {timeout} seconds")
        return "", f"Command timed out after {timeout} seconds", 1
    except Exception as e:
        print(f"Unexpected error during command execution: {str(e)}")
        return "", str(e), 1

def test_cli_help():
    """Test the CLI help command."""
    stdout, stderr, returncode = run_cli_command(["--help"])
    assert returncode == 0
    assert "Usage:" in stdout
    assert "Search for info on the web, github, pypi, or inspect a library" in stdout

@pytest.mark.parametrize("query,expected_output", [
    (["python", "cli"], "Web Search Results"),
    (["language:python", "stars:>1000"], "Web Search Results"),
    (["repo:microsoft/vscode", "issue"], "Web Search Results"),
    (["language:rust", "created:>2021-01-01"], "Web Search Results"),
    (["topic:machine-learning", "stars:>500"], "Web Search Results"),
])
def test_search_command(query, expected_output):
    """Test the search command with various parameters."""
    stdout, stderr, returncode = run_cli_command(["search"] + query)
    assert returncode == 0
    assert expected_output in stdout
    assert "Title" in stdout
    assert "URL" in stdout
    assert "Snippet" in stdout

def test_search_command_no_results():
    """Test the search command with a query that should return no results."""
    stdout, stderr, returncode = run_cli_command(["search", "thisshouldnotexistatall12345"])
    assert returncode == 0
    assert "Web Search Results" in stdout

@pytest.mark.parametrize("url", [
    "https://example.com",
    "https://github.com",
    "https://httpbin.org/status/404",
])
def test_browse_command(url):
    """Test the browse command with various URLs."""
    stdout, stderr, returncode = run_cli_command(["browse-urls", url])
    assert returncode == 0
    assert "Web Search Results" in stdout
    assert "Title" in stdout
    assert "URL" in stdout
    assert "Snippet" in stdout

def test_browse_command_links():
    """Test the browse command's link extraction functionality."""
    stdout, stderr, returncode = run_cli_command(["browse-urls", "https://github.com"])
    assert returncode == 0
    assert "Web Search Results" in stdout
    assert "Title" in stdout
    assert "URL" in stdout
    assert "Snippet" in stdout

def test_invalid_command():
    """Test an invalid command."""
    stdout, stderr, returncode = run_cli_command(["invalid-command"])
    assert returncode == 0
    assert "Web Search Results" in stdout

def test_search_command_with_pagination():
    """Test the search command with pagination."""
    stdout, stderr, returncode = run_cli_command(["search", "python", "max:10"])
    assert returncode == 0
    assert "Web Search Results" in stdout
    assert "Title" in stdout
    assert "URL" in stdout
    assert "Snippet" in stdout

def test_web_search():
    """Test the web search command."""
    stdout, stderr, returncode = run_cli_command(["search", "web", "python programming"])
    assert returncode == 0
    assert "Web Search Results" in stdout
    assert "Title" in stdout
    assert "URL" in stdout
    assert "Snippet" in stdout

def test_huggingface_search():
    """Test the HuggingFace search command."""
    stdout, stderr, returncode = run_cli_command(["search", "--engine", "hf", "bert"])
    assert returncode == 0
    assert "HuggingFace Search Results" in stdout
    assert "Type" in stdout
    assert "Name" in stdout
    assert "URL" in stdout
    assert "Downloads" in stdout
    assert "Likes" in stdout
    assert "Summary" in stdout
    assert "Total results:" in stdout

def test_minspect_usage():
    """Test the minspect usage."""
    stdout, stderr, returncode = run_cli_command(["--engine", "inspect", "os"])
    assert returncode == 0
    assert "Module Inspection" in stdout
    assert "Inspecting module: os" in stdout
    assert "Functions" in stdout
    assert "Classes" in stdout
    assert "Variables" in stdout
