import threading
import gui
import os
import bot_runner
import bot_logging
import token_manager

def run_bot_thread(token):
    """Run the bot in a separate thread."""
    bot_thread = threading.Thread(target=bot_runner.run_bot, args=(token,), daemon=True)
    bot_thread.start()

def main():
    # Initialize logger
    logger = bot_logging.get_logger(__name__)

    # Display the splash screen first
    gui.show_splash_screen()

    # Initialize the GUI
    gui_app = gui.BotGUI()

    # Check if the token file exists and read the token
    token = None
    if os.path.exists(token_manager.TOKEN_FILE):
        with open(token_manager.TOKEN_FILE, 'r') as file:
            token = file.read().strip()

    # Start the bot in a separate thread if token exists
    if token:
        run_bot_thread(token)
    else:
        logger.error("Token not set. Please set the token using the GUI.")

    # Run the GUI's main loop in the main thread
    gui_app.mainloop()

if __name__ == "__main__":
    main()
