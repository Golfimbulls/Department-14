import discord
from discord.ext import commands
import commands as bot_commands
import threading
import bot_logging
import event_handlers
import asyncio
import gui

# Import configurations from config.py
from config import COMMAND_PREFIX, TOKEN_FILE, LOG_CHANNEL_ID

# Global references
bot = None
loop = None

# Initialize logger
logger = bot_logging.get_logger(__name__)

def run_bot(token, log_channel_id=LOG_CHANNEL_ID):  # Use LOG_CHANNEL_ID from config.py
    global bot, loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if not token or not isinstance(token, str):
        logger.error("Invalid or no token provided. Exiting.")
        return

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)  # Use COMMAND_PREFIX from config.py
    loop = asyncio.get_event_loop()

    bot_commands.register_commands(bot)
    event_handlers.setup(bot)

    @bot.event
    async def on_ready():
        try:
            log_channel = bot.get_channel(int(log_channel_id)) if log_channel_id else None
            if log_channel:
                await log_channel.send(f'{bot.user.name} has connected to Discord!')
            else:
                raise ValueError("Log channel not found. Please check the LOG_CHANNEL_ID in config.py.")
        except Exception as e:
            logger.exception("Error in on_ready")

    try:
        bot.run(token)
    except Exception as e:
        logger.exception("Error running bot")

def start_gui(run_bot_callback):
    global gui_instance
    gui_instance = gui.BotGUI(run_bot_callback)
    gui_instance.mainloop()

async def change_bot_status(status):
    """ Change the bot's status (online, idle, invisible). """
    if bot:
        status_dict = {
            'online': discord.Status.online,
            'idle': discord.Status.idle,
            'invisible': discord.Status.invisible
        }
        await bot.change_presence(status=status_dict.get(status, discord.Status.online))

def update_bot_status(status):
    """ Wrapper to run the asynchronous change_bot_status function. """
    if loop and bot:
        asyncio.run_coroutine_threadsafe(change_bot_status(status), loop)

async def set_bot_channel(channel_id):
    """ Set the channel ID for the bot to enter. """
    if bot:
        channel = bot.get_channel(int(channel_id))
        if channel:
            # Implement the logic to set the bot's channel
            # For example, sending a message to the channel
            await channel.send("Bot has entered the channel.")

async def get_online_users_in_channel(channel_id):
    """ Fetch online users in a specific channel with rate limit handling. """
    if bot:
        channel = bot.get_channel(int(channel_id))
        if channel:
            try:
                # Attempt to fetch members
                return [member.name for member in channel.members if str(member.status) == 'online']
            except discord.HTTPException as e:
                if e.status == 429:
                    # Handle rate limit exceeded
                    logger.warning("Rate limit exceeded. Retrying later.")
                    # Optionally, implement a retry mechanism
                else:
                    # Handle other HTTP exceptions
                    logger.error(f"HTTP error occurred: {e}")
            except Exception as e:
                # Handle other exceptions
                logger.error(f"Error occurred: {e}")
    return []

def set_channel(channel_id):
    """ Wrapper to run the asynchronous set_bot_channel function. """
    if loop and bot:
        asyncio.run_coroutine_threadsafe(set_bot_channel(channel_id), loop)
        
async def get_server_list():
    """ Fetch the list of servers the bot is connected to. """
    if bot:
        try:
            guilds = bot.guilds
            return [(guild.name, guild.id, guild.member_count) for guild in guilds]
        except discord.HTTPException as e:
            if e.status == 429:
                # Handle rate limit exceeded
                logger.warning("Rate limit exceeded while fetching server list. Retrying later.")
                # Optionally, implement a retry mechanism
            else:
                # Handle other HTTP exceptions
                logger.error(f"HTTP error occurred while fetching server list: {e}")
        except Exception as e:
            # Handle other exceptions
            logger.error(f"Error occurred while fetching server list: {e}")
    return []

def get_server_list_sync():
    """ Synchronous wrapper for the asynchronous get_server_list function. """
    if loop and bot:
        return asyncio.run_coroutine_threadsafe(get_server_list(), loop).result()

if __name__ == "__main__":
    try:
        # Read the token from the file specified in TOKEN_FILE
        with open(TOKEN_FILE, 'r') as file:
            token = file.read().strip()

        gui_thread = threading.Thread(target=start_gui, args=(lambda: run_bot(token),), daemon=True)
        gui_thread.start()
        gui_thread.join()
    except Exception as e:
        logger.exception("Error starting GUI thread")