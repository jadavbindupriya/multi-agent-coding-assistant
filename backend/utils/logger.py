# backend/utils/logger.py
"""
Logging configuration for the application.

Why logging?
- Track what the agents are doing
- Debug issues in production
- Monitor system health
"""

import logging
import sys
from backend.config import settings

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger for a module.
    
    Args:
        name: Module name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(settings.LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

# Create a global logger
logger = setup_logger(__name__)