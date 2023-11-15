import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog, filedialog, Menu, Label, Entry, Button, messagebox
from PIL import Image, ImageTk
import threading
import main  # Import the main module
import token_manager  # Import the token manager
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
    def __init__(self):
        super().__init__()
        self.title("Discord Bot Control Panel")
        self.geometry("700x700")  # Window size controls

        # Black and green color scheme
        self.bg_color = "#000000"  # Black background
        self.text_color = "#00FF00"  # Green text
        self.menu_bg_color = "#003300"  # Dark green for menu background
        self.menu_fg_color = "#00FF00"  # Green for menu text
        self.button_color = "#004d00"  # Slightly lighter green for buttons
        self.button_text_color = "#00FF00"  # Green text for buttons

        self.configure(bg=self.bg_color)

        # Menu Bar
        self.menu_bar = Menu(self, bg=self.menu_bg_color, fg=self.menu_fg_color)
        self.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = Menu(self.menu_bar, tearoff=0, bg=self.menu_bg_color, fg=self.menu_fg_color)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="View Token", command=self.view_token)
        self.file_menu.add_command(label="Edit Token", command=self.edit_token)
        self.file_menu.add_command(label="Save Token", command=self.save_token)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save Logs", command=self.save_log)

        # Bot Control Frame
        self.bot_control_frame = tk.Frame(self, bg=self.bg_color)
        self.bot_control_frame.pack(padx=10, pady=5)
        
        # Bot Status and Server Count Labels
        self.bot_status_label = Label(self.bot_control_frame, text="Bot Status: Unknown", bg=self.bg_color, fg=self.text_color)
        self.bot_status_label.pack(side=tk.LEFT, padx=5)
        self.server_count_label = Label(self.bot_control_frame, text="Connected Servers: 0", bg=self.bg_color, fg=self.text_color)
        self.server_count_label.pack(side=tk.LEFT, padx=5)

        # Bot Status Control
        self.status_var = tk.StringVar(self)
        self.status_options = ['online', 'idle', 'invisible']
        self.status_menu = tk.OptionMenu(self.bot_control_frame, self.status_var, *self.status_options, command=self.change_bot_status)
        self.status_menu.config(bg=self.button_color, fg=self.button_text_color)
        self.status_menu.pack(side=tk.LEFT, padx=5, pady=5)
        
        # New Frame for Channel IDs
        self.channel_id_frame = tk.Frame(self, bg=self.bg_color)
        self.channel_id_frame.pack(padx=10, pady=5)

        # Log Channel ID Entry
        self.log_channel_id_label = Label(self.channel_id_frame, text="Log Channel ID:", bg=self.bg_color, fg=self.text_color)
        self.log_channel_id_label.pack(side=tk.LEFT, padx=5)
        self.log_channel_id_entry = Entry(self.channel_id_frame, bg=self.bg_color, fg=self.text_color)
        self.log_channel_id_entry.pack(side=tk.LEFT, padx=5)

        # Channel ID Entry
        self.channel_id_label = Label(self.channel_id_frame, text="Channel ID:", bg=self.bg_color, fg=self.text_color)
        self.channel_id_label.pack(side=tk.LEFT, padx=5)
        self.channel_id_entry = Entry(self.channel_id_frame, bg=self.bg_color, fg=self.text_color)
        self.channel_id_entry.pack(side=tk.LEFT, padx=5)
        self.set_channel_button = Button(self.channel_id_frame, text="Set Channel", command=self.set_channel, bg=self.button_color, fg=self.button_text_color)
        self.set_channel_button.pack(side=tk.LEFT, padx=5)

        # Create Notebook (Tab Control)
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(expand=1, fill="both")

        # Tab 1: Log Area
        self.log_tab = tk.Frame(self.tab_control, bg=self.bg_color)
        self.tab_control.add(self.log_tab, text='Log')
        self.log_area = scrolledtext.ScrolledText(self.log_tab, state='disabled', wrap='word', bg=self.bg_color, fg=self.text_color)
        self.log_area.pack(padx=10, pady=10, fill='both', expand=True)

        # Tab 2: User and Server List
        self.user_server_tab = tk.Frame(self.tab_control, bg=self.bg_color)
        self.tab_control.add(self.user_server_tab, text='Users & Servers')

        # User List
        self.user_list_label = tk.Label(self.user_server_tab, text="Users", bg=self.bg_color, fg=self.text_color)
        self.user_list_label.pack(pady=(10, 0))
        self.user_list = tk.Listbox(self.user_server_tab, bg=self.bg_color, fg=self.text_color)
        self.user_list.pack(padx=10, pady=5, fill='both', expand=True)
        # Populate the user list here with user details

        # Server List
        self.server_list_label = tk.Label(self.user_server_tab, text="Servers", bg=self.bg_color, fg=self.text_color)
        self.server_list_label.pack(pady=(10, 0))
        self.server_list = tk.Listbox(self.user_server_tab, bg=self.bg_color, fg=self.text_color)
        self.server_list.pack(padx=10, pady=5, fill='both', expand=True)
        # Populate the server list here with server details

        # Button Frame
        self.button_frame = tk.Frame(self, bg=self.bg_color)
        self.button_frame.pack(padx=10, pady=5)

        # Start Bot Button
        self.start_bot_button = tk.Button(self.button_frame, text="Start Bot", command=self.start_bot, bg=self.button_color, fg=self.button_text_color)
        self.start_bot_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Auto Moderation Toggle Button
        self.auto_mod_button = tk.Button(self.button_frame, text="Toggle Auto Moderation", command=self.toggle_auto_mod, bg=self.button_color, fg=self.button_text_color)
        self.auto_mod_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # After setting up all your widgets, call add_tooltips
        self.add_tooltips()
    
    # Add tooltips to widgets
    def add_tooltips(self):
        Tooltip(self.status_menu, "Change the bot's online status.")
        Tooltip(self.log_channel_id_entry, "Enter the ID of the Discord channel for logging.")
        Tooltip(self.channel_id_entry, "Enter the ID of the Discord channel for the bot to operate in.")
        Tooltip(self.set_channel_button, "Set the bot to use the specified channel.")
        Tooltip(self.start_bot_button, "Start the Discord bot.")
        Tooltip(self.auto_mod_button, "Toggle automatic moderation features.")
    
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
        self.after(30000, self.update_lists_periodically)  # Update every 30 seconds

    def update_server_list(self):
        try:
            server_data = main.get_server_list_sync()
            self.server_list.delete(0, tk.END)  # Clear existing list
            for server_name, server_id, member_count in server_data:
                self.server_list.insert(tk.END, f"{server_name} (ID: {server_id}, Members: {member_count})")
        except Exception as e:
            self.log_message(f"Error updating server list: {e}")
        
    def change_bot_status(self, status):
        """ Change the bot's status (online, idle, invisible). """
        try:
            # Call the update_bot_status function from main.py
            main.update_bot_status(status)
            self.log_message(f"Bot status set to {status}")
        except Exception as e:
            # Log any exceptions that occur
            self.log_message(f"Error changing bot status: {e}")

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
                self.log_message("Invalid channel ID. Please enter a numeric ID.")
            except Exception as e:
                # Handle other exceptions
                self.log_message(f"Error setting channel: {e}")
        else:
            self.log_message("No channel ID entered.")
    
    def update_bot_status(self, status, server_count=0):
        """ Updates the bot status and server count on the GUI. """
        def _update():
            self.bot_status_label.config(text=f"Bot Status: {status}")
            self.server_count_label.config(text=f"Connected Servers: {server_count}")

        self.after(0, _update)
    
    def view_token(self):
        token = token_manager.load_token()
        simpledialog.messagebox.showinfo("Bot Token", token if token else "No token found.")

    def edit_token(self):
        token = simpledialog.askstring("Edit Token", "Enter your Discord Bot Token:", parent=self)
        if token:
            token_manager.save_token(token)
            self.log_message("Token updated.")

    def save_token(self):
        token = token_manager.load_token()
        if token:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
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
        self.auto_mod_button.config(text="Auto Moderation On" if auto_mod_enabled else "Auto Moderation Off")

    def start_bot(self):
        token = token_manager.load_token()
        if not token:
            token = simpledialog.askstring("Token", "Enter your Discord Bot Token:", parent=self)
            if token:
                token_manager.save_token(token)
            else:
                messagebox.showerror("Error", "No token provided.")
                return
        log_channel_id = self.log_channel_id_entry.get()
        try:
            threading.Thread(target=main.run_bot, args=(token, log_channel_id), daemon=True).start()
            self.log_message("Bot started.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {e}")

    def log_message(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert('end', message + '\n')
        self.log_area.yview('end')
        self.log_area.config(state='disabled')

    def save_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
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
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def show_splash_screen():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)
    splash_screen_width, splash_screen_height = 800, 400
    splash_root.geometry(f"{splash_screen_width}x{splash_screen_height}+300+200")

    main_frame = tk.Frame(splash_root, bg="black")
    main_frame.pack(fill="both", expand=True)

    splash_image_path = resource_path('images/splash/dept14.jpg')
    splash_image = Image.open(splash_image_path)

    img_width, img_height = splash_image.size
    scaling_factor = min(splash_screen_width / img_width, splash_screen_height / img_height)
    new_size = (int(img_width * scaling_factor), int(img_height * scaling_factor))
    splash_image = splash_image.resize(new_size, Image.Resampling.LANCZOS)

    splash_photo = ImageTk.PhotoImage(splash_image)

    image_label = tk.Label(main_frame, image=splash_photo, bg="black")
    image_label.pack(fill="both", expand=True)

    # Initial transparency
    splash_root.attributes("-alpha", 0)

    # Fade-in effect
    for i in range(0, 101, 5):
        splash_root.attributes("-alpha", i/100)
        splash_root.update()
        time.sleep(0.05)  # Adjust the speed of the fade-in here

    splash_root.after(3000, splash_root.destroy)
    splash_root.mainloop()

    image_label.image = splash_photo

if __name__ == "__main__":
    show_splash_screen()  # Show the splash screen first
    gui = BotGUI()
    gui_instance = gui
    gui.mainloop()
    