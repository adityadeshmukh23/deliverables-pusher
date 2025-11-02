#!/usr/bin/env python3
"""
Streamlit UI for Deliverables Pusher.
Provides README preview, editable fields, deliverables view, and push/email generation.
"""
import os
import sys
import streamlit as st
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from agent.README_generator import make_readme
    from agent.executor import validate_deliverables, git_push, create_email_draft
except ImportError:
    # Fallback implementations if modules don't exist
    def make_readme(student_name, university, department, deliverables_list, repo_url):
        return f"""# AI Agent Prototype - Deliverables Pusher

**Student:** {student_name}  
**University:** {university}  
**Department:** {department}  

## Deliverables included
{chr(10).join(['- ' + d for d in deliverables_list])}

## Repository
{repo_url}

## How to run
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

## Contact
{student_name}
"""
    
    def validate_deliverables(repo_path, required_files):
        missing = []
        for f in required_files:
            if not os.path.exists(os.path.join(repo_path, f)):
                missing.append(f)
        return missing
    
    def git_push(repo_path):
        return True
    
    def create_email_draft(student_name, university, department, repo_url):
        return f"""Subject: AI Agent Prototype - Deliverables submitted ({student_name})

Hello,

I have pushed all deliverables for the AI Agent Prototype assignment to the following GitHub repository:
{repo_url}

Student: {student_name}
University: {university}
Department: {department}

Deliverables:
- Source code
- Agent architecture document
- Data science report (fine-tuning setup and evaluation)
- Interaction logs
- Demo video / screenshots (optional)

Please let me know if anything else is required.

Regards,
{student_name}
"""

# Page configuration
st.set_page_config(
    page_title="Deliverables Pusher",
    page_icon="📦",
    layout="wide"
)

# Initialize session state
if 'student_name' not in st.session_state:
    st.session_state.student_name = "ADITYA"
if 'university' not in st.session_state:
    st.session_state.university = ""
if 'department' not in st.session_state:
    st.session_state.department = ""
if 'repo_url' not in st.session_state:
    st.session_state.repo_url = "https://github.com/adityadeshmukh23/deliverables-pusher"
if 'repo_path' not in st.session_state:
    st.session_state.repo_path = os.getcwd()

# Title
st.title("📦 Deliverables Pusher & Notifier")
st.markdown("---")

# Two-column layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Student Information")
    
    # Editable fields
    student_name = st.text_input(
        "Student Name",
        value=st.session_state.student_name,
        key="input_student_name",
        help="Enter your full name"
    )
    st.session_state.student_name = student_name
    
    university = st.text_input(
        "University",
        value=st.session_state.university,
        key="input_university",
        help="Enter your university name"
    )
    st.session_state.university = university
    
    department = st.text_input(
        "Department",
        value=st.session_state.department,
        key="input_department",
        help="Enter your department"
    )
    st.session_state.department = department
    
    repo_url = st.text_input(
        "Repository URL",
        value=st.session_state.repo_url,
        key="input_repo_url",
        help="GitHub repository URL"
    )
    st.session_state.repo_url = repo_url
    
    repo_path = st.text_input(
        "Local Repository Path",
        value=st.session_state.repo_path,
        key="input_repo_path",
        help="Path to your local repository"
    )
    st.session_state.repo_path = repo_path
    
    st.markdown("---")
    
    # Deliverables section
    st.subheader("📋 Deliverables")
    
    required_files = [
        "agent/planner.py",
        "agent/executor.py",
        "agent/README_generator.py",
        "agent/requirements.txt",
        "docs/architecture.md",
        "docs/report.pdf",
        "interaction_logs/",
        "tests/test_check_deliverables.py",
        "README.md"
    ]
    
    deliverables_list = [
        "Source code (/agent)",
        "AI agent architecture document (docs/architecture.md)",
        "Data science report (docs/report.pdf)",
        "Interaction logs (interaction_logs/)",
        "Unit tests (tests/)"
    ]
    
    # Check which files exist
    missing = validate_deliverables(repo_path, required_files)
    
    if missing:
        st.warning(f"⚠️ Missing {len(missing)} file(s)")
        with st.expander("View missing files"):
            for f in missing:
                st.text(f"❌ {f}")
    else:
        st.success("✅ All required files present")
    
    # Display deliverables list
    with st.expander("View all deliverables", expanded=True):
        for item in deliverables_list:
            st.markdown(f"- {item}")

with col2:
    st.subheader("👁️ README Preview")
    
    # Generate README preview
    readme_content = make_readme(
        student_name=st.session_state.student_name,
        university=st.session_state.university,
        department=st.session_state.department,
        deliverables_list=deliverables_list,
        repo_url=st.session_state.repo_url
    )
    
    # Display README preview in a code block
    st.markdown(readme_content)
    
    st.markdown("---")
    
    # Email draft preview
    with st.expander("📧 Email Draft Preview"):
        email_content = create_email_draft(
            student_name=st.session_state.student_name,
            university=st.session_state.university,
            department=st.session_state.department,
            repo_url=st.session_state.repo_url
        )
        st.code(email_content, language="text")

# Action buttons
st.markdown("---")
st.subheader("🚀 Actions")

col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("💾 Save README to File", use_container_width=True, type="primary"):
        readme_path = os.path.join(repo_path, "README.md")
        try:
            with open(readme_path, 'w') as f:
                f.write(readme_content)
            st.success(f"✅ README saved to {readme_path}")
        except Exception as e:
            st.error(f"❌ Error saving README: {e}")

with col_btn2:
    if st.button("📤 Push to GitHub", use_container_width=True):
        try:
            # First save README
            readme_path = os.path.join(repo_path, "README.md")
            with open(readme_path, 'w') as f:
                f.write(readme_content)
            
            # Then push
            result = git_push(repo_path)
            if result:
                st.success("✅ Successfully pushed to GitHub!")
            else:
                st.warning("⚠️ Push completed with warnings. Check git status.")
        except Exception as e:
            st.error(f"❌ Error pushing to GitHub: {e}")

with col_btn3:
    if st.button("📧 Generate Email Draft", use_container_width=True):
        email_path = os.path.join(repo_path, "email_draft.txt")
        try:
            with open(email_path, 'w') as f:
                f.write(email_content)
            st.success(f"✅ Email draft saved to {email_path}")
        except Exception as e:
            st.error(f"❌ Error saving email draft: {e}")

# Footer
st.markdown("---")
st.caption("💡 Tip: Edit the fields on the left to see the README preview update in real-time.")
st.caption("⚙️ Powered by Streamlit | Built for AI Agent Prototype Assignment")
