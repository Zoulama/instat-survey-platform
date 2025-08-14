# Makefile for INSTAT Survey Platform

# Variables
COMPOSE_FILE = docker-compose.yml
APP_CONTAINER = app
DB_CONTAINER = db
DB_USER = postgres
DB_NAME = instat_surveys

# Default command
.DEFAULT_GOAL := help

.PHONY: help up down build logs test db-connect clean migrate migrate-new db-upgrade

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  up            - Start all services in detached mode"
	@echo "  down          - Stop and remove all services"
	@echo "  build         - Build or rebuild services"
	@echo "  logs          - View output from containers"
	@echo "  test          - Run tests against the database"
	@echo "  db-connect    - Connect to the PostgreSQL database"
	@echo "  clean         - Remove all Docker volumes and networks"
	@echo "  migrate       - Run database migrations"
	@echo "  migrate-new   - Create a new database migration script"
	@echo "  db-upgrade    - Apply the latest migration to the database"

up:
	@echo "Starting all services..."
	@docker compose -f $(COMPOSE_FILE) up -d

down:
	@echo "Stopping all services..."
	@docker compose -f $(COMPOSE_FILE) down

build:
	@echo "Building services..."
	@docker compose -f $(COMPOSE_FILE) build

logs:
	@echo "Showing logs..."
	@docker compose -f $(COMPOSE_FILE) logs -f

test:
	@echo "Running database tests..."
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) pytest

db-connect:
	@echo "Connecting to PostgreSQL database..."
	@docker compose -f $(COMPOSE_FILE) exec $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

clean:
	@echo "Cleaning up Docker environment..."
	@docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
	@docker volume prune -f
	@docker network prune -f

migrate:
	@echo "Running database migrations..."
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) alembic upgrade head

migrate-new:
	@echo "Creating new migration script..."
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) alembic revision --autogenerate -m "New migration"

db-upgrade:
	@echo "Applying latest migration..."
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) alembic upgrade head

