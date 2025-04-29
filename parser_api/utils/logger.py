import logging
import sys
from pathlib import Path
from parser_api.config.settings import settings

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file and console handlers"""
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)

    # Create logs directory if it doesn't exist
    log_file = Path(settings.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(settings.LOG_FORMAT))
    logger.addHandler(console_handler)

    return logger

# Create default logger
logger = setup_logger("parser_api") 