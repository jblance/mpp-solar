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
	#python3 -m build 
	poetry build
	ls -l dist/

pypi-upload:
	twine upload dist/*

docker-up:
	docker-compose up --build

docker-powermon-dev-up:
	docker-compose -f docker-compose.development.yaml up --build

m-build:
	docker-compose -f docker-compose.dev-min.yaml up --build 

m-run:
	docker-compose -f docker-compose.dev-min.yaml run mppsolar mpp-solar -p test -c QID -D
	# docker-compose -f docker-compose.dev-min.yaml run mppsolar -p test -c QID

