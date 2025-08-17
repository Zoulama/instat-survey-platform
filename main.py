# /instat-survey-platform/main.py

import logging.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from src.api.v1 import (
    surveys, file_upload, instat_routes, mali_reference_routes,
    auth_routes, admin_routes
)
from src.infrastructure.database.connection import db_manager
from src.utils.exception_handler import (
    validation_exception_handler,
    http_exception_handler,
    generic_exception_handler
)
from fastapi.exceptions import RequestValidationError, HTTPException

# Configure logging
try:
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
except:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_application():
    """Create FastAPI application"""
    _app = FastAPI(
        title=config.APP_NAME,
        version=config.APP_VERSION,
        description=config.APP_DESCRIPTION,
        debug=config.DEBUG_MODE
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in config.ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=config.ALLOWED_METHODS,
        allow_headers=config.ALLOWED_HEADERS,
    )

    @_app.on_event("startup")
    async def startup():
        logger.info("Starting up...")
        db_manager.create_tables()  # Create tables on startup

    @_app.on_event("shutdown")
    async def shutdown():
        logger.info("Shutting down...")

    # Add exception handlers
    _app.add_exception_handler(RequestValidationError, validation_exception_handler)
    _app.add_exception_handler(HTTPException, http_exception_handler)
    _app.add_exception_handler(Exception, generic_exception_handler)

    # Include routers
    _app.include_router(auth_routes.router)
    _app.include_router(admin_routes.router)
    _app.include_router(surveys.router)
    _app.include_router(file_upload.router)
    _app.include_router(instat_routes.router)
    _app.include_router(mali_reference_routes.router)

    return _app


app = get_application()
