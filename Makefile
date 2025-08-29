.PHONY: check lint format test testfast ready dumpinitialdata mypy docker-build docker-run docker-stop docker-test docker-test-fast

check:
	docker-compose exec web python manage.py check

format:
	docker-compose exec web isort --atomic --skip-glob="venv/*" rock_music_assignment
	docker-compose exec web black --exclude="venv/" rock_music_assignment

lint:
	docker-compose exec web flake8 rock_music_assignment
	docker-compose exec web black --check --exclude="venv/" rock_music_assignment
	docker-compose exec web mypy rock_music_assignment

test:
	docker-compose exec web python manage.py test

testfast:
	docker-compose exec web python manage.py test --failfast

pytest:
	docker-compose exec web pytest

pytest-fast:
	docker-compose exec web pytest --tb=short

pytest-cov:
	docker-compose exec web pytest --cov=rock_music_assignment --cov-report=html --cov-report=term

ready: check lint pytest-fast

mypy:
	docker-compose exec web mypy rock_music_assignment

docker-build:
	docker-compose build

start:
	docker-compose up -d

migrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

docker-stop:
	docker-compose down

docker-test:
	docker-compose exec web pytest

docker-test-fast:
	docker-compose exec web pytest --tb=short

docker-test-cov:
	docker-compose exec web pytest --cov=rock_music_assignment --cov-report=html --cov-report=term

dumpinitialdata:
	docker-compose exec web python manage.py dumpdata --natural-foreign --natural-primary \
		--exclude=admin.logentry --all --indent=2 > rock_music_assignment/fixtures/initial_data.json
