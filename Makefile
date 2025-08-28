.PHONY: check lint format test testfast ready dumpinitialdata mypy docker-build docker-run docker-stop

check:
	python3 manage.py check

format:
	isort --atomic --skip-glob="venv/*" rock_music_assignment
	black --exclude="venv/" rock_music_assignment

lint:
	flake8 rock_music_assignment
	black --check --exclude="venv/" rock_music_assignment
	mypy rock_music_assignment

test:
	python3 manage.py test

testfast:
	python3 manage.py test --failfast

ready: check lint testfast

mypy:
	mypy rock_music_assignment

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

dumpinitialdata:
	python manage.py dumpdata --natural-foreign --natural-primary \
		--exclude=admin.logentry --all --indent=2 > rock_music_assignment/fixtures/initial_data.json
