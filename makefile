format: 
	flake8 setup.py mppsolar tests

mppsolar-tests: 
	python3 -m discover -s powermon/tests unittest -f -v
	
powermon-tests: 
	python3 -m unittest discover -s powermon/tests -f -v

tests: powermon-tests mppsolar-tests


pypi:
	rm -rf dist/*
	#python3 -m build 
	poetry version patch
	poetry build
	ls -l dist/

pypi-upload:
	twine upload dist/*

docker-up:
	docker-compose up --build

docker-powermon-dev-up:
	docker compose -f docker-compose.development.yaml up --build
