"""
Discord Bot Control Panel GUI

This script creates a graphical user interface (GUI) for controlling and monitoring a Discord bot.
It is designed to be user-friendly and easily understandable for novice users.

Features:
- Start and stop the bot
- Change the bot's online status (online, idle, invisible)
- View and edit the bot's token
- Send commands to the bot
- Display bot's log and activity feed
- Manage channel IDs for logging and operation
- View online users and connected servers
- Toggle auto-moderation features

The GUI is organized into different sections for ease of use:
1. Menu Bar: For token management and log saving.
2. Bot Control Frame: Displays bot status, connected servers, and performance metrics.
3. Command Frame: Allows sending commands to the bot.
4. Notebook (Tab Control): Includes separate tabs for logs, user/server lists, and bot activity.

Each widget (button, label, entry field) is equipped with tooltips for additional guidance.

The script uses the tkinter library for creating the GUI components.
"""

# Import necessary modules from tkinter for creating the GUI
import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, filedialog, Menu, Label, Entry, Button, messagebox

from PIL import Image, ImageTk # PIL is used for image processing - useful for handling images in the GUI
import threading # threading is used for running tasks in separate threads
import token_manager # token_manager is a custom module for handling the bot's token
import event_handlers # event_handlers is a custom module for handling events in the application
# sys and os are standard Python modules for system and operating system functionalities
import sys
import os
import time # time module is used for time-related functions
import psutil

class Tooltip:
    """
    Create a tooltip for a given widget.

    This class is used to create small pop-up boxes (tooltips) that display
    information when the user hovers over a widget. It enhances the user
    experience by providing helpful hints or additional information about
    the GUI elements.
    """

    def __init__(self, widget, text):
        # Initialization function that sets up the tooltip
        self.waittime = 500     # Milliseconds to wait before showing the tooltip
        self.wraplength = 180   # Width in pixels before wrapping text to a new line
        self.widget = widget    # The widget the tooltip is attached to
        self.text = text        # The text displayed in the tooltip
        # Bind mouse events to the widget to show and hide the tooltip
        self.widget.bind("<Enter>", self.enter)  # Mouse enters the widget area
        self.widget.bind("<Leave>", self.leave)  # Mouse leaves the widget area
        self.widget.bind("<ButtonPress>", self.leave)  # Mouse clicks the widget
        self.id = None          # Used to keep track of the delay timer
        self.tw = None          # The tooltip window itself

    def enter(self, event=None):
        # Called when mouse enters the widget area
        self.schedule()         # Schedule the tooltip to appear

    def leave(self, event=None):
        # Called when mouse leaves the widget area or clicks on the widget
        self.unschedule()       # Cancel the tooltip if it's scheduled to appear
        self.hidetip()          # Hide the tooltip

    def schedule(self):
        # Schedule the tooltip to appear after a delay
        self.unschedule()       # Ensure no other tooltip is scheduled
        self.id = self.widget.after(self.waittime, self.showtip)  # Set a timer to show the tooltip

    def unschedule(self):
        # Cancel any scheduled tooltip
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)  # Cancel the timer

    def showtip(self, event=None):
        # Show the tooltip
        x, y, cx, cy = self.widget.bbox("insert")  # Get the position of the widget
        x += self.widget.winfo_rootx() + 25        # Adjust the x-coordinate
        y += self.widget.winfo_rooty() + 20        # Adjust the y-coordinate
        # Create a new top-level window for the tooltip
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)          # Remove window decorations
        self.tw.wm_geometry(f"+{x}+{y}")           # Set the position of the tooltip
        # Create a label inside the tooltip window to show the text
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)    # Pack the label into the window

    def hidetip(self):
        # Hide the tooltip
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()  # Destroy the tooltip window

