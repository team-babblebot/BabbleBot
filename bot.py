# Work with Python 3.6
import os
from discord.ext.commands import Bot
import markov
import discord
import re

from config import DEBUG, TOKEN, PREFIX as BOT_PREFIX, BOT_PING_CREDITS, ALLOW_SENTENCE_MENTIONS
import boomer as boom

MESSAGES_DIRECTORY = "messages/"

client = Bot(command_prefix=BOT_PREFIX)
client.remove_command('help')

@client.command(aliases=['b'])
async def babble(ctx, arg = [], limit: int=10000):
    sentence = await gen_sentence(ctx, arg, limit)
    await send_markov_message(ctx, arg, sentence)


@client.command(aliases=['fb'])
async def boomer(ctx, arg=[], limit: int=10000):
    sentence = await gen_sentence(ctx, arg, limit)
    sentence = boom.add_pre_suf(sentence)
    sentence = boom.add_elipses(sentence)
    sentence = boom.boomer_caps(sentence)
    await send_markov_message(ctx, arg, sentence)

@client.command(pass_context=True, aliases=['r'])
async def relog(ctx, arg = [], *limit:int):
    message = ctx.message
    if arg == []:
        called_user = message.author
    else:
        called_user = message.mentions[0]
    channel = message.channel
    if DEBUG:
        print(called_user.id)
    list_messages = await gen_files(ctx, called_user)
    if DEBUG:
        for i in list_messages:
            print(i)
    outfile = f'{MESSAGES_DIRECTORY}{message.guild.id}/{called_user.id}.out'
    os.remove(outfile)
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w') as f:
        for i in list_messages:
            f.write(i + '\n')
    if DEBUG: print(channel.id)
    await channel.send(f"Relog complete for {called_user.name}!")

@client.command(pass_context=True, aliases=['h'])
async def help(ctx):
    await ctx.message.channel.send(
        f"""
        :book:**Available commands**:book:
__{BOT_PREFIX}help__ — *alias: h* – displays this text
__{BOT_PREFIX}babble__ – *alias: b* – generate a sentence based 
    on your message history. Optionally, add a user's nickname/username
    in plaintext (not a mention) to have the bot instead use their message history.
    Respective examples: `{BOT_PREFIX}babble`, `{BOT_PREFIX}b Xyzzy` .
__{BOT_PREFIX}boomer__ – *alias: fb* – `{BOT_PREFIX}babble` but styled like a
    comment from that one social media site.
__{BOT_PREFIX}relog__ – *alias: r* – Updates a user's message log bot-side. Called and takes
    arguments just like `{BOT_PREFIX}babble` ."""
    )

@client.command(pass_context=True)
async def test(ctx, arg):
    channel = ctx.message.channel 
    server = ctx.message.guild
    await channel.send(server.get_member(int(arg)))

async def gen_files(ctx, called_user):
    guild = ctx.message.guild
    list_messages = []
    for guild_channel in guild.channels:
        if DEBUG:
            print(f'Channel: {guild_channel.type}')
            print(f'Channel: {type(guild_channel.type)}')
        if (str(guild_channel.type) == 'text') and (guild_channel.permissions_for(guild.me).read_messages):
            async for guild_message in guild_channel.history(limit=100):
                if guild_message.author == called_user:
                    list_messages.append(guild_message.content)
    return list_messages

async def gen_sentence(ctx, arg, limit):
    list_messages = []
    channel = ctx.message.channel
    guild = ctx.message.guild
    called_user = ctx.message.author if not arg else ctx.message.mentions[0]

    outfile = f'{MESSAGES_DIRECTORY}{guild.id}/{called_user.id}.out'
    if os.path.exists(outfile) == False:
        if DEBUG:
            print(called_user.id)

        list_messages = await gen_files(ctx, called_user)

        if DEBUG:
            for msg in list_messages:
                print(f'message: {msg}')

        os.makedirs(os.path.dirname(outfile), exist_ok=True)
        with open(outfile, 'w+') as f:
            for msg in list_messages:
                f.write(msg + '\n')
        if DEBUG: print(channel.id)
        if DEBUG: print("hey i'm makin a file here")

    with open(outfile, 'r') as words:
        if DEBUG: print("1")
        corpus = ''
        words = words.readlines()
        for x in words:
            corpus += x
        if DEBUG: print("2")
        sentence = markov.gen_sentence(markov.create_markov_model(corpus))
        if DEBUG: print("3")
        if not ALLOW_SENTENCE_MENTIONS:
            match = re.search(r'<@!?(\d+)>', sentence)
            if match:
                for user_id in match.groups():
                    user_id = int(user_id)
                    print(user_id)
                    pinged_user = guild.get_member(user_id)
                    if pinged_user.nick is None:
                        sentence = re.sub(r'<@!?\d+>', pinged_user.name, sentence)
                    else:
                        sentence = re.sub(r'<@!?\d+>', pinged_user.nick, sentence)
        return sentence

async def send_markov_message(ctx, arg, sentence):
    guild = ctx.message.guild
    if ctx.message.channel.permissions_for(guild.me).send_messages:
        if not arg:
            await ctx.send(sentence)
        else:
            if BOT_PING_CREDITS:
                await ctx.send("\"" + sentence + "\" -<@!" + str(ctx.message.mentions[0].id) + ">")
            else:
                if ctx.message.mentions[0].nick is None:
                    await ctx.send("\"" + sentence + "\" -" + str(ctx.message.mentions[0].name))
                else:
                    await ctx.send("\"" + sentence + "\" -" + str(ctx.message.mentions[0].nick))

if __name__ == '__main__':
    client.run(TOKEN)
