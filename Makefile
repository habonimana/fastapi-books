install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv books-api/main.py

format:
	black *.py

lint:
	pylint --disable=R,C books-api/main.py

all: install lint test