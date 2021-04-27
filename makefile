format: 
	flake8 setup.py mppsolar tests

test: tests/*.py
	python -m unittest
