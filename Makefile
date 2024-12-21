.PHONY: run
run:
	python manage.py runserver

.PHONY: up-d
up-d:
	docker compose -f docker-compose.yml up -d

.PHONY: up
up:
	docker compose -f docker-compose.yml up

.PHONY: up-build
up-build:
	docker compose -f docker-compose.yml up --build

.PHONY: down
down:
	docker compose -f docker-compose.yml down

.PHONY: logs
logs:
	docker compose -f docker-compose.yml logs -f app

.PHONY: ps
ps:
	docker ps --format '{{ json .}}' | jq .


.PHONY: app-bash
app-bash:
	docker compose -f docker-compose.yml exec app bash