import os

TOKEN_FILE = 'bot_token.txt'

def save_token(token):
    """Save the token to a file."""
    with open(TOKEN_FILE, 'w') as file:
        file.write(token)

def load_token():
    """Load the token from a file, or return None if it doesn't exist."""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return file.read().strip()
    else:
        # Create an empty file if it doesn't exist
        with open(TOKEN_FILE, 'w') as file:
            pass
    return None
