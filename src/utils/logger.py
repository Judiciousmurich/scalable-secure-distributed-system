import logging
import os
from datetime import datetime

def setup_logging(name, log_level=logging.INFO):
    """Configure logging for the application"""
    # Ensure logs directory exists
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    # Create unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(name)

def log_error(logger, error_message, exception=None):
    """Log error with optional exception details"""
    if exception:
        logger.error(f"{error_message}: {str(exception)}")
    else:
        logger.error(error_message)

def log_info(logger, message):
    """Log informational message"""
    logger.info(message)

def log_debug(logger, message):
    """Log debug message"""
    logger.debug(message)