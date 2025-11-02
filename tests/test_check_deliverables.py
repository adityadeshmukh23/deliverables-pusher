# test_check_deliverables.py
# Automated tests to validate deliverables structure and README content

import os
import re
import pytest
from pathlib import Path

class TestDeliverablesStructure:
    """Test suite for validating deliverables structure."""
    
    def test_readme_exists(self):
        """Verify README.md exists in repository root."""
        assert os.path.exists("README.md"), "README.md file is missing"
    
    def test_agent_directory_exists(self):
        """Verify agent directory exists."""
        assert os.path.isdir("agent"), "agent/ directory is missing"
    
    def test_agent_files_exist(self):
        """Verify all required agent files exist."""
        required_files = [
            "agent/planner.py",
            "agent/executor.py",
            "agent/README_generator.py",
            "agent/requirements.txt"
        ]
        for file_path in required_files:
            assert os.path.exists(file_path), f"{file_path} is missing"
    
    def test_tests_directory_exists(self):
        """Verify tests directory exists."""
        assert os.path.isdir("tests"), "tests/ directory is missing"
    
    def test_docs_directory_exists(self):
        """Verify docs directory exists."""
        assert os.path.isdir("docs"), "docs/ directory is missing"
    
    def test_interaction_logs_directory_exists(self):
        """Verify interaction_logs directory exists."""
        assert os.path.isdir("interaction_logs"), "interaction_logs/ directory is missing"

class TestREADMEContent:
    """Test suite for validating README.md content."""
    
    @pytest.fixture
    def readme_content(self):
        """Load README.md content."""
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    
    def test_readme_has_title(self, readme_content):
        """Check if README has a title."""
        assert re.search(r"#.*[Aa]gent.*[Pp]rototype", readme_content), \
            "README missing title with 'Agent Prototype'"
    
    def test_readme_has_student_field(self, readme_content):
        """Check if README contains Student field."""
        assert re.search(r"\*\*Student:\*\*", readme_content, re.I), \
            "README missing Student field"
    
    def test_readme_has_university_field(self, readme_content):
        """Check if README contains University field."""
        assert re.search(r"\*\*University:\*\*", readme_content, re.I), \
            "README missing University field"
    
    def test_readme_has_department_field(self, readme_content):
        """Check if README contains Department field."""
        assert re.search(r"\*\*Department:\*\*", readme_content, re.I), \
            "README missing Department field"
    
    def test_readme_has_deliverables_section(self, readme_content):
        """Check if README contains Deliverables section."""
        assert re.search(r"##.*[Dd]eliverables", readme_content), \
            "README missing Deliverables section"
    
    def test_readme_has_how_to_run_section(self, readme_content):
        """Check if README contains How to run section."""
        assert re.search(r"##.*[Hh]ow to run", readme_content), \
            "README missing How to run section"
    
    def test_readme_has_contact_section(self, readme_content):
        """Check if README contains Contact section."""
        assert re.search(r"##.*[Cc]ontact", readme_content), \
            "README missing Contact section"

class TestCodeQuality:
    """Test suite for basic code quality checks."""
    
    def test_python_files_are_valid_syntax(self):
        """Check if all Python files have valid syntax."""
        python_files = [
            "agent/planner.py",
            "agent/executor.py",
            "agent/README_generator.py"
        ]
        
        for file_path in python_files:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
                    try:
                        compile(code, file_path, 'exec')
                    except SyntaxError as e:
                        pytest.fail(f"Syntax error in {file_path}: {e}")
    
    def test_requirements_file_is_valid(self):
        """Check if requirements.txt is properly formatted."""
        if os.path.exists("agent/requirements.txt"):
            with open("agent/requirements.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # Check basic package format
                        assert re.match(r"^[a-zA-Z0-9_-]+([><=!]+[0-9.]+)?$", line), \
                            f"Invalid requirement format: {line}"

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
