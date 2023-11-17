import logging
from logging.handlers import RotatingFileHandler
import asyncio

# Configure logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

# Rotating file handler
file_handler = RotatingFileHandler('discord.log', maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(file_handler)

# Stream handler for console output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def log_message(message, level=logging.INFO, callback=None):
    """
    Log a message at the specified level and optionally call a callback.
    """
    if level == logging.DEBUG:
        logger.debug(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.CRITICAL:
        logger.critical(message)
    else:
        logger.info(message)

    # If a callback is provided, use it to update the GUI
    if callback:
        asyncio.create_task(callback(message))

def log_exception(exc, callback=None):
    """
    Log an exception with a stack trace and optionally call a callback.
    """
    logger.exception(exc)
    if callback:
        asyncio.create_task(callback(f"Exception: {exc}"))

def get_logger(name):
    """
    Get a logger with the specified name.
    """
    new_logger = logging.getLogger(name)
    new_logger.setLevel(logging.INFO)

    # Create a console handler and set the level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    new_logger.addHandler(ch)

    return new_logger

# Example usage in other parts of the program:
# log_message("Some message", callback=update_log)
# log_exception(some_exception, callback=update_log)
