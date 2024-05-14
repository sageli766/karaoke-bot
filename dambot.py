import discord
from discord.ext import commands
import sys
import pyautogui
import damvision

from karaoke import Karaoke
from damcontrol import *
import session

from searchmenu import SearchMenu
from controlmenu import ControlMenu
from queuemenu import QueueMenu

client_id = sys.argv[1]
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

screen_width, screen_height = pyautogui.size()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# test bot command
@bot.command()
async def parrot(ctx, *args):
    for arg in args:
        await ctx.send(f'{arg}')

# manual reset command in case something goes poo poo
@bot.command()
async def r(ctx, *args):
    click_button(Button.TOP)
    session.set_someone_using(False)
    await ctx.send(f'reset!')

@bot.command()
async def jessie(ctx, name):
    await ctx.send(f'{name} is a 傻逼')

@bot.command()
async def sage(ctx, name):
    await ctx.send(f'{name} 是世界上最傻的傻逼')

# starts a karaoke session
@bot.command()
async def kstart(ctx, *args):
    if not args:
        embed=discord.Embed()
        embed.add_field(name='Error', value=f'Please enter a title for the karaoke session.')
        await ctx.send(embed=embed)
    else:
        title = ' '.join(args)
        session.set_current_session(Karaoke(title))
        logger.debug("session started: " + str(session.get_current_session()))
        embed=discord.Embed()
        embed.add_field(name='New Session', value=f'New karaoke session **{title}** started by {ctx.author.name}.')
        await ctx.send(embed=embed)

# ends the current karaoke session
@bot.command()
async def kend(ctx):
    session.set_current_session(None)
    embed=discord.Embed()
    embed.add_field(name='Success', value=f'Current session **{session.get_current_session().title}** ended.')
    await ctx.send(embed=embed)

# adds a song to the current karaoke session's queue
@bot.command()
async def add(ctx, song_title, key=0):
# async def add(ctx, *args):
    # for song_title in args:
    if session.get_current_session():
        session.get_current_session().add_to_queue(song_title, ctx.author, key)
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
    session.get_current_session().remove_from_queue(pos - 1)
    embed = discord.Embed()
    embed.add_field(name='Success', value='Removed')
    await ctx.send(embed=embed)

# clears the current song queue
@bot.command()
async def clear(ctx):
    session.get_current_session().clear()
    embed=discord.Embed()
    embed.add_field(name='Success', value='Cleared the current queue.')
    await ctx.send(embed=embed)

# search songs
@bot.command()
async def s(ctx, keyword):
    if len(keyword) < 2:
        await ctx.send('Your search cannot be less than 2 characters in length.', delete_after=3)
        return
    if session.someone_using():
        await ctx.send('Someone else is currently using the search feature. ' +
                       'If the previous search is not being used, select "Cancel Search" and try again. Override command: $r', delete_after=10)
        return
    session.set_someone_using(True)
    message = await ctx.send('Searching...')
    num_hits, results = search_keyword(keyword)
    if num_hits == None and results == None:
        await message.edit(content='No results found.', delete_after=3)
        session.set_someone_using(False)
        return
    if num_hits == -1:
        num_hits = max(0, len(results))

    view = SearchMenu(ctx, keyword, num_hits, results, message)
    await view.show_results()

# view queue
@bot.command()
async def q(ctx):
    view = QueueMenu(ctx, None)
    await view.show_results()

# controls
@bot.command()
async def c(ctx):
    if not damvision.playing_song():
        await ctx.send('No song is currently playing.', delete_after=3)
        return
    message = await ctx.send("Controls for: **" + session.get_current_session().get_current_song()[0] + "** by **" + session.get_current_session().get_current_song()[1] + "**")
    view = ControlMenu(ctx, message)
    await message.edit(view=view)
    await message.delete(delay=60)

bot.run(f'{client_id}')
