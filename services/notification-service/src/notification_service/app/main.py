from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from notification_service.app.config import Config
from notification_service.app.di_container import create_container
from notification_service.app.errors import register_error_handlers
from notification_service.app.health import router as health_router
from notification_service.app.lifespan import lifespan
from notification_service.app.logging_setup import setup_logging
from notification_service.modules.notifications.presentation.http.router import router


def create_app() -> FastAPI:
    setup_logging()
    config = Config.from_env()
    app = FastAPI(title="Notification Service", version="1.0.0", lifespan=lifespan)
    setup_dishka(create_container(config), app)
    register_error_handlers(app)
    app.include_router(router)
    app.include_router(health_router)
    return app
