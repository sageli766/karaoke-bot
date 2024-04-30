import discord
from discord.ext import commands
from karaoke import Karaoke
import sys

client_id = 'MTIzNDcxMTczNDc0NTU2MzE4Ng.G7rzly.CNMTVJMkq8MWyvJ5br_TytNLwhepImwKfPkNq8'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

current_session = None

running = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def parrot(ctx, *args):
    for arg in args:
        await ctx.send(f'{arg}')

@bot.command()
async def kstart(ctx, title):
    global current_session
    current_session = Karaoke(title)
    embed=discord.Embed()
    embed.add_field(name='New Session', value=f'New karaoke session **{title}** started by {ctx.author.name}.')
    await ctx.send(embed=embed)

@bot.command()
async def kend(ctx):
    global current_session
    current_session = None
    embed=discord.Embed()
    embed.add_field(name='Success', value=f'Current session **{current_session.title}**.')
    await ctx.send(embed=embed)

@bot.command()
async def add(ctx, song_title):
    global current_session
    try:
        current_session.add_to_queue(song_title, ctx.author.name)
        embed = discord.Embed()
        embed.add_field(name='Success', value=f'Added **{song_title}** to the queue.')
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed()
        embed.add_field(name='Success', value='There is no karaoke running right now.')
        await ctx.send(embed=embed)

@bot.command()
async def clear(ctx):
    global current_session
    current_session.clear()
    embed=discord.Embed()
    embed.add_field(name='Success', value='Cleared the current queue.')
    await ctx.send(embed=embed)

@bot.command()
async def getqueue(ctx):
    global current_session
    await ctx.send(embed=current_session.queue_embed)

bot.run(f'{client_id}')