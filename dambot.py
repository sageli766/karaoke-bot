import discord
from discord.ext import tasks
import sys
import pyautogui
import asyncio

import damapi
import damvision
from karaoke import Karaoke, get_current_session, set_current_session
from damcontrol import *
import scaling

from searchmenu import SearchMenu
from controlmenu import ControlMenu
from queuemenu import QueueMenu
from reservemenu import ReserveMenu


client_id = sys.argv[1]
bot = discord.Bot()

servers = ['1239006599633305620', 
           #'1211890173844000820'
           ]

# TODO restart logic, top chart

popped = False
current_song_playing = False

@bot.event
async def on_ready():
    # task_loop.start()
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
    global popped, current_song_playing
    popped = False
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
# @bot.slash_command(guild_ids = servers, name = 'queue', description='view the list of currently queued songs.')
# async def queue(ctx):
#     end_index = min(5, get_current_session().queue_length())
    
#     embed = discord.Embed(title=f'Queue for {get_current_session().get_title()}:', color=discord.Color.blue())
#     for i in range(0, end_index):
#         song, author, key, user = get_current_session().queue[i % 5]
#         if i == 0:
#             embed.add_field(name=f'▶️ {song}', value=f'by {author} • {user} (' + key + ')', inline=False)
#         else:
#             embed.add_field(name=str(i + 1) + f'. {song}', value=f'by {author} • {user} (' + key + ')', inline=False)
        
#     if get_current_session().queue_length() % 5 == 0:
#         embed.set_footer(text=f'Page 1 of {max((get_current_session().queue_length() // 5), 1)}', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhAS56v4R95lmRkF0Z9oqZH66WiBT8MSVWibktrMNzqw&s')
#     else: 
#         embed.set_footer(text=f'Page 1 of {(get_current_session().queue_length() // 5)}', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhAS56v4R95lmRkF0Z9oqZH66WiBT8MSVWibktrMNzqw&s')

#     await ctx.respond(embed=embed, view=QueueMenu(ctx))

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

# @tasks.loop(seconds=10)
# async def task_loop():
#     global popped, current_song_playing

#     if get_current_session():
    
#         x, y = scaling.scale_xy_offset(139, 769)
#         while True:
#             if not current_song_playing:
#                 x1, y1 = scaling.scale_xy_offset(548, 680)
#                 current_color = await get_pixel_color(x1, y1)
#                 if current_color == (205, 29, 27):
#                     click_button(Button.GRADING_START)
#                     click_button(Button.MOUSE_RESET)
#                     logger.debug("color is red!")

#             current_color = await get_pixel_color(x, y)
#             if current_color == (112, 154, 251):
#                 if not current_song_playing:
#                     current_song_playing = True
#                     popped = False
#                     logger.debug("color is blue!")
#             elif current_color == (2, 3, 5) and current_song_playing:
#                 current_song_playing = False
#                 get_current_session().remove_from_queue()
#                 logger.debug("Song is still playing, color is not blue")
#             elif current_color == (2, 3, 5):
#                 if get_current_session():
#                     if get_current_session().queue_length() > 0:
#                         if not popped:
#                             popped = True
#                             song = get_current_session().get_current_song()
#                             await search_keyword_and_reserve(song[0] + " " + song[1], song[2])
#                 logger.debug("color is not blue, song is not playing")
        
#             await asyncio.sleep(3)
            
        


bot.run(f'{client_id}')
