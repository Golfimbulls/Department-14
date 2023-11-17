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

import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, filedialog, Menu, Label, Entry, Button, messagebox
from PIL import Image, ImageTk
import threading
import token_manager  # Import the token manager
import event_handlers  # Import event handlers
import sys
import os
import time


class Tooltip:
    """
    Create a tooltip for a given widget.
    """

    def __init__(self, widget, text):
        self.waittime = 500     # Milliseconds
        self.wraplength = 180   # Pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


class BotGUI(tk.Tk):
    def __init__(self, update_bot_status_callback=None):
        super().__init__()
        self.title("Discord Bot Control Panel")
        self.geometry("700x700")

        # Define the background color attribute
        self.bg_color = "#000000"  # Black background

        self.configure(bg=self.bg_color)  # Use the bg_color attribute
        self.update_bot_status_callback = update_bot_status_callback

        self.setup_menu_bar()
        self.setup_frames_and_panels()
        self.add_tooltips()
        self.initialized = True

    def setup_menu_bar(self):
        menu_bar = Menu(self, bg="#003300", fg="#00FF00")
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0, bg="#003300", fg="#00FF00")
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="View Token", command=self.view_token)
        file_menu.add_command(label="Edit Token", command=self.edit_token)
        file_menu.add_command(label="Save Token", command=self.save_token)
        file_menu.add_separator()
        file_menu.add_command(label="Save Logs", command=self.save_log)

    def setup_frames_and_panels(self):
        self.setup_bot_control_frame()
        self.setup_command_frame()
        self.setup_notebook()
        self.setup_button_frame()

    def setup_bot_control_frame(self):
        # Bot Control Frame
        self.bot_control_frame = tk.Frame(self, bg="#000000")
        self.bot_control_frame.pack(padx=10, pady=5)

        # Bot Status Label
        self.bot_status_label = Label(
            self.bot_control_frame, text="Bot Status: Unknown", bg="#000000", fg="#00FF00")
        self.bot_status_label.pack(side=tk.LEFT, padx=5)

        # Server Count Label
        self.server_count_label = Label(
            self.bot_control_frame, text="Connected Servers: 0", bg="#000000", fg="#00FF00")
        self.server_count_label.pack(side=tk.LEFT, padx=5)

        # Bot Performance Metrics
        self.performance_label = Label(
            self.bot_control_frame, text="Uptime: 0h 0m 0s, CPU Usage: 0%", bg="#000000", fg="#00FF00")
        self.performance_label.pack(side=tk.LEFT, padx=5)

        # Bot Status Control (Dropdown for status change)
        self.status_var = tk.StringVar(self)
        self.status_options = ['online', 'idle', 'invisible']
        self.status_menu = tk.OptionMenu(
            self.bot_control_frame, self.status_var, *self.status_options, command=self.change_bot_status)
        self.status_menu.config(bg="#004d00", fg="#00FF00")
        self.status_menu.pack(side=tk.LEFT, padx=5, pady=5)

        # Additional widgets can be added here as needed

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

        # Start Bot Button
        self.start_bot_button = tk.Button(
            self.button_frame,
            text="Start Bot",
            command=self.check_and_start_bot,
            bg=self.button_color,
            fg=self.button_text_color
        )
        self.start_bot_button.pack(side=tk.LEFT, padx=5, pady=5)

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
        Tooltip(self.start_bot_button, "Start the Discord bot.")
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
    splash_image = splash_image.resize(new_size, Image.Resampling.LANCZOS)

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
