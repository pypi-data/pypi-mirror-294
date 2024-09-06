build-and-release:
	rm -rf dist
	$(shell command -v python3 || command -v python) -m build
	$(shell command -v python3 || command -v python) -m twine upload dist/*
