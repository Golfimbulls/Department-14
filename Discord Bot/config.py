# config.py

# Discord Bot Configuration
# -------------------------
COMMAND_PREFIX = '!'  # Prefix for commands. This is used to recognize bot commands in messages.
TOKEN_FILE = 'token.txt'  # File name where the Discord bot token is stored. Ensure this file is secured and not tracked in version control.

# Logging Configuration
# ---------------------
LOG_CHANNEL_ID = 123456789012345678  # Discord channel ID for logging bot activities. Replace with your actual channel ID.

# Bot Features Configuration
# --------------------------
# Here, you can add configurations specific to the features of your bot.
# For example, IDs for roles or channels that the bot interacts with, or specific settings for certain commands.

# Ticket System Configuration (if implemented)
# --------------------------------------------
TICKET_CATEGORY_ID = 987654321098765432  # Discord category ID for ticket channels. Replace with your actual category ID.

# Moderation Features
# -------------------
# Configuration for moderation features of the bot.
# This can include role IDs for moderators, a list of banned words, auto-moderation settings, etc.

# API Keys (if your bot interacts with external services)
# -------------------------------------------------------
# SOME_API_KEY = 'your_api_key_here'
# Store API keys for any external services your bot interacts with.
# Ensure these keys are kept secure and not exposed in your codebase.

# Other Constants
# ---------------
# Define other constants that your bot may use.
# This can include welcome messages, default responses, error messages, or any other static data.

# Security Note:
# --------------
# It's important to keep sensitive data like API keys and tokens secure.
# Consider using environment variables or a secure vault for storing such information.
