import discord
import os
import sys
import random
import aiohttp
from bs4 import BeautifulSoup
import datetime
import asyncio
from discord.ext import commands
import requests
import json
from bot_logging import log_message, log_exception  # Import logging functions

# Global dictionary to store auto-moderation state for each server
auto_mod_states = {}

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def convert_to_uwu(text):
    uwu_text = text
    # Replace 'r' and 'l' with 'w'
    uwu_text = uwu_text.replace("r", "w").replace("l", "w")
    # Replace 'R' and 'L' with 'W'
    uwu_text = uwu_text.replace("R", "W").replace("L", "W")
    # Replace 'th' with 'd' or 'f'
    uwu_text = uwu_text.replace("th", random.choice(["d", "f"]))
    # Add uwu faces at the end of sentences
    uwu_text = '. '.join(sentence + random.choice([" uwu", " owo", ""]) for sentence in uwu_text.split('. '))
    # Randomly apply transformations for a more natural feel
    if random.choice([True, False]):
        uwu_text = uwu_text.replace("n", "ny")
    return uwu_text

async def fetch_news(url="https://www.ign.com/pc", item_selector='div.content-item', title_selector='a', max_items=5, timeout=10):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    news_items = soup.select(item_selector)
                    news_titles = [item.select_one(title_selector).get_text(strip=True) for item in news_items if item.select_one(title_selector)]
                    await log_message(f"Fetched {len(news_titles)} news titles successfully.", logging.INFO)
                    return news_titles[:max_items]
                else:
                    await log_message(f"Failed to fetch news: HTTP {response.status}", logging.ERROR)
                    return []
    except Exception as e:
        await log_exception(e)
        return []

async def fetch_ducat_prices():
    url = "https://warframe.market/tools/ducats"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            # Find all elements with the class 'ducats--KbUMm' which seems to be the container for each item
            items = soup.find_all('div', class_='ducats--KbUMm')

            ducat_data = {}
            for item in items:
                # Extract the item name
                name_element = item.find('div', class_='ducats__itemName--N28_d')
                name = name_element.find('span', class_='ducats__itemName-text--KdajT').text.strip() if name_element else 'Unknown Item'

                # Extract the ducat value
                ducat_element = item.find('div', class_='ducats__ducats--z_pID')
                ducat_value = ducat_element.find('span').text.strip() if ducat_element else 'Unknown Value'

                ducat_data[name] = ducat_value

            return ducat_data
        
async def fetch_weather(city):
    # Replace with your weather API URL and key
    url = f"http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q={city}"
    response = requests.get(url)
    return response.json()

async def fetch_quote():
    response = requests.get("https://api.quotable.io/random")
    return response.json()

async def fetch_meme():
    response = requests.get("https://meme-api.herokuapp.com/gimme")
    return response.json()

