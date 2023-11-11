import tkinter as tk
from tkinter import scrolledtext, simpledialog, filedialog, Menu, Label
import threading
import main  # Import the main module
import token_manager  # Import the token manager

class BotGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Discord Bot Control Panel")
        self.geometry("650x500")  # Adjusted window size

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

        # Status Frame
        self.status_frame = tk.Frame(self, bg=self.bg_color)
        self.status_frame.pack(padx=10, pady=5, fill='x')

        self.bot_status_label = Label(self.status_frame, text="Bot Status: Disconnected", bg=self.bg_color, fg=self.text_color)
        self.bot_status_label.pack(side=tk.LEFT, padx=5)

        self.server_count_label = Label(self.status_frame, text="Connected Servers: 0", bg=self.bg_color, fg=self.text_color)
        self.server_count_label.pack(side=tk.LEFT, padx=5)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(self, state='disabled', wrap='word', bg=self.bg_color, fg=self.text_color)
        self.log_area.pack(padx=10, pady=10, fill='both', expand=True)

        # Button Frame
        self.button_frame = tk.Frame(self, bg=self.bg_color)
        self.button_frame.pack(padx=10, pady=5)

        # Start Bot Button
        self.start_bot_button = tk.Button(self.button_frame, text="Start Bot", command=self.start_bot, bg=self.button_color, fg=self.button_text_color)
        self.start_bot_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Auto Moderation Toggle Button
        self.auto_mod_button = tk.Button(self.button_frame, text="Toggle Auto Moderation", command=self.toggle_auto_mod, bg=self.button_color, fg=self.button_text_color)
        self.auto_mod_button.pack(side=tk.LEFT, padx=5, pady=5)
    
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
        # Logic to send a command to the bot to toggle auto moderation
        # This should communicate with the bot and change the state of auto moderation
        self.log_message("Auto Moderation toggled.")
        # Update button text based on new state
        # Example: self.auto_mod_button.config(text="Auto Moderation On" if auto_mod_enabled else "Auto Moderation Off")

    def start_bot(self):
        token = token_manager.load_token()
        if not token:
            token = simpledialog.askstring("Token", "Enter your Discord Bot Token:", parent=self)
            if token:
                token_manager.save_token(token)
            else:
                self.log_message("No token provided. Exiting.")
                return
        threading.Thread(target=main.run_bot, args=(self,), daemon=True).start()
        self.log_message("Bot started.")

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

if __name__ == "__main__":
    gui = BotGUI()
    gui_instance = gui
    gui.mainloop()
    
