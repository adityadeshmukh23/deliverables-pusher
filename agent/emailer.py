#!/usr/bin/env python3
"""
emailr.py
Create a local email draft file (email_draft.txt) that you can copy-paste into your mail client.
This script intentionally does NOT send emails (avoids storing creds).
"""
import os

DEFAULT_TO = [
    "yasuhironose@imbesideyou.world",
    "sanskarnanegaonkar@imbesideyou.world",
    "mamindla@imbesideyou.world",
    "Animeshmishra@imbesideyou.world"
]

def build_email(student_name, university, department, repo_url, to_list=None):
    if to_list is None:
        to_list = DEFAULT_TO
    subject = f"AI Agent Prototype - Deliverables submitted ({student_name})"
    body = f"""Hello,

I have pushed all deliverables for the AI Agent Prototype assignment to the following GitHub repository:
{repo_url}

Student: {student_name}
University: {university}
Department: {department}

Deliverables included:
- Source code (agent/)
- Agent architecture document (docs/architecture.md)
- Data science report (docs/report.pdf)
- Interaction logs (interaction_logs/)
- Demo / screenshots (optional)

Kindly confirm receipt.

Regards,
{student_name}
"""
    return {"to": to_list, "subject": subject, "body": body}

def save_draft(path, email):
    with open(path, "w") as f:
        f.write("To: " + ", ".join(email["to"]) + "\n")
        f.write("Subject: " + email["subject"] + "\n\n")
        f.write(email["body"])
    print("Email draft saved at", path)

if __name__ == "__main__":
    import argparse, os
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo_path", required=True)
    ap.add_argument("--name", default="ADITYA")
    ap.add_argument("--university", default="IIT Kanpur")
    ap.add_argument("--department", default="MSE")
    ap.add_argument("--repo_url", default="https://github.com/adityadeshmukh23/deliverables-pusher")
    args = ap.parse_args()
    draft_path = os.path.join(args.repo_path, "email_draft.txt")
    email = build_email(args.name, args.university, args.department, args.repo_url)
    save_draft(draft_path, email)
