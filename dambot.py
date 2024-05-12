import asyncio
import discord
from discord.ext import commands
from discord.ui import View, button
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


SONGS_PER_PAGE = 5
class SearchMenu(View):
    def __init__(self, ctx, keyword, num_hits, results, message):
        super().__init__()
        self.ctx = ctx
        self.keyword = keyword
        self.num_hits = num_hits
        self.results = results
        self.page = 1
        self.pagemax = (num_hits + SONGS_PER_PAGE - 1) // SONGS_PER_PAGE
        self.message = message

    async def update_results(self):
        start_index = (self.page - 1) * SONGS_PER_PAGE
        end_index = min(self.page * SONGS_PER_PAGE, self.num_hits)
        
        embed = discord.Embed(title=f'Search Results for {self.keyword}:', color=discord.Color.blue())

        for i in range(start_index, end_index):
            song, author = self.results[i % 5]
            embed.add_field(name=str(i + 1) + f'. {song}', value=f'{author}', inline=False)

        embed.set_footer(text=f'Page {self.page} of {self.pagemax}')

        # for item in self.children:
        #     if isinstance(item, discord.ui.Button) and item.custom_id.startswith("song_"):
        #         self.remove_item(item)

        # for i in range(start_index, end_index):
        #     button_label = str(i + 1)
        #     self.add_item(discord.ui.Button(label=button_label, style=discord.ButtonStyle.green, custom_id=f"song_{i+1}", row=2))
        
        return embed

    async def show_results(self):
            await self.message.edit(content='', embed=await self.update_results(), view=self)

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @button(label="Previous Page", style=discord.ButtonStyle.gray, row=1)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1

            await interaction.response.defer()
            embed = discord.Embed(title=f'Loading page {self.page} for {self.keyword}:', color=discord.Color.yellow())
            start_index = (self.page - 1) * SONGS_PER_PAGE
            end_index = min(self.page * SONGS_PER_PAGE, self.num_hits)
            for i in range(start_index, end_index):
                embed.add_field(name=str(i + 1) + f'. ----', value=f'--', inline=False)
            embed.set_footer(text=f'Page {self.page} of {self.pagemax}')
            await self.message.edit(embed=embed, view=self)

            self.num_hits, self.results = scroll_up_update()
            await self.show_results()

    @button(label="Next Page", style=discord.ButtonStyle.gray, row=1)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.pagemax:
            self.page += 1

            await interaction.response.defer()
            embed = discord.Embed(title=f'Loading page {self.page} for {self.keyword}:', color=discord.Color.yellow())
            start_index = (self.page - 1) * SONGS_PER_PAGE
            end_index = min(self.page * SONGS_PER_PAGE, self.num_hits)
            for i in range(start_index, end_index):
                embed.add_field(name=str(i + 1) + f'. ----', value=f'--', inline=False)
            embed.set_footer(text=f'Page {self.page} of {self.pagemax}')
            await self.message.edit(embed=embed, view=self)

            self.num_hits, self.results = scroll_down_update()
            await self.show_results()

    @button(label="1", style=discord.ButtonStyle.green, row=2)
    async def song1(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[0]
        await self.message.edit(content="**" + song + "** has been added to the queue!", suppress=True, view=None)
        select_and_queue(1)
        logger.info("song " + song + " by " + author + " has been added to the queue.")


    @button(label="2", style=discord.ButtonStyle.green, row=2)
    async def song2(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[1]
        await self.message.edit(content="**" + song + "** has been added to the queue!", suppress=True, view=None)
        select_and_queue(2)
        logger.info("song " + song + " by " + author + " has been added to the queue.")

    @button(label="3", style=discord.ButtonStyle.green, row=2)
    async def song3(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[2]
        await self.message.edit(content="**" + song + "** has been added to the queue!", suppress=True, view=None)
        select_and_queue(3)
        logger.info("song " + song + " by " + author + " has been added to the queue.")

    @button(label="4", style=discord.ButtonStyle.green, row=2)
    async def song4(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[3]
        await self.message.edit(content="**" + song + "** has been added to the queue!", suppress=True, view=None)
        select_and_queue(4)
        logger.info("song " + song + " by " + author + " has been added to the queue.")

    @button(label="5", style=discord.ButtonStyle.green, row=2)
    async def song5(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[4]
        await self.message.edit(content="**" + song + "** has been added to the queue!", suppress=True, view=None)
        select_and_queue(5)
        logger.info("song " + song + " by " + author + " has been added to the queue.")


# search songs
@bot.command()
async def s(ctx, keyword):
    message = await ctx.send('Searching...')
    num_hits, results = search_keyword(keyword)
    if num_hits == -1:
        num_hits = max(0, len(results))

    view = SearchMenu(ctx, keyword, num_hits, results, message)
    await view.show_results()

bot.run(f'{client_id}')