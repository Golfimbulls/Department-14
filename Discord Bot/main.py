import discord
from discord.ext import commands
import commands as bot_commands
import threading
import bot_logging  # Import the logging module
# import config  # Import the config module (No longer needed for LOG_CHANNEL_ID)
import event_handlers  # Import the event handlers module
import asyncio
import gui  # Import the GUI module

# Global references
bot = None
loop = None

def run_bot(token, log_channel_id=None):
    global bot, loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if not token or not isinstance(token, str):
        print("Invalid or no token provided. Exiting.")
        return

    intents = discord.Intents.default()
    intents.members = True  # If you've enabled "Server Members Intent"
    intents.message_content = True  # If you've enabled "Message Content Intent"
    bot = commands.Bot(command_prefix='!', intents=intents)


    bot = commands.Bot(command_prefix='!', intents=intents)
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
            print(f"Error in on_ready: {e}")

    try:
        bot.run(token)
    except Exception as e:
        print(f"Error running bot: {e}")

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

def set_channel(channel_id):
    """ Wrapper to run the asynchronous set_bot_channel function. """
    if loop and bot:
        asyncio.run_coroutine_threadsafe(set_bot_channel(channel_id), loop)

if __name__ == "__main__":
    try:
        gui_thread = threading.Thread(target=start_gui, args=(run_bot,), daemon=True)
        gui_thread.start()
        gui_thread.join()
    except Exception as e:
        print(f"Error starting GUI thread: {e}")