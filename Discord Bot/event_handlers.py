import discord
from discord.ext import commands
from bot_logging import log_message, log_exception

async def on_ready(bot):
    try:
        log_message(f'{bot.user.name} has connected to Discord!')
        await bot.change_presence(status=discord.Status.online, activity=discord.Game("Type !help"))
        gui_instance.update_bot_status("Connected", len(bot.guilds))
    except Exception as e:
        log_exception(e)

async def on_member_join(member):
    try:
        channel = member.guild.system_channel
        if channel:
            await channel.send(f'Welcome {member.mention} to {member.guild.name}!')
        log_message(f'{member.name} has joined the server.')
    except Exception as e:
        log_exception(e)

async def on_member_remove(member):
    try:
        channel = member.guild.system_channel
        if channel:
            await channel.send(f'Goodbye {member.mention} from {member.guild.name}.')
        log_message(f'{member.name} has left the server.')
    except Exception as e:
        log_exception(e)

async def on_message_delete(message):
    try:
        log_message(f'A message by {message.author.display_name} was deleted.')
    except Exception as e:
        log_exception(e)

async def on_message_edit(before, after):
    try:
        if before.content != after.content:
            log_message(f'Message by {before.author.display_name} was edited.')
    except Exception as e:
        log_exception(e)

def setup(bot):
    @bot.event
    async def on_member_join(member):
        await on_member_join(member)

    @bot.event
    async def on_member_remove(member):
        await on_member_remove(member)

    @bot.event
    async def on_message_delete(message):
        await on_message_delete(message)

    @bot.event
    async def on_message_edit(before, after):
        await on_message_edit(before, after)

    @bot.event
    async def on_ready():
        await on_ready(bot)
