import discord
from discord.ext import commands
from karaoke import Karaoke
from damcontrol import *
import sys
import pyautogui

client_id = sys.argv[1]
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

current_session = None

screen_width, screen_height = pyautogui.size()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# test bot command
@bot.command()
async def parrot(ctx, *args):
    for arg in args:
        await ctx.send(f'{arg}')

@bot.command()
async def jessie(ctx, name):
    await ctx.send(f'{name} is a 傻逼')

@bot.command()
async def sage(ctx, name):
    await ctx.send(f'{name} 是世界上最傻的傻逼')

# starts a karaoke session
@bot.command()
async def kstart(ctx, *args):
    global current_session
    if not args:
        embed=discord.Embed()
        embed.add_field(name='Error', value=f'Please enter a title for the karaoke session.')
        await ctx.send(embed=embed)
    else:
        title = ' '.join(args)
        current_session = Karaoke(title)
        embed=discord.Embed()
        embed.add_field(name='New Session', value=f'New karaoke session **{title}** started by {ctx.author.name}.')
        await ctx.send(embed=embed)

# ends the current karaoke session
@bot.command()
async def kend(ctx):
    global current_session
    current_session = None
    embed=discord.Embed()
    embed.add_field(name='Success', value=f'Current session **{current_session.title}** ended.')
    await ctx.send(embed=embed)

# adds a song to the current karaoke session's queue
@bot.command()
async def add(ctx, song_title, key=0):
# async def add(ctx, *args):
    global current_session
    # for song_title in args:
    if current_session:
        current_session.add_to_queue(song_title, ctx.author, key)
        if key == 0:
            embed = discord.Embed()
            embed.add_field(name='Success', value=f'Added **{song_title}** to the queue.')
            await ctx.send(embed=embed)
        else:
            keytext = '+' + str(key) if key > 0 else key
            embed = discord.Embed()
            embed.add_field(name='Success', value=f'Added **{song_title}** with key **{keytext}** to the queue.')
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed()
        embed.add_field(name='Error', value='Start a karaoke session to add songs.')
        await ctx.send(embed=embed)

# removes a song from the karaoke session's queue from a specified position (1-indexed)
@bot.command()
async def remove(ctx, pos):
    global current_session
    current_session.remove_from_queue(pos - 1)
    embed = discord.Embed()
    embed.add_field(name='Success', value='Removed')
    await ctx.send(embed=embed)

# clears the current song queue
@bot.command()
async def clear(ctx):
    global current_session
    current_session.clear()
    embed=discord.Embed()
    embed.add_field(name='Success', value='Cleared the current queue.')
    await ctx.send(embed=embed)

# gives a list of the current queue
@bot.command()
async def getqueue(ctx):
    global current_session
    if not current_session:
        embed = discord.Embed()
        embed.add_field(name='Error', value='Please queue at least one song to view.')
        await ctx.send(embed=embed)
    queuelen = len(current_session.queue)
    page = 1
    pagemax = queuelen // 5 + 1

    queue_list = discord.Embed(
        title='Current queue:',
        color=discord.Color.blue()
    )

    def update_queue(pg):
        global current_session

        new_embed = discord.Embed(
            title='Current queue:',
            color=discord.Color.blue()
        )

        new_embed.set_footer(text=f'Page {pg} of {pagemax}')

        start_index = (pg - 1) * 5
        end_index = min(pg * 5, len(current_session.queue))

        for i in range(start_index, end_index):
            song, user = current_session.queue[i]
            new_embed.add_field(name=f'{song}', value=f'{user}', inline=False)

        return new_embed


    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']

    # initial page
    queue_list = await ctx.send(embed=update_queue(page))
    
    if page > 1:
        await queue_list.add_reaction('⬅️')
    if page < pagemax:
        await queue_list.add_reaction('➡️')

    try:
        while True:
            reaction, _ = await bot.wait_for('reaction_add', timeout=30, check=check)
            if str(reaction.emoji) == '➡️' and page < pagemax:
                page += 1
                new_embed = update_queue(page)
                await queue_list.edit(embed=new_embed)
                await queue_list.remove_reaction('➡️', ctx.author)
                if page == pagemax:
                    await queue_list.remove_reaction('➡️', bot.user)
                if page - 1 == 1:
                    await queue_list.remove_reaction('➡️', bot.user)
                    await queue_list.add_reaction('⬅️')
                    await queue_list.add_reaction('➡️')

            if str(reaction.emoji) == '⬅️' and page > 1:
                page -= 1
                new_embed = update_queue(page)
                await queue_list.edit(embed=new_embed)
                await queue_list.remove_reaction('⬅️', ctx.author)
                if page == 1:
                    await queue_list.remove_reaction('⬅️', bot.user)
                if page + 1 == pagemax:
                    await queue_list.remove_reaction('⬅️', bot.user)
                    await queue_list.add_reaction('⬅️')
                    await queue_list.add_reaction('➡️')
    except:
        pass

@bot.command()
async def next(ctx):
    global current_session
    if not current_session.queue:
        embed = discord.Embed()
        embed.add_field(name='Error', value='Please have at least one song queued.')
        await ctx.send(embed=embed)
    elif current_session:
        curr_song, user, key = current_session.queue[0]
        queue(to_romaji(curr_song), key)
        current_session.remove_from_queue(0)
        embed = discord.Embed()
        embed.add_field(name='Success', value=f'Queueing {curr_song} requested by {user}.')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed()
        embed.add_field(name='Error', value='Please start a karaoke session and input at least one song.')
        await ctx.send(embed=embed)

@bot.command()
async def controls(ctx):
    panel = discord.Embed()
    panel.add_field(name='Control Panel', value='Control the current song by reacting to the emojis below. This panel will stay active for one minute.')

    ctrl_emojis = ['🛑', '⏯️', '🔄', '⬆️', '⬇️']

    def check(reaction, user):
        return str(reaction.emoji) in ctrl_emojis

    await ctx.send(embed=panel)
    for emoji in ctrl_emojis:
        await panel.add_reaction(emoji)

    try:
        while True:
            reaction, _ = await bot.wait_for('reaction_add', timeout=120, check=check)
            if str(reaction.emoji) == '🛑':
                await panel.remove_reaction('🛑', ctx.author)
                cancel()
            elif str(reaction.emoji) == '⏯️':
                await panel.remove_reaction('⏯️', ctx.author)
                pause()
            elif str(reaction.emoji) == '🔄':
                await panel.remove_reaction('🔄', ctx.author)
                restart()
            elif str(reaction.emoji) == '⬆️':
                await panel.remove_reaction('⬆️', ctx.author)
                keyup()
            elif str(reaction.emoji) == '⬇️':
                await panel.remove_reaction('⬇️', ctx.author)
                keydown()
    except:
        pass

bot.run(f'{client_id}')