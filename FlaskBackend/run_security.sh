#!/usr/bin/env bash
set -euo pipefail

# Run Bandit security scans for the Flask backend
# Generates:
#  - bandit-report.txt (human readable)
#  - bandit-report.json (machine readable for CI)
#
# Usage:
#   bash run_security.sh
#   or make it executable and run: ./run_security.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "${ROOT_DIR}"

echo "Running Bandit scan (text)..."
bandit -r . -c bandit.yaml -x venv,.venv,env,.env,tests,node_modules,interfaces \
  -q -f txt -o bandit-report.txt

echo "Running Bandit scan (JSON)..."
bandit -r . -c bandit.yaml -x venv,.venv,env,.env,tests,node_modules,interfaces \
  -q -f json -o bandit-report.json

echo "Bandit scan complete."
echo "Reports generated:"
echo " - ${ROOT_DIR}/bandit-report.txt"
echo " - ${ROOT_DIR}/bandit-report.json"
