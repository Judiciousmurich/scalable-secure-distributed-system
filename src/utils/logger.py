import logging
import os
from datetime import datetime
import sys

def setup_logging(name, log_level=logging.INFO, log_to_file=True):
    """
    Configure comprehensive logging for the application.
    
    Args:
        name (str): Logger name.
        log_level (int): Logging level.
        log_to_file (bool): Whether to log to file.
    
    Returns:
        logging.Logger: Configured logger.
    """
    # Ensure logs directory exists
    log_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{name}_{timestamp}.log")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_to_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def log_error(logger, error_message, exception=None):
    """
    Log error with optional exception details.
    
    Args:
        logger (logging.Logger): Logger instance.
        error_message (str): Error message.
        exception (Exception, optional): Exception object.
    """
    if exception:
        logger.error(f"{error_message}: {str(exception)}", exc_info=True)
    else:
        logger.error(error_message)

def log_info(logger, message):
    """Log informational message."""
    logger.info(message)

def log_debug(logger, message):
    """Log debug message."""
    logger.debug(message)

def log_warning(logger, message):
    """Log warning message."""
    logger.warning(message)
