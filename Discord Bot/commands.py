import discord
import os
import random
import aiohttp
from bs4 import BeautifulSoup
import datetime
import asyncio
om discord.ext import commands  # Import the correct module

async def fetch_news():
    url = "https://www.ign.com/pc"  # Example URL, replace with your preferred news source
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            news_items = soup.find_all('div', class_='content-item')  # Adjust this according to the website's HTML structure
            news_titles = [item.find('a').get_text(strip=True) for item in news_items if item.find('a')]
            return news_titles[:5]  # Return the top 5 news titles

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

# Function to register all commands to the bot
def register_commands(bot):
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
        images_path = "images/DnD"

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
@commands.has_permissions(manage_guild=True)  # Use the correct decorator
async def toggle_auto_mod(ctx):
    # Logic to toggle auto moderation state
    # Update state in storage
    # Respond with the new state
    pass
   

# Remember to add the register_commands function to your bot in the main.py file
