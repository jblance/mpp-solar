format: 
	flake8 setup.py mppsolar tests

mppsolar-tests: 
	python3 -m unittest discover -s tests/mppsolar -f -v
	
powermon-unit-tests: 
	python3 -m unittest discover -s tests/powermon/unit -f -v

powermon-integration-tests: 
	python3 -m unittest discover -s tests/powermon/integration -f -v

tests: powermon-unit-tests powermon-integration-tests mppsolar-tests


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
