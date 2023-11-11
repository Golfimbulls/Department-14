import discord
from discord.ext import commands
import commands as bot_commands
import threading
import gui  # Import the GUI module
import bot_logging  # Import the logging module
import config  # Import the config module
import event_handlers  # Import the event handlers module

def run_bot(token):
    # Set up the bot with intents
    intents = discord.Intents.default()
    intents.members = True
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    # Register commands from commands.py
    bot_commands.register_commands(bot)

    # Register event handlers from event_handlers.py
    event_handlers.setup(bot)

    @bot.event
    async def on_ready():
        try:
            log_channel = bot.get_channel(config.LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(f'{bot.user.name} has connected to Discord!')
                gui.log_message(f'{bot.user.name} has connected to Discord!')
            else:
                raise ValueError("Log channel not found. Please check the LOG_CHANNEL_ID in config.py.")
        except Exception as e:
            gui.log_message(f"Error in on_ready: {e}")

    # Run the bot
    try:
        bot.run(token)
    except Exception as e:
        gui.log_message(f"Error running bot: {e}")

if __name__ == "__main__":
    try:
        gui_thread = threading.Thread(target=gui.start_gui, args=(run_bot,), daemon=True)
        gui_thread.start()
        gui_thread.join()
    except Exception as e:
        print(f"Error starting GUI thread: {e}")
