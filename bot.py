# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
import os
from discord import Game
from discord.ext.commands import Bot

DEBUG = False

BOT_PREFIX = ("$")
import config.py # either comment out this line and uncomment the next line, or make a config.py file that has your token stored in it, either or will work, this is just so i don't goof again and push the file with the token to github :^)
#TOKEN = "BOT SECRET DO NOT PUT ON GITHUB"  # Get at discordapp.com/developers/applications/me

client = Bot(command_prefix=BOT_PREFIX)

@client.command(pass_context=True, aliases=['archive'])
async def log(ctx, *limit:int):
    list_messages = []
    channel = ctx.message.channel 
    calleduser = ctx.message.author
    if DEBUG:
        print(calleduser.id)
    async for message in channel.history(limit=10000):
        if message.author == calleduser:
            list_messages.append(message.content)
    if DEBUG:
        for i in list_messages:
            print(i)
    outfile = '{}/{}.out'.format(channel.id, calleduser.id)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w') as f:
        for i in list_messages:
            f.write(i + '\n')
    print(channel.id)
@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

client.run(TOKEN)
