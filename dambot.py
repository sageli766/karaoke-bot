import discord
from discord.ext import commands
import karaoke
import sys

client_id = 'MTIzNDcxMTczNDc0NTU2MzE4Ng.G7rzly.CNMTVJMkq8MWyvJ5br_TytNLwhepImwKfPkNq8'
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

running = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def parrot(ctx, *args):
    for arg in args:
        await ctx.send(f'{arg}')

@bot.command()
async def kstart(ctx):
    current_session = karaoke()
    await ctx.send(f'')

@bot.command()
async def add(ctx, song_title):
    try:
        current_session.add_to_queue(song_title, ctx.author.name)
        embed = discord.Embed()
        embed.add_field(value=f'Successfully added {song_title} to the queue.')
        ctx.send(embed=embed)
    except:
        embed = discord.Embed()
        ctx.send

@bot.command()
async def clear(ctx):
    current_session

bot.run(f'{client_id}')