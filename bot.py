# Work with Python 3.6
import os
from discord.ext.commands import Bot
import markov

DEBUG = False

from config import TOKEN   # either comment out this line and uncomment the next line, or make a config.py file that has your token stored in it, either or will work, this is just so i don't goof again and push the file with the token to github :^)
# TOKEN = "BOT SECRET DO NOT PUT ON GITHUB"  # Get at discordapp.com/developers/applications/me
BOT_PREFIX = ("$")

MESSAGES_DIRECTORY = "messages/"

client = Bot(command_prefix=BOT_PREFIX)

@client.command(pass_context=True)
async def babble(ctx, limit: int=10000):
    list_messages = []
    channel = ctx.message.channel 
    calleduser = ctx.message.author

    
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

    with open(outfile, 'r') as words:
        corpus = ''
        words = words.readlines()
        for x in words:
            corpus += x
        sentence = markov.gen_sentence(markov.create_markov_model(corpus))
        await channel.send(sentence)

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

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)


if __name__ == '__main__':
    client.run(TOKEN)
