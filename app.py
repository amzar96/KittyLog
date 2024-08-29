import logging
from core import models
from fastapi import FastAPI
from database.db import engine
from routers import users, cats


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KittyLog",
    description="API for KittyLog",
    version="0.0.1",
    docs_url="/docs",
)

app.include_router(users.router)
app.include_router(cats.router)

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@app.get("/health")
async def root():
    return {"message": "server is up"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
