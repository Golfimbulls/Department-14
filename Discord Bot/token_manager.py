import os
import logging

# Initialize logging
logger = logging.getLogger(__name__)

TOKEN_FILE = 'bot_token.txt'

def save_token(token, filepath=TOKEN_FILE):
    """Save the token to a file. Validate the token format before saving."""
    try:
        # Simple token format validation (you can enhance this as per your needs)
        if not token or not isinstance(token, str):
            raise ValueError("Invalid token format.")

        with open(filepath, 'w') as file:
            file.write(token)
        logger.info("Token successfully saved.")
    except Exception as e:
        logger.error(f"Error saving token: {e}")

def load_token(filepath=TOKEN_FILE):
    """Load the token from a file, or return None if it doesn't exist."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                return file.read().strip()
        else:
            # Create an empty file if it doesn't exist
            with open(filepath, 'w') as file:
                pass
        logger.info("Token file created.")
        return None
    except Exception as e:
        logger.error(f"Error loading token: {e}")
        return None
