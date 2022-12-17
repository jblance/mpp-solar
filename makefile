format: 
	flake8 setup.py mppsolar tests

test: tests/*.py
	# python3 -m unittest -v
	coverage run -m unittest
	coverage report -m
	coverage html

t: tests/*.py
	python3 -m unittest 

pypi:
	rm -rf dist/*
	python3 -m build 
	ls -l dist/

pypi-upload:
	twine upload dist/*
