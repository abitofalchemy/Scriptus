VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip


run: activate_venv
	$(PYTHON) app.py

activate_venv: requirements.txt
	python3 -m venv $(VENV) 
	$(PIP) install -r requirements.txt 


clean:
	rm -rf __pycache__
	rm -rf $(VENV)

.PHONY: run clean 
