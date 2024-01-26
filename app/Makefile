.DEFAULT_GOAL := all

all:
	docker compose up --build
down:
	docker compose down
all-d:
	docker compose up --build -d
clean:
	docker volume rm app_app-db-volume