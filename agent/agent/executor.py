#!/usr/bin/env python3
"""
Executor component for the Deliverables Pusher agent.
Runs concrete actions: file creation, validations, tests, git commit/push, and email draft.
"""

import os
import re
import json
import subprocess
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

try:
    from git import Repo
except ImportError:
    Repo = None  # Optional dependency; recommend installing GitPython


@dataclass
class ExecutionResult:
    success: bool
    message: str
    details: Optional[Dict[str, Any]] = None


class Executor:
    def __init__(self, repo_path: str, logs_path: str = "interaction_logs/"):
        self.repo_path = os.path.abspath(repo_path)
        self.logs_path = logs_path
        os.makedirs(self.logs_path, exist_ok=True)

    # ---------- Filesystem helpers ----------
    def ensure_path(self, relative_path: str, is_dir: bool = False) -> None:
        path = os.path.join(self.repo_path, relative_path)
        if is_dir or relative_path.endswith("/"):
            os.makedirs(path, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write("")

    def create_placeholders(self, files: List[str]) -> ExecutionResult:
        created = []
        for f in files:
            try:
                self.ensure_path(f, is_dir=f.endswith("/"))
                created.append(f)
            except Exception as e:
                return ExecutionResult(False, f"Failed creating {f}: {e}")
        return ExecutionResult(True, "Placeholders ensured", {"created": created})

    # ---------- Validations ----------
    def validate_required(self, required_files: List[str]) -> ExecutionResult:
        missing = []
        for f in required_files:
            if not os.path.exists(os.path.join(self.repo_path, f.rstrip("/"))):
                missing.append(f)
        return ExecutionResult(len(missing) == 0, "Validation complete", {"missing": missing})

    def assert_readme_fields(self, readme_path: str = "README.md") -> ExecutionResult:
        path = os.path.join(self.repo_path, readme_path)
        if not os.path.exists(path):
            return ExecutionResult(False, "README not found")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        required_patterns = [
            r"(?i)Title|^# ",
            r"(?i)Student|Name",
            r"(?i)University",
            r"(?i)Department",
            r"(?i)Deliverables",
            r"(?i)How to run|Installation",
            r"(?i)Contact",
        ]
        missing = [p for p in required_patterns if not re.search(p, content)]
        return ExecutionResult(len(missing) == 0, "README fields check", {"missing_patterns": missing})

    # ---------- Tests ----------
    def run_tests(self, test_path: str = "tests") -> ExecutionResult:
        if not os.path.exists(os.path.join(self.repo_path, test_path)):
            return ExecutionResult(True, "No tests directory found; skipping")
        try:
            result = subprocess.run(
                ["python", "-m", "pytest", "-q"],
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=600,
            )
            success = result.returncode == 0
            return ExecutionResult(success, "Tests executed", {"output": result.stdout})
        except Exception as e:
            return ExecutionResult(False, f"Test run failed: {e}")

    # ---------- Git operations ----------
    def git_commit(self, message: str = "Auto: push deliverables") -> ExecutionResult:
        try:
            if Repo is None:
                # fallback to CLI git
                subprocess.run(["git", "add", "-A"], cwd=self.repo_path, check=True)
                subprocess.run(["git", "commit", "-m", message], cwd=self.repo_path, check=True)
            else:
                repo = Repo(self.repo_path)
                repo.git.add(all=True)
                # Only commit if there is something to commit
                if repo.is_dirty(untracked_files=True):
                    repo.index.commit(message)
            return ExecutionResult(True, "Git commit complete")
        except subprocess.CalledProcessError as e:
            return ExecutionResult(False, f"Git CLI commit failed: {e}")
        except Exception as e:
            return ExecutionResult(False, f"GitPython commit failed: {e}")

    def git_push(self, branch: str = "main") -> ExecutionResult:
        try:
            if Repo is None:
                subprocess.run(["git", "push", "origin", branch], cwd=self.repo_path, check=True)
            else:
                repo = Repo(self.repo_path)
                origin = repo.remote(name="origin")
                origin.push(branch)
            return ExecutionResult(True, "Git push complete")
        except subprocess.CalledProcessError as e:
            return ExecutionResult(False, f"Git CLI push failed: {e}")
        except Exception as e:
            return ExecutionResult(False, f"GitPython push failed: {e}")

    # ---------- Email draft ----------
    def create_email_draft(
        self,
        student_name: str,
        university: str,
        department: str,
        repo_url: str,
        recipients: Optional[List[str]] = None,
        subject_prefix: str = "AI Agent Prototype - Deliverables submitted",
        out_path: str = "email_draft.txt",
    ) -> ExecutionResult:
        recipients = recipients or []
        lines = [
            f"Subject: {subject_prefix} ({student_name})",
            "",
            "Hello,",
            "",
            "I have pushed all deliverables for the AI Agent Prototype assignment to the following GitHub repository:",
            repo_url,
            "",
            f"Student: {student_name}",
            f"University: {university}",
            f"Department: {department}",
            "",
            "Deliverables included:",
            "- Source code",
            "- Agent architecture document",
            "- Data science report (fine-tuning details & evaluation)",
            "- Interaction logs",
            "- Optional: demo video/screenshots",
            "",
            "Please let me know if you need any additional information.",
            "",
            f"Regards,\n{student_name}",
            "",
            f"To: {', '.join(recipients)}" if recipients else "",
        ]
        draft_content = "\n".join([l for l in lines if l is not None])
        path = os.path.join(self.repo_path, out_path)
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(draft_content)
            return ExecutionResult(True, "Email draft created", {"path": path})
        except Exception as e:
            return ExecutionResult(False, f"Failed to create email draft: {e}")

    # ---------- Orchestration ----------
    def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, ExecutionResult]:
        results: Dict[str, ExecutionResult] = {}
        for i, action in enumerate(plan.get("actions", []), 1):
            a_type = action.get("type")
            key = f"{i:02d}_{a_type}"
            if a_type == "create_missing_files":
                results[key] = self.create_placeholders(action.get("files", []))
            elif a_type == "generate_readme":
                # Placeholder: README generation handled by README_generator
                results[key] = ExecutionResult(True, "README generation delegated")
            elif a_type == "run_tests":
                results[key] = self.run_tests()
            elif a_type == "git_commit":
                results[key] = self.git_commit()
            elif a_type == "git_push":
                results[key] = self.git_push()
            elif a_type == "generate_email":
                params = action.get("parameters", {})
                results[key] = self.create_email_draft(
                    student_name=plan.get("student_name", ""),
                    university=plan.get("university", ""),
                    department=plan.get("department", ""),
                    repo_url=plan.get("repo_url", ""),
                    recipients=params.get("recipients", []),
                )
            else:
                results[key] = ExecutionResult(False, f"Unknown action: {a_type}")
        return results


# CLI for manual execution
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Execute deliverables plan")
    parser.add_argument("--repo_path", required=True)
    parser.add_argument("--plan_path", required=True, help="Path to JSON plan file")

    args = parser.parse_args()

    with open(args.plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    ex = Executor(args.repo_path)
    results = ex.execute_plan(plan)

    # Save results
    out = os.path.join(args.repo_path, "interaction_logs", f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({k: v.__dict__ for k, v in results.items()}, f, indent=2)

    print("Execution complete. Results saved to:", out)
