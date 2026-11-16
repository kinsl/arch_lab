import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from notification_service.modules.notifications.domain.errors import (
    ConflictError,
    DependencyUnavailableError,
    InvalidUserError,
    NotFoundError,
)

logger = logging.getLogger(__name__)

ERROR_STATUSES: dict[type[Exception], int] = {
    NotFoundError: 404,
    ConflictError: 409,
    InvalidUserError: 422,
    DependencyUnavailableError: 503,
}


def application_error(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=ERROR_STATUSES[type(exc)], content={"detail": str(exc)})


def database_error(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Database request failed", exc_info=exc)
    return JSONResponse(status_code=503, content={"detail": "Database temporarily unavailable"})


def register_error_handlers(app: FastAPI) -> None:
    for error in ERROR_STATUSES:
        app.add_exception_handler(error, application_error)
    app.add_exception_handler(SQLAlchemyError, database_error)
