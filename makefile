mppsolar-integration-tests: 
	python3 -m unittest discover -s tests/integration -f -v

mppsolar-unit-tests: 
	python3 -m unittest discover -s tests/unit -f -v
	
test:
	python3 -m unittest discover -s tests -f

tests: mppsolar-unit-tests mppsolar-integration-tests

pypi:
	rm -rf dist/*
	#python3 -m build 
	./make_version.sh
	poetry build
	poetry version patch
	./make_version_dev.sh
	ls -l dist/
	cat mppsolar/version.py

pypi-upload:
	twine upload dist/*

docker-up:
	docker-compose up --build


git-tag-release:
	@./make_version.sh
	@echo Creating a tag for version: `awk '/^version/ {print $$3}' pyproject.toml`
	@echo Pushing version changes to git
	git add mppsolar/version.py
	git commit -m "remove -dev from version"
	git push
	@git tag `awk '/^version/ {print substr($$3, 2, length($$3)-2)}' pyproject.toml`
	@git push origin --tags
	@echo "Now go to github and create a release for the latest tag" `awk '/^version/ {print substr($$3, 2, length($$3)-2)}' pyproject.toml`
	@echo Bumping version..
	@poetry version patch
	@echo Adding '-dev' to version in git
	@./make_version_dev.sh
	@echo Pushing version changes to git
	git add mppsolar/version.py pyproject.toml
	git commit -m "Update versions"
	git push
