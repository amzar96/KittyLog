import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from src.config import settings
from src.shared.seed import run_seed
from src.utils.db import SessionLocal
from src.utils.logger import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    db = SessionLocal()
    try:
        run_seed(db)
    except Exception:
        logger.exception("Failed to seed database")
    finally:
        db.close()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="KittyLog",
        description="API for cat parents to manage everything about their cats' lives",
        version="1.0.0",
        docs_url="/docs",
        lifespan=lifespan,
    )

    app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

    from src.domains.auth.router import router as auth_router
    from src.domains.cats.router import router as cats_router
    from src.domains.health.router import router as health_router
    from src.domains.nutrition.router import router as nutrition_router
    from src.domains.diary.router import router as diary_router
    from src.domains.monitoring.router import router as monitoring_router
    from src.domains.appointments.router import router as appointments_router
    from src.domains.notifications.router import router as notifications_router

    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(cats_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(nutrition_router, prefix="/api/v1")
    app.include_router(diary_router, prefix="/api/v1")
    app.include_router(monitoring_router, prefix="/api/v1")
    app.include_router(appointments_router, prefix="/api/v1")
    app.include_router(notifications_router, prefix="/api/v1")

    @app.get("/health")
    async def health_check():
        return {"message": "server is up"}

    return app


app = create_app()
