import logging
from logging.handlers import RotatingFileHandler
import asyncio
from gui import update_log  # Import the update_log function from gui.py

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

async def log_to_gui(message):
    """
    Log a message to the GUI.
    """
    update_log(message)

def log_message(message, level=logging.INFO):
    """
    Log a message at the specified level.
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
    
    # Log to GUI asynchronously
    asyncio.create_task(log_to_gui(message))

def log_exception(exc):
    """
    Log an exception with a stack trace.
    """
    logger.exception(exc)
    asyncio.create_task(log_to_gui(f"Exception: {exc}"))

# Example of a logging function
async def log_member_join(member):
    await log_message(f'{member.name} has joined the server.')
    
def get_logger(name):
    # Create a logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a console handler and set the level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger

# You can add more functions here for different logging purposes
