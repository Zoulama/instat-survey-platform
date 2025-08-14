"""
Configuration management for INSTAT Survey Platform
"""
from os import environ as env
from typing import Optional


def __getattr__(name):
    """Get environment variable by name"""
    return env.get(name.upper(), None)


# Application Configuration
APP_NAME = env.get("APP_NAME", "INSTAT Survey Platform")
APP_VERSION = env.get("APP_VERSION", "1.0.0")
APP_DESCRIPTION = env.get("APP_DESCRIPTION", "Digital Platform for Managing Statistical Activities")
DEBUG_MODE = env.get("DEBUG_MODE", "true").lower() == "true"

# Database Configuration
DATABASE_URL = env.get("DATABASE_URL", "postgresql://postgres:password@localhost:5432/instat_surveys")
DATABASE_POOL_SIZE = int(env.get("DATABASE_POOL_SIZE", "10"))
DATABASE_MAX_OVERFLOW = int(env.get("DATABASE_MAX_OVERFLOW", "20"))

# Authentication
SECRET_KEY = env.get("SECRET_KEY", "your-secret-key-change-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
ALGORITHM = env.get("ALGORITHM", "HS256")

# File Upload Configuration
MAX_FILE_SIZE = int(env.get("MAX_FILE_SIZE", "10485760"))  # 10MB
ALLOWED_FILE_EXTENSIONS = env.get("ALLOWED_FILE_EXTENSIONS", ".xlsx,.xls,.docx,.doc,.pdf").split(",")
UPLOAD_DIR = env.get("UPLOAD_DIR", "uploads")

# AI Configuration (optional)
OPENAI_API_KEY = env.get("OPENAI_API_KEY")
ENABLE_AI_FEATURES = env.get("ENABLE_AI_FEATURES", "false").lower() == "true"

# External Services
SUPERSET_URL = env.get("SUPERSET_URL")
SUPERSET_USERNAME = env.get("SUPERSET_USERNAME")
SUPERSET_PASSWORD = env.get("SUPERSET_PASSWORD")

# Logging Configuration
LOG_LEVEL = env.get("LOG_LEVEL", "INFO")
LOG_FORMAT = env.get("LOG_FORMAT", "json")

# CORS Configuration
ALLOWED_ORIGINS = env.get("ALLOWED_ORIGINS", "*").split(",")
ALLOWED_METHODS = env.get("ALLOWED_METHODS", "GET,POST,PUT,DELETE,PATCH").split(",")
ALLOWED_HEADERS = env.get("ALLOWED_HEADERS", "*").split(",")

# Redis Configuration (for caching)
REDIS_URL = env.get("REDIS_URL", "redis://localhost:6379")

# Email Configuration (for notifications)
SMTP_SERVER = env.get("SMTP_SERVER")
SMTP_PORT = int(env.get("SMTP_PORT", "587"))
SMTP_USERNAME = env.get("SMTP_USERNAME")
SMTP_PASSWORD = env.get("SMTP_PASSWORD")
SMTP_USE_TLS = env.get("SMTP_USE_TLS", "true").lower() == "true"

# Survey Configuration
DEFAULT_PAGE_SIZE = int(env.get("DEFAULT_PAGE_SIZE", "20"))
MAX_PAGE_SIZE = int(env.get("MAX_PAGE_SIZE", "100"))

# Form Generation
FORM_TEMPLATES_DIR = env.get("FORM_TEMPLATES_DIR", "templates/forms")
GENERATED_FORMS_DIR = env.get("GENERATED_FORMS_DIR", "generated/forms")

# Data Processing
PROCESSING_BATCH_SIZE = int(env.get("PROCESSING_BATCH_SIZE", "1000"))
ENABLE_BACKGROUND_PROCESSING = env.get("ENABLE_BACKGROUND_PROCESSING", "true").lower() == "true"
