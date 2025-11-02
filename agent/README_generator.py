# README_generator.py
# Generate professional README content for deliverables submission

from typing import List, Dict, Optional
import os

class READMEGenerator:
    def __init__(self, student_name: str, university: str, department: str):
        self.student_name = student_name
        self.university = university
        self.department = department
    
    def generate_readme(self, 
                       deliverables: List[str],
                       repo_url: str,
                       how_to_run: Optional[str] = None,
                       contact_email: Optional[str] = None) -> str:
        """Generate a complete README.md content.
        
        Args:
            deliverables: List of deliverable items
            repo_url: GitHub repository URL
            how_to_run: Instructions for running the project
            contact_email: Contact email address
        
        Returns:
            Complete README content as markdown string
        """
        
        readme_content = f"""# AI Agent Prototype - Deliverables Pusher

**Student:** {self.student_name}  
**University:** {self.university}  
**Department:** {self.department}  

## Repository
{repo_url}

## Deliverables included
"""
        
        # Add deliverables list
        for deliverable in deliverables:
            readme_content += f"- {deliverable}\n"
        
        # Add how to run section
        if how_to_run:
            readme_content += f"\n## How to run\n{how_to_run}\n"
        else:
            readme_content += """\n## How to run (quick)
1. Create venv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r agent/requirements.txt
   ```

2. Run demo:
   ```bash
   python agent/planner.py --repo_path /path/to/repo
   ```
"""
        
        # Add contact section
        contact_info = contact_email if contact_email else "your.email@domain"
        readme_content += f"""\n## Contact
{self.student_name} — [{contact_info}](mailto:{contact_info})
"""
        
        return readme_content
    
    def validate_readme(self, readme_content: str) -> Dict[str, bool]:
        """Validate that README contains all required fields.
        
        Args:
            readme_content: The generated README content
        
        Returns:
            Dictionary with validation results for each field
        """
        validations = {
            "has_student_name": self.student_name in readme_content,
            "has_university": self.university in readme_content,
            "has_department": self.department in readme_content,
            "has_deliverables_section": "Deliverables" in readme_content,
            "has_how_to_run": "How to run" in readme_content,
            "has_contact": "Contact" in readme_content
        }
        return validations
    
    def save_readme(self, readme_content: str, repo_path: str) -> None:
        """Save README content to file.
        
        Args:
            readme_content: The generated README content
            repo_path: Path to repository root
        """
        readme_path = os.path.join(repo_path, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"✓ README.md saved to {readme_path}")

def generate_email_draft(student_name: str,
                        university: str,
                        department: str,
                        repo_url: str,
                        recipient_emails: List[str],
                        deliverables: List[str]) -> str:
    """Generate email draft for submission.
    
    Args:
        student_name: Student's name
        university: University name
        department: Department name
        repo_url: GitHub repository URL
        recipient_emails: List of recipient email addresses
        deliverables: List of deliverable items
    
    Returns:
        Email draft content
    """
    
    recipients_str = ", ".join(recipient_emails)
    deliverables_list = "\n".join([f"- {d}" for d in deliverables])
    
    email_content = f"""To: {recipients_str}
Subject: AI Agent Prototype - Deliverables submitted ({student_name})

Hello,

I have pushed all deliverables for the AI Agent Prototype assignment to the following GitHub repository:
{repo_url}

Student: {student_name}
University: {university}
Department: {department}

Deliverables:
{deliverables_list}

Please let me know if anything else is required.

Regards,
{student_name}
"""
    
    return email_content

if __name__ == "__main__":
    # Example usage
    generator = READMEGenerator(
        student_name="ADITYA",
        university="<Your University>",
        department="<Your Department>"
    )
    
    deliverables = [
        "Source code of the prototype (`/agent`)",
        "AI agent architecture document (`docs/architecture.md`)",
        "Data science report (`docs/report.pdf`)",
        "Interaction logs (`interaction_logs/`)",
        "Optional demo: `demo.mp4`"
    ]
    
    readme = generator.generate_readme(
        deliverables=deliverables,
        repo_url="https://github.com/adityadeshmukh23/deliverables-pusher"
    )
    
    print(readme)
    print("\n=== Validation ===")
    print(generator.validate_readme(readme))
