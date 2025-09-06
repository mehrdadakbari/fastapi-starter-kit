import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from mongoengine import connect, disconnect

from core.config import settings

logger = logging.getLogger(__name__)


def init_db():
    """Initialize MongoDB connection."""
    try:
        connect(
            db = settings.db_name,
            username = settings.db_user,
            password = settings.db_password,
            host = settings.db_host,
            port = settings.db_port,
            uuidRepresentation="standard"
        )

        logger.info("✅ Connected to MongoDB")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise


def close_db():
    """Close MongoDB connection."""
    try:
        disconnect()
        logger.info("❌ Disconnected from MongoDB")
    except Exception as e:
        logger.warning(f"⚠️ Error while disconnecting MongoDB: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan for startup/shutdown DB management."""
    init_db()
    try:
        yield
    finally:
        close_db()
