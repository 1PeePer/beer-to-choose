import asyncio
import sys
from fastapi import FastAPI
from parser_api.api.routes import products
from parser_api.config.settings import settings
from parser_api.utils.logger import logger

# Настройка event loop для Windows
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

# Include routers
app.include_router(products.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Log startup event"""
    logger.info("API started")

@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown event"""
    logger.info("API stopped") 