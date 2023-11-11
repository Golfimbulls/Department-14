import discord
from gui import update_log  # Import the update_log function from gui.py

async def log_message(message):
    """
    Log a message to the GUI.
    """
    update_log(message)  # Use the update_log function to append the message to the GUI

# Example of a logging function
async def log_member_join(member):
    await log_message(f'{member.name} has joined the server.')

# You can add more functions here for different logging purposes,
# such as logging message deletions, edits, member leaves, etc.
