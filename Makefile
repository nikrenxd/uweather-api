.PHONY: run
run:
	python manage.py runserver

.PHONY: up
up:
	docker compose -f docker-compose.yml up -d

.PHONY: down
down:
	docker compose -f docker-compose.yml down

.PHONY: logs
logs:
	docker compose -f docker-compose.yml logs -f app

.PHONY: app-bash
app-bash:
	docker compose -f docker-compose.yml exec app bash