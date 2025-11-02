#!/usr/bin/env python3
"""
Streamlit UI for Deliverables Pusher.
Collects user inputs and orchestrates planning and execution.
"""

import os
import json
import streamlit as st
from datetime import datetime

# Local imports (assumes same package)
from planner import DeliverablePlanner
from executor import Executor

st.set_page_config(page_title="Deliverables Pusher", page_icon="📦", layout="wide")

st.title("📦 Deliverables Pusher & Notifier")
st.write("Plan, validate, push to GitHub, and draft the submission email.")

with st.sidebar:
    st.header("Student Info")
    student_name = st.text_input("Name", value=os.environ.get("STUDENT_NAME", ""))
    university = st.text_input("University", value=os.environ.get("UNIVERSITY", ""))
    department = st.text_input("Department", value=os.environ.get("DEPARTMENT", ""))

    st.header("Repository")
    repo_path = st.text_input("Local repo path", value=os.getcwd())
    repo_url = st.text_input("GitHub repo URL", value="")

    st.header("Options")
    create_placeholders = st.checkbox("Create placeholders for missing files", value=True)
    run_tests_opt = st.checkbox("Run tests after generation", value=False)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1) Plan")
    if st.button("Generate Plan", type="primary"):
        planner = DeliverablePlanner(interaction_logs_path=os.path.join(repo_path, "interaction_logs"))
        student_info = {
            "name": student_name,
            "university": university,
            "department": department,
            "repo_url": repo_url,
        }
        plan = planner.create_execution_plan(repo_path, student_info)
        if plan is None:
            st.error("Failed to create plan. Please check inputs.")
        else:
            st.success("Plan created.")
            st.session_state["plan"] = plan.__dict__
            st.code(json.dumps(plan.__dict__, indent=2))

with col2:
    st.subheader("2) Execute")
    if st.button("Execute Plan", disabled="plan" not in st.session_state):
        plan_dict = st.session_state.get("plan")
        if plan_dict:
            # Optionally remove run_tests or create_missing_files actions
            if not run_tests_opt:
                plan_dict["actions"] = [a for a in plan_dict["actions"] if a.get("type") != "run_tests"]
            if not create_placeholders:
                plan_dict["actions"] = [a for a in plan_dict["actions"] if a.get("type") != "create_missing_files"]

            ex = Executor(repo_path, logs_path=os.path.join(repo_path, "interaction_logs"))
            results = ex.execute_plan(plan_dict)
            st.session_state["results"] = {k: v.__dict__ for k, v in results.items()}
            st.success("Execution complete.")
            st.code(json.dumps(st.session_state["results"], indent=2))

st.subheader("3) README Generator")
st.caption("Use your fine-tuned model or a template-first generator in agent/README_generator.py.")
st.write("This UI assumes README generation is delegated to the generator script, which should be called by an action or via a separate button.")

st.subheader("Notes")
st.markdown("- Keep tokens and secrets out of the repo.\n- Use CI to run tests on push.\n- Save interaction logs for reproducibility.")
