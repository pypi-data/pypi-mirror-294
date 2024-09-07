build-and-release:
	rm -rf dist
	$(shell command -v python3 || command -v python) -m venv env
	. env/bin/activate && pip install build twine
	. env/bin/activate && python -m build && python -m twine upload dist/*
