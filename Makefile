.PHONY: check lint format test testfast ready dumpinitialdata mypy docker-build docker-run docker-stop

check:
	python3 manage.py check

format:
	isort --atomic --skip-glob="venv/*" grunge
	black --exclude="venv/" grunge

lint:
	flake8 grunge
	black --check --exclude="venv/" grunge
	mypy grunge

test:
	python3 manage.py test

testfast:
	python3 manage.py test --failfast

ready: check lint testfast

mypy:
	mypy grunge

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

dumpinitialdata:
	python manage.py dumpdata --natural-foreign --natural-primary \
		--exclude=admin.logentry --all --indent=2 > grunge/fixtures/initial_data.json
