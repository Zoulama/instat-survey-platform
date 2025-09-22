# =====================================================================
# INSTAT Survey Platform - Enhanced Makefile
# Complete development and deployment automation
# =====================================================================

# Variables
COMPOSE_FILE = docker-compose.yml
APP_CONTAINER = app
DB_CONTAINER = db
REDIS_CONTAINER = redis
DB_USER = postgres
DB_NAME = instat_surveys
BACKUP_DIR = backups
DATE = $(shell date +%Y%m%d_%H%M%S)

# Colors for output
COLOR_BLUE = \033[0;34m
COLOR_GREEN = \033[0;32m
COLOR_YELLOW = \033[1;33m
COLOR_RED = \033[0;31m
COLOR_NC = \033[0m # No Color

# Default command
.DEFAULT_GOAL := help

.PHONY: help deploy deploy-fresh deploy-update deploy-verify setup-dirs setup-env \
        up down build rebuild logs logs-app logs-db logs-redis test health \
        db-connect db-setup db-migrate db-populate db-verify db-backup db-restore \
        clean clean-all auth-test mali-data-test template-test \
        migrate migrate-new db-upgrade audit-logs parsing-stats \
        dev-setup dev-run dev-test format lint security-scan

help:
	@echo "$(COLOR_BLUE)==============================================$(COLOR_NC)"
	@echo "$(COLOR_BLUE)INSTAT Survey Platform - Makefile Commands$(COLOR_NC)"
	@echo "$(COLOR_BLUE)==============================================$(COLOR_NC)"
	@echo ""
	@echo "$(COLOR_GREEN)🚀 DEPLOYMENT COMMANDS:$(COLOR_NC)"
	@echo "  deploy        - Complete deployment with database setup"
	@echo "  deploy-fresh  - Fresh deployment (removes old containers/volumes)"
	@echo "  deploy-update - Update existing deployment"
	@echo "  deploy-verify - Verify current deployment"
	@echo ""
	@echo "$(COLOR_GREEN)🐳 DOCKER COMMANDS:$(COLOR_NC)"
	@echo "  up            - Start all services in detached mode"
	@echo "  down          - Stop and remove all services"
	@echo "  build         - Build or rebuild services"
	@echo "  rebuild       - Force rebuild without cache"
	@echo "  logs          - View output from all containers"
	@echo "  logs-app      - View application logs"
	@echo "  logs-db       - View database logs"
	@echo "  logs-redis    - View Redis logs"
	@echo ""
	@echo "$(COLOR_GREEN)🗄️ DATABASE COMMANDS:$(COLOR_NC)"
	@echo "  db-setup      - Complete database setup (migration + data)"
	@echo "  db-migrate    - Run complete database migration"
	@echo "  db-populate   - Populate Mali reference data"
	@echo "  db-verify     - Verify database setup and data"
	@echo "  db-connect    - Connect to PostgreSQL database"
	@echo "  db-backup     - Create database backup"
	@echo "  db-restore    - Restore database from backup"
	@echo ""
	@echo "$(COLOR_GREEN)🔐 SECURITY & AUTH COMMANDS:$(COLOR_NC)"
	@echo "  auth-test     - Test OAuth2 authentication system"
	@echo "  audit-logs    - View recent audit logs"
	@echo "  parsing-stats - View parsing statistics"
	@echo ""
	@echo "$(COLOR_GREEN)🧪 TESTING COMMANDS:$(COLOR_NC)"
	@echo "  test          - Run application tests"
	@echo "  health        - Check service health"
	@echo "  mali-data-test - Test Mali reference data endpoints"
	@echo "  template-test - Test template endpoints"
	@echo ""
	@echo "$(COLOR_GREEN)🛠️ DEVELOPMENT COMMANDS:$(COLOR_NC)"
	@echo "  dev-setup     - Setup development environment"
	@echo "  dev-run       - Run in development mode"
	@echo "  dev-test      - Run development tests"
	@echo "  format        - Format code with black"
	@echo "  lint          - Run linting checks"
	@echo "  security-scan - Run security vulnerability scan"
	@echo ""
	@echo "$(COLOR_GREEN)🧹 CLEANUP COMMANDS:$(COLOR_NC)"
	@echo "  clean         - Clean up Docker environment"
	@echo "  clean-all     - Complete cleanup (containers, volumes, images)"
	@echo ""
	@echo "$(COLOR_GREEN)📋 LEGACY COMMANDS:$(COLOR_NC)"
	@echo "  migrate       - Legacy Alembic migrations (use db-setup instead)"
	@echo "  migrate-new   - Create new Alembic migration"
	@echo "  db-upgrade    - Apply Alembic migrations (use db-setup instead)"

# =====================================================================
# Deployment Commands
# =====================================================================

deploy: setup-dirs setup-env up db-setup
	@echo "$(COLOR_GREEN)✅ Deployment complete!$(COLOR_NC)"
	deploy-verify

deploy-fresh: clean-all setup-dirs setup-env build up db-setup
	@echo "$(COLOR_GREEN)✅ Fresh deployment complete!$(COLOR_NC)"
	deploy-verify

deploy-update: down build up
	@echo "$(COLOR_GREEN)✅ Deployment updated!$(COLOR_NC)"
	deploy-verify

deploy-verify: health mali-data-test template-test
	@echo "$(COLOR_GREEN)✅ Deployment verification complete!$(COLOR_NC)"

setup-dirs:
	@echo "$(COLOR_BLUE)Setting up directories...$(COLOR_NC)"
	mkdir -p $(BACKUP_DIR)

# Create .env file if it doesn't exist
setup-env:
	@echo "$(COLOR_BLUE)Checking environment configuration...$(COLOR_NC)"
	if [ ! -f .env ]; then \
		echo "$(COLOR_YELLOW)Creating default .env file...$(COLOR_NC)"; \
		echo "POSTGRES_USER=$(DB_USER)" > .env; \
		echo "POSTGRES_PASSWORD=instat_password" >> .env; \
		echo "POSTGRES_DB=$(DB_NAME)" >> .env; \
		echo "SECRET_KEY=development_secret_key" >> .env; \
		echo "$(COLOR_YELLOW)Created default .env file. Please update with secure values for production.$(COLOR_NC)"; \
	else \
		echo "$(COLOR_BLUE).env file already exists$(COLOR_NC)"; \
	fi

# =====================================================================
# Docker Commands
# =====================================================================

up:
	@echo "$(COLOR_BLUE)Starting all services...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) up -d

down:
	@echo "$(COLOR_BLUE)Stopping all services...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) down

build:
	@echo "$(COLOR_BLUE)Building services...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) build

rebuild:
	@echo "$(COLOR_BLUE)Force rebuilding services without cache...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) build --no-cache

logs:
	@echo "$(COLOR_BLUE)Showing all logs...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) logs -f

logs-app:
	@echo "$(COLOR_BLUE)Showing application logs...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) logs -f $(APP_CONTAINER)

logs-db:
	@echo "$(COLOR_BLUE)Showing database logs...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) logs -f $(DB_CONTAINER)

logs-redis:
	@echo "$(COLOR_BLUE)Showing Redis logs...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) logs -f $(REDIS_CONTAINER)

# =====================================================================
# Database Commands
# =====================================================================

db-setup: db-migrate db-populate
	@echo "$(COLOR_GREEN)✅ Database setup complete!$(COLOR_NC)"

# Run database migrations
db-migrate:
	@echo "$(COLOR_BLUE)Running database migrations...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) alembic upgrade head

# Populate Mali reference data
db-populate:
	@echo "$(COLOR_BLUE)Populating Mali reference data...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) python -m scripts.populate_mali_reference_data

# Verify database setup
db-verify:
	@echo "$(COLOR_BLUE)Verifying database setup...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) python -m scripts.verify_database

# Connect to database
db-connect:
	@echo "$(COLOR_BLUE)Connecting to PostgreSQL database...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

# Create database backup
db-backup:
	@echo "$(COLOR_BLUE)Creating database backup...$(COLOR_NC)"
	@mkdir -p $(BACKUP_DIR)
	@docker compose -f $(COMPOSE_FILE) exec -T $(DB_CONTAINER) pg_dump -U $(DB_USER) $(DB_NAME) > $(BACKUP_DIR)/$(DB_NAME)_$(DATE).sql
	@echo "$(COLOR_GREEN)✅ Backup created: $(BACKUP_DIR)/$(DB_NAME)_$(DATE).sql$(COLOR_NC)"

# Restore database from backup
db-restore:
	@echo "$(COLOR_YELLOW)Warning: This will overwrite the current database!$(COLOR_NC)"
	@read -p "Enter backup file name (from $(BACKUP_DIR)/ directory): " BACKUP_FILE && \
	if [ -f "$(BACKUP_DIR)/$$BACKUP_FILE" ]; then \
		echo "$(COLOR_BLUE)Restoring database from backup...$(COLOR_NC)" && \
		docker compose -f $(COMPOSE_FILE) exec -T $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" && \
		cat $(BACKUP_DIR)/$$BACKUP_FILE | docker compose -f $(COMPOSE_FILE) exec -T $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) && \
		echo "$(COLOR_GREEN)✅ Database restored successfully!$(COLOR_NC)"; \
	else \
		echo "$(COLOR_RED)Error: Backup file $(BACKUP_DIR)/$$BACKUP_FILE not found!$(COLOR_NC)"; \
	fi

# =====================================================================
# Testing Commands
# =====================================================================

test:
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) pytest

health:
	@echo "$(COLOR_BLUE)Checking service health...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) ps
	mali-data-test:
	@echo "$(COLOR_BLUE)Testing Mali reference data endpoints...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) curl -s http://localhost:8000/v1/instat/mali/regions | grep -q "data" && \
	echo "$(COLOR_GREEN)✅ Mali regions endpoint working$(COLOR_NC)" || echo "$(COLOR_RED)❌ Mali regions endpoint failed$(COLOR_NC)"

template-test:
	@echo "$(COLOR_BLUE)Testing template endpoints...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) curl -s http://localhost:8000/v1/instat/templates | grep -q "data" && \
	echo "$(COLOR_GREEN)✅ Templates endpoint working$(COLOR_NC)" || echo "$(COLOR_RED)❌ Templates endpoint failed$(COLOR_NC)"

auth-test:
	@echo "$(COLOR_BLUE)Testing authentication system...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) curl -s -X POST http://localhost:8000/v1/api/auth/token -d "username=admin@instat.gov.ml&password=admin123" | grep -q "access_token" && \
	echo "$(COLOR_GREEN)✅ Authentication system working$(COLOR_NC)" || echo "$(COLOR_RED)❌ Authentication system failed$(COLOR_NC)"

# =====================================================================
# Audit & Analytics
# =====================================================================

audit-logs:
	@echo "$(COLOR_BLUE)Viewing recent audit logs...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) python -m scripts.view_audit_logs

parsing-stats:
	@echo "$(COLOR_BLUE)Viewing parsing statistics...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) python -m scripts.view_parsing_stats

# =====================================================================
# Cleanup Commands
# =====================================================================

clean:
	@echo "$(COLOR_BLUE)Cleaning up Docker environment...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
	@docker volume prune -f
	@docker network prune -f

clean-all: clean
	@echo "$(COLOR_BLUE)Complete cleanup including images...$(COLOR_NC)"
	@docker image prune -af

# =====================================================================
# Development Commands
# =====================================================================

dev-setup:
	@echo "$(COLOR_BLUE)Setting up development environment...$(COLOR_NC)"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

dev-run:
	@echo "$(COLOR_BLUE)Running in development mode...$(COLOR_NC)"
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

dev-test:
	@echo "$(COLOR_BLUE)Running development tests...$(COLOR_NC)"
	python -m pytest

format:
	@echo "$(COLOR_BLUE)Formatting code with black...$(COLOR_NC)"
	black .

lint:
	@echo "$(COLOR_BLUE)Running linting checks...$(COLOR_NC)"
	flake8 .
	security-scan:
	@echo "$(COLOR_BLUE)Running security vulnerability scan...$(COLOR_NC)"
	bandit -r src/

# =====================================================================
# Legacy Commands - Kept for backward compatibility
# =====================================================================

migrate: db-migrate
	@echo "$(COLOR_YELLOW)Note: 'migrate' is deprecated, use 'db-migrate' instead$(COLOR_NC)"

migrate-new:
	@echo "$(COLOR_BLUE)Creating new migration script...$(COLOR_NC)"
	@docker compose -f $(COMPOSE_FILE) exec $(APP_CONTAINER) alembic revision --autogenerate -m "New migration"

db-upgrade: db-migrate
	@echo "$(COLOR_YELLOW)Note: 'db-upgrade' is deprecated, use 'db-migrate' instead$(COLOR_NC)"

