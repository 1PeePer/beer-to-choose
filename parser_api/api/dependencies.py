from fastapi import Depends
from parser_api.utils.logger import logger
from parser_api.parsers.lenta_parser import AsyncLentaProductParse
from parser_api.config.settings import settings

async def get_parser():
    """Dependency for getting parser instance"""
    try:
        parser = AsyncLentaProductParse(settings.DEFAULT_ADDRESS)
        return parser
    except Exception as e:
        logger.error(f"Error creating parser: {str(e)}")
        raise

async def get_logger():
    """Dependency for getting logger instance"""
    return logger 