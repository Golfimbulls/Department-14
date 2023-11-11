import discord
from discord.ext import commands
import commands as bot_commands
import threading
import gui  # Import the GUI module
import bot_logging  # Import the logging module
import config  # Import the config module
import event_handlers  # Import the event handlers module

def run_bot(token):
    # Ensure the token is not None or empty
    if not token:
        print("No token provided. Exiting.")
        return

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
            else:
                raise ValueError("Log channel not found. Please check the LOG_CHANNEL_ID in config.py.")
        except Exception as e:
            print(f"Error in on_ready: {e}")

    # Run the bot
    try:
        bot.run(token)
    except Exception as e:
        print(f"Error running bot: {e}")

def start_gui(run_bot_callback):
    global gui_instance
    gui_instance = gui.BotGUI(run_bot_callback)
    gui_instance.mainloop()

if __name__ == "__main__":
    try:
        # Pass the run_bot function as a callback to the GUI
        gui_thread = threading.Thread(target=start_gui, args=(run_bot,), daemon=True)
        gui_thread.start()
        gui_thread.join()
    except Exception as e:
        print(f"Error starting GUI thread: {e}")
