import discord
from discord.ext import commands

async def on_ready(bot):
    print(f'{bot.user.name} has connected to Discord!')

async def on_member_join(member):
    print(f'{member.name} has joined the server.')

async def on_member_remove(member):
    print(f'{member.name} has left the server.')

async def on_message_delete(message):
    print(f'A message by {message.author.display_name} was deleted.')

async def on_message_edit(before, after):
    if before.content != after.content:
        print(f'Message by {before.author.display_name} was edited.')

def setup(bot):
    @bot.event
    async def on_ready():
        await on_ready(bot)

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
