#!/usr/bin/env bash
set -e
REPO_PATH="$(pwd)"

echo "=== Running Deliverables Demo ==="

# 1. Generate README
python agent/README_generator.py --repo_path "$REPO_PATH" \
  --name "ADITYA" \
  --university "IIT Kanpur" \
  --department "MSE" \
  --repo_url "https://github.com/adityadeshmukh23/deliverables-pusher"

# 2. Ensure required directories exist
mkdir -p docs interaction_logs agent tests

# 3. Create placeholder files if missing
touch docs/architecture.md docs/report.pdf

# 4. Generate email draft
python agent/emailer.py --repo_path "$REPO_PATH" \
  --name "ADITYA" \
  --university "IIT Kanpur" \
  --department "MSE" \
  --repo_url "https://github.com/adityadeshmukh23/deliverables-pusher"

# 5. Validate deliverables
python - <<PY
from agent.executor import validate_deliverables, create_placeholder
base = "$REPO_PATH"
req = ["agent/", "docs/architecture.md", "docs/report.pdf", "interaction_logs/"]
missing = validate_deliverables(base, req)
print("Missing before:", missing)
for m in missing:
    create_placeholder(base, m)
print("Validation done.")
PY

echo "=== Demo complete ==="
echo "README.md and email_draft.txt generated successfully!"
