serve: venv
	flask run --debug # auto-reload on code change

venv: pyproject.toml
	python -m venv venv
	pip install --upgrade pip
	pip install -e .
