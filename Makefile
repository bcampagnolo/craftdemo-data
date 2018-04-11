all: run

clean:
	rm -rf venv && rm -rf *.egg-info && rm -rf dist && rm -rf *.log*

venv:
	virtualenv --python=python3 venv && venv/bin/python setup.py develop

run: venv
	FLASK_APP=indecision INDECISION_SETTINGS=../settings.cfg venv/bin/flask run

test: venv
	INDECISION_SETTINGS=../settings.cfg venv/bin/python -m unittest discover -s tests

sdist: venv req
	venv/bin/python setup.py sdist --formats=zip

req:
	venv/bin/python -m pip install -r requirements.txt