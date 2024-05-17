import discord
from discord.ext import tasks
import sys
import pyautogui
import asyncio
from proxy import InterceptRequests
import nest_asyncio
nest_asyncio.apply()

import damapi
from karaoke import Karaoke, get_current_session, set_current_session
from damcontrol import *

from searchmenu import SearchMenu
from controlmenu import ControlMenu
from queuemenu import QueueMenu

client_id = sys.argv[1]
bot = discord.Bot()

servers = ['1239006599633305620', 
           #'1211890173844000820'
           ]

# TODO restart logic, top chart
queued = False

@tasks.loop(seconds=5)
async def start_proxy():
    from mitmproxy.tools.main import mitmdump

    logger.info("Starting proxy...")
    mitmdump(['-s', 'proxy.py', '--quiet'])

@tasks.loop(seconds=2)
async def update_queue():
    global queued
    session = get_current_session()
    if not session: return

    if queued and session.is_new_song_playing():
            queued = False
        
    if  not queued and session.is_results_shown() and session.queue_length() > 0:
        queued = True
        logger.debug("adding next song to queue")
        song = session.remove_from_queue()
        await search_keyword_and_reserve(song[0] + " " + song[1], song[2])
    elif not queued and not session.is_new_song_playing() and session.queue_length() > 0:
        queued = True
        song = session.remove_from_queue()
        logger.debug("adding song to queue")
        await search_keyword_and_reserve(song[0] + " " + song[1], song[2])
    
    # print("new_song_playing: " + str(session.is_new_song_playing()))
    # print("results_shown: " + str(session.is_results_shown()))
    # print("is_first_song: " + str(session.is_first_song()))
    # print("popped: " + str(queued))
    # print(session.queue_length())


@bot.event
async def on_ready():
    start_proxy.start()
    update_queue.start()
    print(f'Logged in as {bot.user}')

@bot.slash_command(guild_ids = servers, name = 'jessie', description='傻逼')
async def jessie(ctx, name):
    await ctx.respond(f'{name} is a 傻逼')

@bot.slash_command(guild_ids = servers, name = 'sage', description='最傻的傻逼')
async def sage(ctx, name):
    await ctx.respond(f'{name} 是世界上最傻的傻逼')

# starts a karaoke session
@bot.slash_command(guild_ids = servers, name = 'start', description='start a new session')
async def start(ctx, name=discord.Option(str, description="Name of the session")):
    # TODO check if session already exists
    global queued, current_song_playing
    queued = False
    current_song_playing = False
    set_current_session(Karaoke(name))
    logger.debug("session started: " + str(get_current_session()))
    embed=discord.Embed()
    embed.add_field(name='New Session', value=f'New karaoke session **{name}** started by {ctx.author.name}.')
    await ctx.respond(embed=embed)

# ends the current karaoke session
@bot.slash_command(guild_ids = servers, name = 'end', description='ends the current session.')
async def end(ctx):
    embed=discord.Embed()
    embed.add_field(name='Success', value=f'Current session **{get_current_session().get_title()}** ended.')
    set_current_session(None)
    await ctx.respond(embed=embed)

# removes a song from the karaoke session's queue from a specified position (1-indexed)
@bot.slash_command(guild_ids = servers, name = 'remove', description='remove a song from the queue.')
async def remove(ctx, position=discord.Option(int, description='position of the song to remove.')):
    get_current_session().remove_from_queue(position)
    embed = discord.Embed()
    embed.add_field(name='Success', value='Removed')
    await ctx.send(embed=embed)

# clears the current song queue
@bot.slash_command(guild_ids = servers, name = 'clear', description='clears the queue. This command is untested and has a small chance of breaking on edge cases.')
async def clear(ctx):
    get_current_session().clear()
    embed=discord.Embed()
    embed.add_field(name='Success', value='Cleared the current queue.')
    await ctx.send(embed=embed)

# search songs
@bot.slash_command(guild_ids = servers, name = 'search', description='search for a song by keyword.')
async def search(ctx, keyword=discord.Option(str, description="any keyword you want to search by.")):
    if len(keyword) < 2:
        await ctx.respond('Your search cannot be less than 2 characters in length.', delete_after=3)
        return
    message = await ctx.respond('Searching...')
    request = await damapi.get_song_info(await damapi.search_by_keyword(keyword, 5, 1))

    view = SearchMenu(ctx, keyword, request, message)
    await view.update_buttons()
    await view.show_results()

# view queue
@bot.slash_command(guild_ids = servers, name = 'queue', description='view the list of currently queued songs.')
async def queue(ctx):
    session = get_current_session()
    end_index = min(5, session.queue_length())
    
    embed = discord.Embed(title=f'Queue for {session.get_title()}:', color=discord.Color.blue())
    
    # Display currently playing song
    if session.now_playing:
        song, author, key, user = session.now_playing
        embed.add_field(name=f'▶️ *{song}', value=f'by {author} • {user} (' + key + ')*', inline=False)
    
    # Display queued songs starting from index 1
    for i in range(end_index):
        song, author, key, user = session.queue[i % 5]
        embed.add_field(name=str(i + 1) + f'. {song}', value=f'by {author} • {user} (' + key + ')', inline=False)
        embed.set_footer(text=f'Page 1 of {max(((session.queue_length() + 4)// 5), 1)}', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhAS56v4R95lmRkF0Z9oqZH66WiBT8MSVWibktrMNzqw&s')

    await ctx.respond(embed=embed, view=QueueMenu(ctx))

# controls
@bot.slash_command(guild_ids = servers, name = 'controls', description='get a control panel of options for the currently playing song.')
async def controls(ctx):
    global current_song_playing
    if not current_song_playing:
        await ctx.respond('No song is currently playing.', delete_after=3)
        return
    message = await ctx.send("Controls for: **" + get_current_session().get_current_song()[0] + "** by **" + get_current_session().get_current_song()[1] + "**")
    view = ControlMenu(ctx, message)
    await message.edit(view=view)
    await message.delete(delay=60)

async def get_pixel_color(x, y):
    loop = asyncio.get_running_loop()
    screenshot = await loop.run_in_executor(None, pyautogui.screenshot)
    pixel = screenshot.getpixel((x, y))
    return pixel
        
bot.run(f'{client_id}')
