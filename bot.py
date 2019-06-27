# Work with Python 3.6
import os
from discord.ext.commands import Bot
import markov
import discord
import re

DEBUG = False

from config import TOKEN   # either comment out this line and uncomment the next line, or make a config.py file that has your token stored in it, either or will work, this is just so i don't goof again and push the file with the token to github :^)
from config import BotPingCredits
BOT_PREFIX = ("$")

MESSAGES_DIRECTORY = "messages/"

client = Bot(command_prefix=BOT_PREFIX)

@client.command(pass_context=True)
async def babble(ctx, arg = [], limit: int=10000):
    list_messages = []
    channel = ctx.message.channel 
    server = ctx.message.guild
    if arg == []:
        calleduser = ctx.message.author
        original = True
    else:
        calleduser = ctx.message.mentions[0] 
        original = False
    
    outfile = f'{MESSAGES_DIRECTORY}{channel.id}/{calleduser.id}.out'
    if os.path.exists(outfile) == False:
        if DEBUG:
            print(calleduser.id)

        async for message in channel.history(limit=limit):
            if message.author == calleduser:
                list_messages.append(message.content)

        if DEBUG:
            for msg in list_messages:
                print(msg)

        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        with open(outfile, 'w+') as f:
            for msg in list_messages:
                f.write(msg + '\n')
        if DEBUG: print(channel.id)
        if DEBUG: print("hey i'm makin a file here")
    
    r = re.compile('<@!?(\d+)>')
    with open(outfile, 'r') as words:
        corpus = ''
        words = words.readlines()
        for x in words:
            if r.match(x) is not None:
                pinged_uid = int(re.sub(r'[^\d]', '', x))
                pinged = server.get_member(int(pinged_uid))
                if pinged.nick == None:
                    x = "[" + pinged.name + "]"
                else:
                    x = "[" + pinged.nick + "]"
            corpus += x
        sentence = markov.gen_sentence(markov.create_markov_model(corpus))
        if original:
            await channel.send(sentence)
        else:
            if BotPingCredits:
                await channel.send("\"" + sentence + "\" -<@!" + str(ctx.message.mentions[0].id) + ">")
            else:
                if ctx.message.mentions[0].nick == None:
                    await channel.send("\"" + sentence + "\" -" + str(ctx.message.mentions[0].name))
                else:
                    await channel.send("\"" + sentence + "\" -" + str(ctx.message.mentions[0].nick))

@client.command(pass_context=True, aliases=['archive'])
async def relog(ctx, *limit:int):
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
    outfile = f'{MESSAGES_DIRECTORY}{channel.id}/{calleduser.id}.out'
    os.remove(outfile)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w') as f:
        for i in list_messages:
            f.write(i + '\n')
    if DEBUG: print(channel.id)
    await channel.send("Relog complete!")

@client.command(pass_context=True)
async def test(ctx, arg):
    channel = ctx.message.channel 
    server = ctx.message.guild
    await channel.send(server.get_member(int(arg)))

if __name__ == '__main__':
    client.run(TOKEN)
