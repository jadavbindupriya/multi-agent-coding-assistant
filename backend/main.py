# backend/main.py
"""Main FastAPI application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from datetime import datetime

from backend.config import settings
from backend.api.routes import router
from backend.api.knowledge import router as knowledge_router
from backend.api.integrations import router as integrations_router
from backend.api.analytics import router as analytics_router
from backend.middleware.metrics import MetricsMiddleware
from backend.mcp.client import mcp_client

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(MetricsMiddleware)

app.include_router(router, prefix="/api", tags=["tasks"])
app.include_router(knowledge_router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(integrations_router, prefix="/api/integrations", tags=["integrations"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.ENVIRONMENT,
        "features": {
            "rag": True,
            "tools": settings.ENABLE_TOOLS,
            "test_execution": settings.ENABLE_TEST_EXECUTION,
            "mcp_services": mcp_client.available_services(),
        },
    }


@app.get("/")
async def root():
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": settings.API_DESCRIPTION,
        "docs": "/docs",
        "features": ["RAG", "Tool Calling", "MCP", "Enhanced Testing", "Analytics"],
    }


@app.on_event("startup")
async def startup_event():
    import os
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.KNOWLEDGE_UPLOAD_DIR, exist_ok=True)
    logger.info("=" * 50)
    logger.info("🚀 Backend starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"MCP services: {mcp_client.available_services() or 'none configured'}")
    logger.info("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Backend shutting down...")


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Request failed", "detail": exc.detail, "code": exc.status_code},
    )
