.PHONY: bandit bandit-json bandit-all

bandit:
	@echo "Running Bandit (text report)..."
	@bandit -r . -c bandit.yaml -x venv,.venv,env,.env,tests,node_modules,interfaces -q -f txt -o bandit-report.txt
	@echo "bandit-report.txt generated."

bandit-json:
	@echo "Running Bandit (JSON report)..."
	@bandit -r . -c bandit.yaml -x venv,.venv,env,.env,tests,node_modules,interfaces -q -f json -o bandit-report.json
	@echo "bandit-report.json generated."

bandit-all: bandit bandit-json
	@echo "Bandit scans complete."
