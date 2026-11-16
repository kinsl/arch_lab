from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from order_service.app.config import Config
from order_service.app.di_container import create_container
from order_service.app.errors import register_error_handlers
from order_service.app.health import router as health_router
from order_service.app.lifespan import lifespan
from order_service.app.logging_setup import setup_logging
from order_service.modules.orders.presentation.http.router import router


def create_app() -> FastAPI:
    setup_logging()
    config = Config.from_env()
    app = FastAPI(title="Order Service", version="1.0.0", lifespan=lifespan)
    setup_dishka(create_container(config), app)
    register_error_handlers(app)
    app.include_router(router)
    app.include_router(health_router)
    return app
