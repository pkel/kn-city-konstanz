dev: venv app/static/style.css
	flask run --debug # error messages & auto-reload on code change

venv: pyproject.toml
	python -m venv venv
	pip install --upgrade pip
	pip install -e .
	touch venv

clean:
	rm -rf venv
	rm -f app/static/style.css

app/static/style.css:
	wget https://raw.githubusercontent.com/andybrewer/mvp/v1.15/mvp.css -O $@