class BotGUI(tk.Tk):
    # This class represents the main window of the Discord Bot Control Panel GUI
    def __init__(self, update_bot_status_callback=None):
        super().__init__()  # Initialize the superclass (tk.Tk) to set up the window
        self.title("Discord Bot Control Panel")  # Set the window title
        self.geometry("700x700")  # Set the window size to 700x700 pixels

        # Define the color scheme for the GUI
        self.bg_color = "#000000"  # Black background
        self.text_color = "#00FF00"  # Green text for contrast against the black background
        self.button_color = "#004d00"  # Dark green color for buttons
        self.button_text_color = "#00FF00"  # Green text on buttons for readability

        self.configure(bg=self.bg_color)  # Set the background color for the window
        self.update_bot_status_callback = update_bot_status_callback  # Callback function to update bot status

        # Set up various components of the GUI
        self.setup_menu_bar()  # Set up the menu bar at the top of the window
        self.setup_frames_and_panels()  # Set up the main frames and panels in the GUI
        self.add_tooltips()  # Add tooltips to provide additional information for widgets
        self.start_time = time.time()  # Record the start time for uptime calculation
        self.update_performance_metrics()  # Start updating performance metrics
        self.initialized = True  # Mark that initialization is complete

    def setup_menu_bar(self):
        # Set up the menu bar for the application
        menu_bar = Menu(self, bg="#003300", fg="#00FF00")  # Create a menu bar with dark green background
        self.config(menu=menu_bar)  # Add the menu bar to the main window

        # Create a 'File' menu
        file_menu = Menu(menu_bar, tearoff=0, bg="#003300", fg="#00FF00")
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Logs", command=self.save_log)
        file_menu.add_command(label="Exit", command=self.quit)

        # Create a 'Bot Token' menu
        token_menu = Menu(menu_bar, tearoff=0, bg="#003300", fg="#00FF00")
        menu_bar.add_cascade(label="Bot Token", menu=token_menu)
        token_menu.add_command(label="View Token", command=self.view_token)
        token_menu.add_command(label="Edit Token", command=self.edit_token)
        token_menu.add_command(label="Save Token", command=self.save_token)

        # Create a 'Bot Management' menu
        bot_management_menu = Menu(menu_bar, tearoff=0, bg="#003300", fg="#00FF00")
        menu_bar.add_cascade(label="Bot Management", menu=bot_management_menu)
        bot_management_menu.add_command(label="Start Bot", command=self.check_and_start_bot)
        bot_management_menu.add_command(label="Stop Bot", command=self.stop_bot)
        bot_management_menu.add_command(label="Restart Bot", command=self.restart_bot)

        # Create a 'Settings' menu
        settings_menu = Menu(menu_bar, tearoff=0, bg="#003300", fg="#00FF00")
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="General Settings", command=self.open_general_settings)
        settings_menu.add_command(label="Moderation Settings", command=self.open_moderation_settings)

        # Create a 'Help' menu
        help_menu = Menu(menu_bar, tearoff=0, bg="#003300", fg="#00FF00")
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.open_documentation)
        help_menu.add_command(label="About", command=self.open_about)
        
    # Placeholder methods for new menu actions
    def stop_bot(self):
        pass  # Logic to stop the bot

    def restart_bot(self):
        pass  # Logic to restart the bot

    def open_general_settings(self):
        pass  # Logic to open general settings dialog

    def open_moderation_settings(self):
        pass  # Logic to open moderation settings dialog

    def open_documentation(self):
        pass  # Logic to open documentation

    def open_about(self):
        about_text = """
        Discord Bot Control Panel
        Version: 1.0.0
        Developed by: Your Name or Your Organization's Name

        Description:
        This Discord bot is designed for gaming communities, offering features like dice rolling, character generation for D&D, game session scheduling, polls, game statistics, and the latest gaming news.

        Features:
        - Dice rolling with `!roll` command.
        - Random D&D character generation with `!character` command.
        - Game session scheduling with `!schedule` command.
        - Simple yes/no polls with `!poll` command.
        - Game statistics and latest gaming news.

        For more information, source code, and contributions, visit:
        https://github.com/Golfimbulls/Department-14

        Contact:
        If you have questions or want to reach out, contact <your_email>.

        Acknowledgments:
        - Contributors to this project.
        - Special thanks to [OpenAI](https://openai.com/) for language model assistance.
    
        Licensed under the MIT License.
        """
        messagebox.showinfo("About", about_text)
    
    def update_performance_metrics(self):
        # Calculate uptime
        uptime_seconds = time.time() - self.start_time
        uptime_str = time.strftime('%Hh %Mm %Ss', time.gmtime(uptime_seconds))

        cpu_usage = psutil.cpu_percent() # Get CPU usage
        self.performance_label.config(text=f"Uptime: {uptime_str}, CPU Usage: {cpu_usage}%") # Update the label

        # Schedule this method to be called again after 1000 milliseconds (1 second)
        self.after(1000, self.update_performance_metrics)

    def setup_frames_and_panels(self):
        # This method organizes the main sections (frames and panels) of the GUI.
        self.setup_bot_control_frame()  # Sets up the 'Bot Control Frame' which is a dedicated section in the GUI for displaying the bot's status, connected servers, and performance metrics.
        self.setup_command_frame()  # Initializes the 'Command Frame'. This is where the user can input and send commands to the Discord bot. It typically includes a text entry field and a send button.
        self.setup_channel_id_frame()  # Creates a frame for managing channel IDs. This is important for specifying which Discord channels the bot should log messages to or operate in. It is important to set this up before the notebook because it might be referenced in the tabs of the notebook.
        self.setup_notebook()  # Prepares a 'Notebook' widget, which is a tabbed control element in Tkinter. It allows the GUI to have multiple tabs for different purposes, such as logs, user/server lists, and activity feeds.
        self.setup_button_frame()  # Establishes a 'Button Frame' which contains various buttons for actions like starting the bot, toggling auto-moderation, and other functions. This is where you would add buttons that perform global actions related to the bot.

    def setup_bot_control_frame(self):
        # This method creates and configures the 'Bot Control Frame' within the GUI. This frame is dedicated to displaying various information about the bot's operational status.

        # Create a frame to hold bot control elements, with a black background.
        self.bot_control_frame = tk.Frame(self, bg="#000000")
        self.bot_control_frame.pack(padx=10, pady=5)

        # Bot Status Label: Shows the current status of the bot (e.g., online, offline). Initially set to "Unknown" until the bot's status is updated.
        self.bot_status_label = Label(self.bot_control_frame, text="Bot Status: Unknown", bg="#000000", fg="#00FF00")
        self.bot_status_label.pack(side=tk.LEFT, padx=5)

        # Server Count Label: Displays the number of servers the bot is currently connected to. Initially set to 0.
        self.server_count_label = Label(self.bot_control_frame, text="Connected Servers: 0", bg="#000000", fg="#00FF00")
        self.server_count_label.pack(side=tk.LEFT, padx=5)

        # Bot Performance Metrics: Shows key performance indicators such as uptime and CPU usage. Initially shows zero usage.
        self.performance_label = Label(self.bot_control_frame, text="Uptime: 0h 0m 0s, CPU Usage: 0%", bg="#000000", fg="#00FF00")
        self.performance_label.pack(side=tk.LEFT, padx=5)

        # Bot Status Control: A dropdown menu to change the bot's status (e.g., online, idle, invisible). This allows dynamic control over the bot's operational status.
        self.status_var = tk.StringVar(self)
        self.status_options = ['online', 'idle', 'invisible']
        self.status_menu = tk.OptionMenu(self.bot_control_frame, self.status_var, *self.status_options, command=self.change_bot_status)
        self.status_menu.config(bg="#004d00", fg="#00FF00")
        self.status_menu.pack(side=tk.LEFT, padx=5, pady=5)

        # Additional widgets can be added to this frame as needed to extend functionality.

    def setup_command_frame(self):
        self.command_frame = tk.Frame(self, bg="#000000")
        self.command_frame.pack(padx=10, pady=5)

        # Command input field
        self.command_entry = Entry(
            self.command_frame, bg="#ffffff", fg="#000000")
        self.command_entry.pack(side=tk.LEFT, padx=5)

        # Send Command button
        self.send_command_button = Button(
            self.command_frame, text="Send Command", command=self.send_command, bg="#004d00", fg="#00FF00")
        self.send_command_button.pack(side=tk.LEFT, padx=5)

    def setup_performance_metrics(self):
        # Bot Performance Metrics
        self.performance_label = Label(
            self.bot_control_frame, text="Uptime: 0h 0m 0s, CPU Usage: 0%", bg=self.bg_color, fg=self.text_color)
        self.performance_label.pack(side=tk.LEFT, padx=5)

    def setup_bot_status_control(self):
        # Bot Status and Server Count Labels
        self.bot_status_label = Label(
            self.bot_control_frame, text="Bot Status: Unknown", bg=self.bg_color, fg=self.text_color)
        self.bot_status_label.pack(side=tk.LEFT, padx=5)
        self.server_count_label = Label(
            self.bot_control_frame, text="Connected Servers: 0", bg=self.bg_color, fg=self.text_color)
        self.server_count_label.pack(side=tk.LEFT, padx=5)

        # Configuration Panel
        self.config_frame = tk.Frame(self, bg=self.bg_color)
        self.config_frame.pack(padx=10, pady=5)
        # Add configuration widgets here

        # Bot Status Control
        self.status_var = tk.StringVar(self)
        self.status_options = ['online', 'idle', 'invisible']
        self.status_menu = tk.OptionMenu(
            self.bot_control_frame, self.status_var, *self.status_options, command=self.change_bot_status)
        self.status_menu.config(bg=self.button_color,
                                fg=self.button_text_color)
        self.status_menu.pack(side=tk.LEFT, padx=5, pady=5)

    def setup_channel_id_frame(self):
        # New Frame for Channel IDs
        self.channel_id_frame = tk.Frame(self, bg=self.bg_color)
        self.channel_id_frame.pack(padx=10, pady=5)

        # Log Channel ID Entry
        self.log_channel_id_label = Label(
            self.channel_id_frame, text="Log Channel ID:", bg=self.bg_color, fg=self.text_color)
        self.log_channel_id_label.pack(side=tk.LEFT, padx=5)
        self.log_channel_id_entry = Entry(
            self.channel_id_frame, bg=self.bg_color, fg=self.text_color)
        self.log_channel_id_entry.pack(side=tk.LEFT, padx=5)

        # Channel ID Entry
        self.channel_id_label = Label(
            self.channel_id_frame, text="Channel ID:", bg=self.bg_color, fg=self.text_color)
        self.channel_id_label.pack(side=tk.LEFT, padx=5)
        self.channel_id_entry = Entry(
            self.channel_id_frame, bg=self.bg_color, fg=self.text_color)
        self.channel_id_entry.pack(side=tk.LEFT, padx=5)
        self.set_channel_button = Button(self.channel_id_frame, text="Set Channel",
                                         command=self.set_channel, bg=self.button_color, fg=self.button_text_color)
        self.set_channel_button.pack(side=tk.LEFT, padx=5)

    def setup_notebook(self):
        # Create Notebook (Tab Control)
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        # Tab 1: Log Area
        self.log_tab = tk.Frame(self.tab_control, bg=self.bg_color)
        self.tab_control.add(self.log_tab, text='Log')
        self.log_area = scrolledtext.ScrolledText(
            self.log_tab, state='disabled', wrap='word', bg=self.bg_color, fg=self.text_color)
        self.log_area.pack(padx=10, pady=10, fill='both', expand=True)

        # Tab 2: User and Server List
        self.user_server_tab = tk.Frame(self.tab_control, bg=self.bg_color)
        self.tab_control.add(self.user_server_tab, text='Users & Servers')
        self.setup_user_server_tab()  # Call a separate method to setup this tab

        # Tab 3: Bot Activity Feed
        self.activity_tab = tk.Frame(self.tab_control, bg=self.bg_color)
        self.tab_control.add(self.activity_tab, text='Activity Feed')
        self.setup_activity_tab()  # Call a separate method to setup this tab

    def setup_user_server_tab(self):
        # User List
        self.user_list_label = tk.Label(
            self.user_server_tab, text="Users", bg=self.bg_color, fg=self.text_color)
        self.user_list_label.pack(pady=(10, 0))
        self.user_list = tk.Listbox(
            self.user_server_tab, bg=self.bg_color, fg=self.text_color)
        self.user_list.pack(padx=10, pady=5, fill='both', expand=True)
        self.update_user_list()  # Populate the user list

        # Server List
        self.server_list_label = tk.Label(
            self.user_server_tab, text="Servers", bg=self.bg_color, fg=self.text_color)
        self.server_list_label.pack(pady=(10, 0))
        self.server_list = tk.Listbox(
            self.user_server_tab, bg=self.bg_color, fg=self.text_color)
        self.server_list.pack(padx=10, pady=5, fill='both', expand=True)
        self.update_server_list()  # Populate the server list

    def setup_activity_tab(self):
        # Activity Feed
        self.activity_feed = scrolledtext.ScrolledText(
            self.activity_tab, state='normal', wrap='word', bg="#ffffff", fg="#000000")
        self.activity_feed.pack(padx=10, pady=10, fill='both', expand=True)
        # Additional setup for the activity feed...

    # Methods to update user and server lists
    def update_user_list(self):
        # Logic to update the user list
        pass

    def update_server_list(self):
        # Logic to update the server list
        pass

    def setup_button_frame(self):
        # Button Frame
        self.button_frame = tk.Frame(self, bg=self.bg_color)
        self.button_frame.pack(padx=10, pady=5)

        # Auto Moderation Toggle Button
        self.auto_mod_button = tk.Button(
            self.button_frame,
            text="Toggle Auto Moderation",
            command=self.toggle_auto_mod,
            bg=self.button_color,
            fg=self.button_text_color
        )
        self.auto_mod_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Notification Alerts
        self.notification_label = Label(
            self.bot_control_frame,
            text="",
            bg=self.bg_color,
            fg=self.text_color
        )
        self.notification_label.pack(side=tk.LEFT, padx=5)

        # Add tooltips to widgets if necessary
        self.add_tooltips()

        # Implement any additional logic using the update_bot_status_callback if provided
        if self.update_bot_status_callback:
            # Additional callback logic
            pass

    def is_gui_initialized(self):
        """Utility function to check if the GUI is initialized."""
        return self.initialized

    def send_command(self):
        command = self.command_entry.get()
        # Logic to send the command to the bot
        self.log_message(f"Command sent: {command}")

    # Add tooltips to widgets
    def add_tooltips(self):
        Tooltip(self.status_menu, "Change the bot's online status.")
        Tooltip(self.log_channel_id_entry,
                "Enter the ID of the Discord channel for logging.")
        Tooltip(self.channel_id_entry,
                "Enter the ID of the Discord channel for the bot to operate in.")
        Tooltip(self.set_channel_button,
                "Set the bot to use the specified channel.")
        Tooltip(self.auto_mod_button, "Toggle automatic moderation features.")

    def check_and_start_bot(self):
        """ Check for a token and start the bot if available. Prompt for token if not set. """
        token = token_manager.load_token()
        if not token:
            # Prompt the user to enter the bot token if it's not already set
            token = simpledialog.askstring(
                "Enter Token", "Enter your Discord Bot Token:", parent=self)
            if token:
                # Save the newly entered token and start the bot
                token_manager.save_token(token)
                self.log_message("Token set. Starting bot.")
                threading.Thread(target=self.start_bot_thread,
                                 args=(token,), daemon=True).start()
            else:
                messagebox.showerror(
                    "Token Required", "No token provided. Unable to start bot.")
        else:
            # Token already exists, so start the bot directly
            threading.Thread(target=self.start_bot_thread,
                             args=(token,), daemon=True).start()
            self.log_message("Bot started.")

    def start_bot_thread(self, token):
        """ Thread wrapper for starting the bot. """
        try:
            import main  # Import main here to avoid circular import issues
            main.run_bot(token)
        except Exception as e:
            self.log_message(f"Error starting bot: {str(e)}")

    def change_bot_status(self, status):
        """ Change the bot's status (online, idle, invisible). """
        try:
            if self.update_bot_status_callback:
                self.update_bot_status_callback(status)
            self.log_message(f"Bot status set to {status}")
        except Exception as e:
            self.log_message(f"Error changing bot status: {e}")

    def update_user_list(self):
        channel_id = self.log_channel_id_entry.get()
        if channel_id:
            try:
                online_users = main.get_online_users_in_channel(channel_id)
                self.user_list.delete(0, tk.END)  # Clear existing list
                for user in online_users:
                    self.user_list.insert(tk.END, user)
            except Exception as e:
                self.log_message(f"Error updating user list: {e}")

    def update_lists_periodically(self):
        self.update_user_list()
        self.update_server_list()
        # Update every 30 seconds
        self.after(30000, self.update_lists_periodically)

    def update_server_list(self):
        try:
            server_data = main.get_server_list_sync()
            self.server_list.delete(0, tk.END)  # Clear existing list
            for server_name, server_id, member_count in server_data:
                self.server_list.insert(
                    tk.END, f"{server_name} (ID: {server_id}, Members: {member_count})")
        except Exception as e:
            self.log_message(f"Error updating server list: {e}")

    def update_gui_status(self, status, guild_count):
        """ Update the GUI with the bot's status and guild count. """
        try:
            # Update GUI elements to reflect bot's status
            # For example, updating a label or text widget with the status and guild count
            self.status_label.config(
                text=f"Status: {status}, Guilds: {guild_count}")
            self.log_message(f"GUI updated: {status}, Guilds: {guild_count}")
        except Exception as e:
            self.log_message(f"Error updating GUI status: {e}")

    def set_channel(self):
        """ Set the channel ID for the bot to enter. """
        channel_id = self.channel_id_entry.get().strip()
        if channel_id:
            try:
                # Check if the channel ID is a valid integer
                channel_id_int = int(channel_id)
                # Call the set_channel function from main.py
                main.set_channel(channel_id)
                self.log_message(f"Channel set to {channel_id}")
            except ValueError:
                # Handle invalid channel ID (not an integer)
                self.log_message(
                    "Invalid channel ID. Please enter a numeric ID.")
            except Exception as e:
                # Handle other exceptions
                self.log_message(f"Error setting channel: {e}")
        else:
            self.log_message("No channel ID entered.")

    def update_bot_status(self, status, server_count=0):
        """ Updates the bot status and server count on the GUI. """
        def _update():
            self.bot_status_label.config(text=f"Bot Status: {status}")
            self.server_count_label.config(
                text=f"Connected Servers: {server_count}")

        self.after(0, _update)

    def view_token(self):
        token = token_manager.load_token()
        messagebox.showinfo("Bot Token", token if token else "No token set.")

    def edit_token(self):
        token = simpledialog.askstring(
            "Edit Token", "Enter your Discord Bot Token:", parent=self)
        if token:
            token_manager.save_token(token)
            self.log_message("Token updated.")
            self.check_and_start_bot()
        else:
            messagebox.showinfo("No Change", "Token was not updated.")

    def save_token(self):
        token = token_manager.load_token()
        if token:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                                     ("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(token)
                self.log_message(f"Token saved to {file_path}")
        else:
            self.log_message("No token to save.")

    def toggle_auto_mod(self):
        # Implement the logic to communicate with the bot
        auto_mod_enabled = False  # Replace with actual state check
        self.log_message("Auto Moderation toggled.")
        self.auto_mod_button.config(
            text="Auto Moderation On" if auto_mod_enabled else "Auto Moderation Off")

    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert('end', message + '\n')
        self.log_area.yview('end')
        self.log_area.config(state='disabled')

    def save_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                                 ("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                log_content = self.log_area.get("1.0", tk.END)
                file.write(log_content)
            self.log_message(f"Log saved to {file_path}")


# Global reference to the GUI instance
gui_instance = None


def update_log(message):
    if gui_instance:
        gui_instance.log_message(message)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def show_splash_screen():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)

    # Get the screen width and height
    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()
    splash_screen_width, splash_screen_height = 800, 400

    # Calculate position x, y
    x = (screen_width - splash_screen_width) // 2
    y = (screen_height - splash_screen_height) // 2
    splash_root.geometry(
        f"{splash_screen_width}x{splash_screen_height}+{x}+{y}")

    # Main frame to hold image
    main_frame = tk.Frame(splash_root, bg="black")
    main_frame.pack(fill="both", expand=True)

    # Load your AI-generated image
    splash_image_path = resource_path('images/splash/dept14.jpg')
    splash_image = Image.open(splash_image_path)

    # Resize the image while maintaining aspect ratio
    img_width, img_height = splash_image.size
    scaling_factor = min(splash_screen_width / img_width,
                         splash_screen_height / img_height)
    new_size = (int(img_width * scaling_factor),
                int(img_height * scaling_factor))
    splash_image = splash_image.resize(new_size, Image.LANCZOS)

    splash_photo = ImageTk.PhotoImage(splash_image)

    # Image label
    image_label = tk.Label(main_frame, image=splash_photo, bg="black")
    image_label.pack(side="top", fill="both", expand=True)

    # Initial transparency
    splash_root.attributes("-alpha", 0)

    # Fade-in effect
    for i in range(0, 101, 5):
        splash_root.attributes("-alpha", i/100)
        splash_root.update()
        time.sleep(0.05)  # Adjust the speed of the fade-in here

    # Close the splash screen after 3000 milliseconds (3 seconds)
    splash_root.after(3000, splash_root.destroy)
    splash_root.mainloop()

    # Keep a reference to the image to prevent garbage collection
    image_label.image = splash_photo


if __name__ == "__main__":
    show_splash_screen()  # Show the splash screen first

    gui = BotGUI()
    event_handlers.setup_handlers(gui)
    if gui.is_gui_initialized():
        gui.mainloop()
    else:
        print("GUI failed to initialize.")