# Function to register all commands to the bot
def register_commands(bot):
    @bot.command(name='uwu')
    async def uwu_command(ctx, *, message: str):
        uwu_message = convert_to_uwu(message)
        await ctx.send(uwu_message)
    
    @bot.command(name='roll', help='Rolls a dice in NdN format.')
    async def roll(ctx, dice: str):
        """Rolls a dice using NdN format. For example, '2d6' rolls two 6-sided dice."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @bot.command(name='character', help='Generates a detailed random D&D character.')
    async def character(ctx):
        """Generates a detailed random D&D character."""
        races = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Gnome", "Half-Elf", "Half-Orc", "Tiefling"]
        classes = ["Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard"]
        backgrounds = ["Acolyte", "Criminal", "Folk Hero", "Noble", "Sage", "Soldier"]
        alignments = ["Lawful Good", "Neutral Good", "Chaotic Good", "Lawful Neutral", "True Neutral", "Chaotic Neutral", "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
        traits = [
            "Always has a plan for when things go wrong",
            "Is incredibly slow to trust",
            "Is always polite and respectful",
            "Has a secret fear of the dark",
            "Always wants to know how things work",
            "Loves a good insult, even one directed at them",
            "Is suspicious of strangers",
            "Has a heart of gold, but never lets it show",
            "Is always calm, no matter what the situation",
            "Has a habit of talking to themselves"
        ]

        race = random.choice(races)
        cls = random.choice(classes)
        background = random.choice(backgrounds)
        alignment = random.choice(alignments)
        trait = random.choice(traits)

        character_profile = (
            f"**Character Profile**\n"
            f"Race: {race}\n"
            f"Class: {cls}\n"
            f"Background: {background}\n"
            f"Alignment: {alignment}\n"
            f"Unique Trait: {trait}"
        )

        # Path to the images directory
        images_path = resource_path("images/DnD")

        # Mapping races to their respective image filenames
        race_images = {
            "Human": "Human.jpg",
            "Elf": "Elf.jpg",
            "Dwarf": "Dwarf.jpg",
            "Halfling": "Halfling.jpg",
            "Dragonborn": "Dragonborn.jpg",
            "Gnome": "Gnome.jpg",
            "Half-Elf": "Half-Elf.jpg",
            "Half-Orc": "Half-Orc.jpg",
            "Tiefling": "Tiefling.jpg"
        }

        # Select the image based on the chosen race
        image_filename = race_images.get(race, "default.jpg")  # default.jpg is a fallback image
        image_path = os.path.join(images_path, image_filename)

        # Create a Discord file object from the image
        file = discord.File(image_path, filename=image_filename)

        # Send the character profile along with the image
        await ctx.send(character_profile, file=file)

    @bot.command(name='schedule', help='Schedules a game session.')
    async def schedule(ctx, date: str, time: str):
        """Schedules a game session."""
        # Parse the date and time
        try:
            scheduled_time = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            await ctx.send("Invalid date format. Please use YYYY-MM-DD HH:MM format.")
            return

        # Check if the scheduled time is in the future
        if scheduled_time < datetime.datetime.now():
            await ctx.send("You cannot schedule a session in the past. Please choose a future time.")
            return

        # Confirm the scheduled session
        confirmation_message = await ctx.send(f"Game session scheduled on {scheduled_time.strftime('%Y-%m-%d at %H:%M')}. React with 👍 to confirm.")
        await confirmation_message.add_reaction("👍")

        # Wait for confirmation reaction
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍' and reaction.message.id == confirmation_message.id

        try:
            await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Session scheduling timed out.")
        else:
            await ctx.send(f"Session confirmed for {scheduled_time.strftime('%Y-%m-%d at %H:%M')}.")

        # Additional functionality like reminders or calendar integration can be added here
        # ...

    @bot.command(name='poll', help='Creates a simple yes or no poll.')
    async def poll(ctx, *, question):
        """Creates a simple yes or no poll."""
        message = await ctx.send(f'Poll: {question}')
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    @bot.command(name='ducats', help='Shows ducat values for items.')
    async def ducats(ctx):
        try:
            ducat_data = await fetch_ducat_prices()
            message = "\n".join([f"{item}: {price}" for item, price in ducat_data.items()])
            await ctx.send(f"Ducat Prices:\n{message}")
        except Exception as e:
            await ctx.send(f"Error fetching ducat prices: {e}")

    @bot.command(name='news', help='Provides the latest gaming news.')
    async def news(ctx):
        """Provides the latest gaming news."""
        try:
            news_titles = await fetch_news()
            news_message = "\n".join(news_titles) if news_titles else "No news found."
            await ctx.send(f"Latest gaming news:\n{news_message}")
        except Exception as e:
            await ctx.send(f"Error fetching news: {e}")
    
    @bot.command(name='toggleAutoMod', help='Toggles auto moderation on or off.')
    @commands.has_permissions(manage_guild=True)
    async def toggle_auto_mod(ctx):
        """Toggles auto moderation on or off."""
        guild_id = ctx.guild.id

        # Toggle the auto-moderation state
        if guild_id in auto_mod_states:
            auto_mod_states[guild_id] = not auto_mod_states[guild_id]
        else:
            auto_mod_states[guild_id] = True  # Enable auto-moderation if it's the first time

        # Respond with the new state
        state = "enabled" if auto_mod_states[guild_id] else "disabled"
        await ctx.send(f"Auto-moderation is now {state}.")

    @bot.command(name='weather', help='Shows current weather for a city.')
    async def weather(ctx, *, city: str):
        """Shows current weather for a specified city."""
        weather_data = await fetch_weather(city)
        if 'error' in weather_data:
            await ctx.send("Couldn't fetch weather data. Please try again.")
        else:
            description = weather_data['current']['condition']['text']
            temperature = weather_data['current']['temp_c']
            await ctx.send(f"Weather in {city}: {description}, {temperature}°C")

    @bot.command(name='quote', help='Displays an inspirational quote.')
    async def quote(ctx):
        """Displays an inspirational quote of the day."""
        quote_data = await fetch_quote()
        await ctx.send(f"{quote_data['content']} - {quote_data['author']}")

    @bot.command(name='serverinfo', help='Displays information about the server.')
    async def serverinfo(ctx):
        """Displays information about the server."""
        server = ctx.guild
        num_text_channels = len(server.text_channels)
        num_voice_channels = len(server.voice_channels)
        num_members = server.member_count
        server_description = server.description
        embed = discord.Embed(title=f"{server.name} Information", description=server_description or "No description")
        embed.add_field(name="Member Count", value=num_members)
        embed.add_field(name="Text Channels", value=num_text_channels)
        embed.add_field(name="Voice Channels", value=num_voice_channels)
        await ctx.send(embed=embed)

    @bot.command(name='userinfo', help='Displays information about a user.')
    async def userinfo(ctx, member: discord.Member):
        """Displays information about a user."""
        roles = [role.name for role in member.roles]
        embed = discord.Embed(title=f"{member.name}'s Information", description=f"Roles: {', '.join(roles)}")
        embed.add_field(name="Joined at", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        embed.add_field(name="Created at", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        await ctx.send(embed=embed)

    @bot.command(name='reminder', help='Sets a reminder.')
    async def reminder(ctx, time: int, *, reminder: str):
        """Sets a reminder for the user."""
        await ctx.send(f"Reminder set for {time} minutes. I will remind you about: {reminder}")
        await asyncio.sleep(time * 60)
        await ctx.send(f"Hey {ctx.author.mention}, remember to: {reminder}")

    @bot.command(name='meme', help='Displays a random meme.')
    async def meme(ctx):
        """Fetches and displays a random meme."""
        meme_data = await fetch_meme()
        embed = discord.Embed(title=meme_data['title'])
        embed.set_image(url=meme_data['url'])
        await ctx.send(embed=embed)

    # Add more commands as needed
    # ...

# Remember to add the register_commands function to your bot in the main.py file
