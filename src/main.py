# src/main.py
# FastAPI packages
import gc
import warnings
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from config import global_settings
from database import create_engine_and_sessionmaker
from logging_config import logger, shutdown_logging

warnings.filterwarnings("ignore")

logger.info("Starting fastapi-microservice-template application...")


# ---------------- Lifespan ---------------- #
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App is starting up...")
    if global_settings.database_url:
        engine, sessionmaker = create_engine_and_sessionmaker(
            global_settings.database_url,
            pool_size=global_settings.db_pool_size,
            max_overflow=global_settings.db_max_overflow,
            pool_timeout=global_settings.db_pool_timeout,
            pool_recycle=global_settings.db_pool_recycle,
        )
        app.state.engine = engine
        app.state.sessionmaker = sessionmaker

        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logger.info("Database connection is ready.")
        except Exception:
            logger.exception("Database startup check failed.")
            raise
    else:
        logger.warning(
            "GLOBAL_DATABASE_URL is not set. Starting without database connectivity."
        )

    yield

    logger.info("App is shutting down...")
    try:
        if hasattr(app.state, "engine"):
            await app.state.engine.dispose()
            logger.info("Database engine disposed.")
        gc.collect()
    finally:
        shutdown_logging()


# ---------------- App Setup ---------------- #
app = FastAPI(
    title="fastapi-microservice-template",
    description="A clean, modular FastAPI microservice template.",
    version="0.0.1",
    lifespan=lifespan,  # <- use lifespan here
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Routers ---------------- #
# app.include_router(orchestrator_router)


# ---------------- Endpoints ---------------- #
@app.get("/")
async def read_root():
    return "Welcome to fastapi-microservice-template"


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# ---------------- Run ---------------- #
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
