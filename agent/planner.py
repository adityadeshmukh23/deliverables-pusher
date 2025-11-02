# planner.py
# AI Agent Planner - generates high-level plan for deliverables submission

import os
import json
from typing import List, Dict

class DeliverablePlanner:
    def __init__(self, repo_path: str, required_files: List[str]):
        self.repo_path = repo_path
        self.required_files = required_files
        self.plan = []
    
    def analyze_deliverables(self) -> Dict:
        """Check which required files exist and which are missing."""
        missing = []
        existing = []
        
        for file in self.required_files:
            full_path = os.path.join(self.repo_path, file)
            if os.path.exists(full_path):
                existing.append(file)
            else:
                missing.append(file)
        
        return {"existing": existing, "missing": missing}
    
    def generate_plan(self) -> List[str]:
        """Generate step-by-step execution plan."""
        status = self.analyze_deliverables()
        
        self.plan = [
            "Check repository structure",
            f"Verify existing files: {', '.join(status['existing'])}",
        ]
        
        if status['missing']:
            self.plan.append(f"Create missing files/directories: {', '.join(status['missing'])}")
        
        self.plan.extend([
            "Generate README.md with student info and deliverables",
            "Run validation tests",
            "Commit all changes to git",
            "Push to GitHub repository",
            "Generate email draft for submission"
        ])
        
        return self.plan
    
    def display_plan(self):
        """Print the generated plan."""
        print("\n=== DELIVERABLES SUBMISSION PLAN ===")
        for i, step in enumerate(self.plan, 1):
            print(f"{i}. {step}")
        print("\n")

if __name__ == "__main__":
    # Example usage
    import argparse
    
    parser = argparse.ArgumentParser(description="Plan deliverables submission")
    parser.add_argument("--repo_path", required=True, help="Path to repository")
    args = parser.parse_args()
    
    required = [
        "README.md",
        "agent/executor.py",
        "agent/README_generator.py",
        "docs/architecture.md",
        "docs/report.pdf",
        "interaction_logs/"
    ]
    
    planner = DeliverablePlanner(args.repo_path, required)
    planner.generate_plan()
    planner.display_plan()
