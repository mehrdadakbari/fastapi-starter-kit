from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from routes import user
from core.logging_config import setup_logging
from core.config import settings
from core.database import lifespan

# -----------------------------
# Setup logging
# -----------------------------
setup_logging()
logger = logging.getLogger(__name__)

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
    debug=settings.debug
)

# -----------------------------
# CORS Middleware
# -----------------------------
origins = ["http://localhost:8080"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API Prefix
# -----------------------------
api_prefix = "/api/v1"
app.include_router(user.router, prefix=api_prefix)
#app.include_router(jwt_auth.router, prefix=api_prefix)

# -----------------------------
# Project info route
# -----------------------------
@app.get("/", summary="Get project info")
def get_project_info():
    """Returns basic project information."""
    return {
        "project": settings.app_name,
        "version": settings.version,
        "debug": settings.debug,
        "environment": settings.environment
    }

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
