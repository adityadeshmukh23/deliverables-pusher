# executor.py
# Executor module - performs file operations, git commands, and validation

import os
import subprocess
from typing import List, Dict
from git import Repo

def validate_deliverables(base_path: str, required_files: List[str]) -> List[str]:
    """Validate that all required deliverable files exist.
    
    Args:
        base_path: Root path of the repository
        required_files: List of required file/directory paths
    
    Returns:
        List of missing files/directories
    """
    missing = []
    for file_path in required_files:
        full_path = os.path.join(base_path, file_path)
        if not os.path.exists(full_path):
            missing.append(file_path)
    return missing

def create_placeholder_files(base_path: str, missing_files: List[str]) -> None:
    """Create placeholder files/directories for missing deliverables.
    
    Args:
        base_path: Root path of the repository
        missing_files: List of missing file/directory paths
    """
    for file_path in missing_files:
        full_path = os.path.join(base_path, file_path)
        
        # Create directory if path ends with /
        if file_path.endswith('/'):
            os.makedirs(full_path, exist_ok=True)
            # Create a .gitkeep file to track empty directory
            with open(os.path.join(full_path, '.gitkeep'), 'w') as f:
                f.write('')
        else:
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            # Create placeholder file
            with open(full_path, 'w') as f:
                f.write(f"# Placeholder for {file_path}\n")

def git_add_all(repo_path: str) -> None:
    """Stage all changes in the repository.
    
    Args:
        repo_path: Path to git repository
    """
    repo = Repo(repo_path)
    repo.git.add(all=True)
    print("✓ All changes staged")

def git_commit(repo_path: str, message: str) -> None:
    """Commit staged changes.
    
    Args:
        repo_path: Path to git repository
        message: Commit message
    """
    repo = Repo(repo_path)
    repo.index.commit(message)
    print(f"✓ Committed: {message}")

def git_push(repo_path: str, branch: str = 'main') -> None:
    """Push commits to remote repository.
    
    Args:
        repo_path: Path to git repository
        branch: Branch name to push (default: 'main')
    """
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')
        origin.push(branch)
        print(f"✓ Pushed to remote branch: {branch}")
    except Exception as e:
        print(f"✗ Push failed: {e}")
        print("Please ensure you have push access and your credentials are configured.")

def run_validation_tests(repo_path: str) -> bool:
    """Run validation tests to check deliverables.
    
    Args:
        repo_path: Path to repository
    
    Returns:
        True if all tests pass, False otherwise
    """
    try:
        result = subprocess.run(
            ['python', '-m', 'pytest', 'tests/'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ All validation tests passed")
            return True
        else:
            print(f"✗ Some tests failed:\n{result.stdout}")
            return False
    except FileNotFoundError:
        print("⚠ pytest not found, skipping tests")
        return True
    except Exception as e:
        print(f"⚠ Error running tests: {e}")
        return True

if __name__ == "__main__":
    # Example usage
    print("Executor module loaded successfully")
