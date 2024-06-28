dev: venv statics instance/app.sqlite
	venv/bin/flask run --debug # error messages & auto-reload on code change

venv: requirements.txt
	python -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install pip-tools
	venv/bin/pip install -r requirements.txt
	touch venv

.PHONY: update
update: venv
	venv/bin/pip-compile --strip-extras --quiet
	venv/bin/pip install -r requirements.txt
	touch venv

clean:
	rm -rf venv instance
	rm -f app/static/toastui*.css
	rm -f app/static/style.css
	rm -f app/static/toast.*.js
	rm -f app/static/toastui*.js
	rm -f app/static/tui*.js
	rm -f app/static/preact*.js

statics: app/static/style.css app/static/tui-time-picker.js app/static/tui-date-picker.js app/static/preact.min.js app/static/toastui-calendar.min.js app/static/toastui-calendar.min.css


instance/app.sqlite:
	mkdir -p instance
	venv/bin/flask init-db

app/static/style.css:
	wget https://raw.githubusercontent.com/andybrewer/mvp/v1.15/mvp.css -O $@

app/static/tui-time-picker.js:
	wget https://uicdn.toast.com/tui.time-picker/latest/tui-time-picker.js -O $@

app/static/tui-date-picker.js:
	wget https://uicdn.toast.com/tui.date-picker/latest/tui-date-picker.js -O $@

app/static/preact.min.js:
	wget https://cdnjs.cloudflare.com/ajax/libs/preact/10.22.0/preact.min.js -O $@

app/static/toastui-calendar.min.js:
	wget https://uicdn.toast.com/calendar/latest/toastui-calendar.min.js -O $@

app/static/toastui-calendar.min.css:
	wget https://uicdn.toast.com/calendar/latest/toastui-calendar.min.css -O $@

deploy:
	git remote rm tmp-deploy || true
	git remote add tmp-deploy dokku@dokku.sandbox.sgckn.pkel.dev:kn-city-logistik
	git push tmp-deploy main -f
	git remote rm tmp-deploy
