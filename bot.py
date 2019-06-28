# Work with Python 3.6
import os
from discord.ext.commands import Bot
import markov
import discord
import re

from config import DEBUG, TOKEN, PREFIX as BOT_PREFIX, BOT_PING_CREDITS, ALLOW_SENTENCE_MENTIONS

MESSAGES_DIRECTORY = "messages/"

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.command(pass_context=True, aliases=['b'])
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

    with open(outfile, 'r') as words:
        corpus = ''
        words = words.readlines()
        for x in words:
            corpus += x
        sentence = markov.gen_sentence(markov.create_markov_model(corpus))

        if not ALLOW_SENTENCE_MENTIONS:
            match = re.search(r'<@!?(\d+)>', sentence)
            print(f'SENTENCE: {sentence}')
            print(f'match: {match}')
            if match:
                for user_id in match.groups():
                    user_id = int(user_id)
                    pinged_user = server.get_member(user_id)
                    if pinged_user.nick == None:
                        sentence = re.sub(r'<@!?\d+>', pinged_user.name, sentence)
                    else:
                        sentence = re.sub(r'<@!?\d+>', pinged_user.nick, sentence)

        if original:
            await channel.send(sentence)
        else:
            if BOT_PING_CREDITS:
                await channel.send("\"" + sentence + "\" -<@!" + str(ctx.message.mentions[0].id) + ">")
            else:
                if ctx.message.mentions[0].nick == None:
                    await channel.send("\"" + sentence + "\" -" + str(ctx.message.mentions[0].name))
                else:
                    await channel.send("\"" + sentence + "\" -" + str(ctx.message.mentions[0].nick))

@client.command(pass_context=True, aliases=['r'])
async def relog(ctx, arg = [], *limit:int):
    list_messages = []
    if arg == []:
        called_user = ctx.message.author
    else:
        called_user = ctx.message.mentions[0]
    channel = ctx.message.channel
    if DEBUG:
        print(called_user.id)
    async for message in channel.history(limit=10000):
        if message.author == called_user:
            list_messages.append(message.content)
    if DEBUG:
        for i in list_messages:
            print(i)
    outfile = f'{MESSAGES_DIRECTORY}{channel.id}/{called_user.id}.out'
    os.remove(outfile)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w') as f:
        for i in list_messages:
            f.write(i + '\n')
    if DEBUG: print(channel.id)
    await channel.send(f"Relog complete for {called_user.name}!")

@client.command(pass_context=True, aliases=['h'])
async def help(ctx, limit: int=10000):
    await ctx.message.channel.send(
        f"""
        :book:**Available commands**:book:
__{BOT_PREFIX}help__ — *alias: h* – displays this text
__{BOT_PREFIX}babble__ – *alias: b* – generate a sentence based 
    on your message history. Optionally, add a user's nickname/username
    in plaintext (not a mention) to have the bot instead use their message history.
    Respective examples: `{BOT_PREFIX}babble`, `{BOT_PREFIX}b Xyzzy` .
__{BOT_PREFIX}relog__ – *alias: r* – Updates a user's message log bot-side. Called and takes
    arguments just like `{BOT_PREFIX}babble` ."""
    )

@client.command(pass_context=True)
async def test(ctx, arg):
    channel = ctx.message.channel 
    server = ctx.message.guild
    await channel.send(server.get_member(int(arg)))

if __name__ == '__main__':
    client.run(TOKEN)
