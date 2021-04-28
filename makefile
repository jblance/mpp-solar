format: 
	flake8 setup.py mppsolar tests

test: tests/*.py
	python3 -m unittest -v
