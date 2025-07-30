"""Main FastAPI application."""

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ray
from ray import serve

from src.config.settings import settings
from src.config.ray_config import RAY_INIT_CONFIG
from src.api.endpoints import health, inference
from src.services.ray_serve import init_ray_serve, shutdown_ray_serve

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting MLServe application...")
    
    try:
        # Initialize Ray
        if not ray.is_initialized():
            logger.info("Initializing Ray...")
            ray.init(**RAY_INIT_CONFIG)
            logger.info(f"Ray initialized. Dashboard at: http://localhost:8265")
        
        # Initialize Ray Serve
        await init_ray_serve()
        logger.info("Ray Serve initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down MLServe application...")
    try:
        await shutdown_ray_serve()
        if ray.is_initialized():
            ray.shutdown()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    openapi_url=f"{settings.api_prefix}/openapi.json",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    health.router,
    prefix=settings.api_prefix,
    tags=["health"]
)

app.include_router(
    inference.router,
    prefix=settings.api_prefix,
    tags=["inference"]
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to MLServe API",
        "version": settings.app_version,
        "docs": f"{settings.api_prefix}/docs",
        "ray_dashboard": "http://localhost:8265",
        "endpoints": {
            "health": f"{settings.api_prefix}/health",
            "models": f"{settings.api_prefix}/models",
            "predict": f"{settings.api_prefix}/predict",
            "ray_status": f"{settings.api_prefix}/ray/status"
        }
    }