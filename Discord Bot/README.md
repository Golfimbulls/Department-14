# Discord Bot Project

## Description
This project is a Discord bot designed to provide various functionalities for gaming communities. It includes features like dice rolling, character generation for D&D, game session scheduling, polls, game statistics, and the latest gaming news.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher installed on your machine.
- A Discord account and a bot token. [Learn how to create a bot account here](https://discordpy.readthedocs.io/en/stable/discord.html).

## Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/your-username/your-project-name.git
   cd your-project-name
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**
- Windows:
  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```
- macOS/Linux:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Start the Bot**
- Run the bot using the following command:
  ```
  python gui.py
  ```
- This command starts the bot through the GUI interface.

2. **Using the Bot in Discord**
- Invite the bot to your Discord server.
- Use the bot commands in your server. For example, type `!roll 2d6` to roll two six-sided dice.

## Building an Executable
To build an executable version of your bot for easy distribution and execution:

1. **Install PyInstaller**
   ```
   pip install pyinstaller
   ```

2. **Prepare the Spec File**
- Modify the `gui.spec` file to include all necessary files and configurations.

3. **Build the Executable Using the Spec File**
- Navigate to your project directory.
- Run the following command:
  ```
  pyinstaller gui.spec
  ```
- This command includes the `requests` module as a hidden import, ensuring it's packaged with the executable.
- This will create a `dist` folder in your project directory containing the `gui.exe` file.

3. **Run the Executable**
- You can now run your bot using the executable file in the `dist` folder.

## Features
- Dice rolling with `!roll` command.
- Random D&D character generation with `!character` command.
- Game session scheduling with `!schedule` command.
- Simple yes/no polls with `!poll` command.
- Game statistics display (specific to Warframe) with `!gamestats` command.
- Latest gaming news with `!news` command.
- Auto moderation toggle with `!toggleAutoMod` command (requires manage server permissions).

## Contributing
Contributions to this project are welcome. Please follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`.
4. Push to the original branch: `git push origin <project_name>/<location>`.
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## License
This project is licensed under the [MIT License](LICENSE).

## Contact
If you have any questions or want to reach out, contact me at `<your_email>`.

## Acknowledgments
- Thanks to everyone who has contributed to this project.
- Special thanks to [OpenAI](https://openai.com/) for the language model assistance.
