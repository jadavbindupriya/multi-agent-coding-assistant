# backend/main.py
"""
Main FastAPI application.

This file:
1. Creates the FastAPI app
2. Includes routes
3. Handles startup/shutdown
4. Configures middleware
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from datetime import datetime

from backend.config import settings
from backend.api.routes import router

# ========================
# LOGGING SETUP
# ========================

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger(__name__)

# ========================
# CREATE FASTAPI APP
# ========================

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# ========================
# CORS CONFIGURATION
# ========================
# CORS = Cross-Origin Resource Sharing
# Why? React frontend (localhost:3000) needs to call backend (localhost:8000)
# Without CORS, browser blocks the request

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins like ["https://example.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("✅ CORS middleware configured")

# ========================
# INCLUDE ROUTES
# ========================

app.include_router(router, prefix="/api", tags=["tasks"])

# ========================
# HEALTH CHECK ENDPOINT
# ========================

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Client calls this to verify backend is running.
    
    Usage:
    GET http://localhost:8000/health
    
    Response:
    {
        "status": "healthy",
        "timestamp": "2024-01-01T12:00:00",
        "environment": "development"
    }
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.ENVIRONMENT
    }

# ========================
# ROOT ENDPOINT
# ========================

@app.get("/")
async def root():
    """
    Root endpoint. Client can check this to see API info.
    """
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

# ========================
# STARTUP/SHUTDOWN EVENTS
# ========================

@app.on_event("startup")
async def startup_event():
    """Run when FastAPI server starts"""
    logger.info("=" * 50)
    logger.info("🚀 Backend starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug: {settings.DEBUG}")
    logger.info(f"API Key loaded: {bool(settings.OPENAI_API_KEY)}")
    logger.info("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    """Run when FastAPI server shuts down"""
    logger.info("🛑 Backend shutting down...")

# ========================
# ERROR HANDLER
# ========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom error handler for HTTPException.
    Returns consistent error format.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Request failed",
            "detail": exc.detail,
            "code": exc.status_code
        }
    )