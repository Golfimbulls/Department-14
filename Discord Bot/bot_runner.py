import discord
from discord.ext import commands
import asyncio
import bot_logging
import event_handlers
from config import COMMAND_PREFIX, LOG_CHANNEL_ID

# Global variables for bot and event loop
bot = None
loop = None

def run_bot(token, log_channel_id=LOG_CHANNEL_ID):
    global bot, loop
    logger = bot_logging.get_logger(__name__)

    # Create a new event loop for the bot
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Set up the bot with the specified token
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

    # Register commands and event handlers
    # import bot_commands  # Uncomment if you have a separate module for commands
    # bot_commands.register_commands(bot)
    event_handlers.setup(bot)

    @bot.event
    async def on_ready():
        try:
            log_channel = bot.get_channel(int(log_channel_id))
            if log_channel:
                await log_channel.send(f'{bot.user.name} has connected to Discord!')
            else:
                raise ValueError("Log channel not found.")
        except Exception as e:
            logger.exception("Error in on_ready")

    # Run the bot
    try:
        bot.run(token)
    except Exception as e:
        logger.exception("Error running bot")

# Additional bot-related functions can be added here
