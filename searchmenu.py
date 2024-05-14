import asyncio
import discord
from discord.ui import View, button

from damcontrol import *
import damvision
import session

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
        
        embed.set_thumbnail(url="https://dan.onl/images/emptysong.jpg")

        embed.set_footer(text=f'Page {self.page} of {self.pagemax} • BETA feature. Results may not be accurate.', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHfcxYZjBZ2U3rgSspBSkRWU-Ynyh-P-okUNhnUu0Z3A&s')

        # i hate discord.py i do not know how to make buttons that update with the song numbers
        # for item in self.children:
        #     if isinstance(item, discord.ui.Button) and item.custom_id.startswith("song_"):
        #         self.remove_item(item)

        # for i in range(start_index, end_index):
        #     button_label = str(i + 1)
        #     self.add_item(discord.ui.Button(label=button_label, style=discord.ButtonStyle.green, custom_id=f"song_{i+1}", row=2))
        
        return embed

    async def queue_song(self, number):
        start_index = (self.page - 1) * SONGS_PER_PAGE
        end_index = min(self.page * SONGS_PER_PAGE, self.num_hits)
        
        embed = discord.Embed(title=f'Search Results for {self.keyword}:', color=discord.Color.yellow())

        for i in range(start_index, end_index):
            song, author = self.results[i % 5]
            if i % 5 == number - 1:
                embed.add_field(name=str(i + 1) + f'. {song} <- Reserving...', value=f'{author}', inline=False)
            else:
                embed.add_field(name=str(i + 1) + '. ----', value='--', inline=False)
        
        embed.set_thumbnail(url="https://dan.onl/images/emptysong.jpg")

        embed.set_footer(text=f'Page {self.page} of {self.pagemax} • BETA feature. Results may not be accurate.', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQefE5gdPyyrwTpGrMlLVbIsgp5cCDTccBUVtuIR-j0BQ&s')
        
        return embed

    async def show_results(self):
        await self.message.edit(content='', embed=await self.update_results(), view=self)
        #TODO add timeout if no interaction


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

    @button(label="Cancel Search", style=discord.ButtonStyle.red, row=1)
    async def cancel_search(self, interaction: discord.Interaction, button: discord.ui.Button):
        damvision.click_button(Button.TOP)
        session.set_someone_using(False)
        await self.message.delete()

    # too lazy to make a function for these lmao
    @button(label="1", style=discord.ButtonStyle.green, row=2)
    async def song1(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[0]
        await interaction.response.defer()
        await self.message.edit(embed=await self.queue_song(1), view=None)
        await asyncio.sleep(3)
        select_and_queue(1)
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.edit(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**", suppress=True)
        session.set_someone_using(False)

    @button(label="2", style=discord.ButtonStyle.green, row=2)
    async def song2(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[1]
        await interaction.response.defer()
        await self.message.edit(embed=await self.queue_song(2), view=None)
        await asyncio.sleep(3)
        select_and_queue(2)
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.edit(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**", suppress=True)
        session.set_someone_using(False)

    @button(label="3", style=discord.ButtonStyle.green, row=2)
    async def song3(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[2]
        await interaction.response.defer()
        await self.message.edit(embed=await self.queue_song(3), view=None)
        await asyncio.sleep(3)
        select_and_queue(3)
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.edit(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**", suppress=True)
        session.set_someone_using(False)

    @button(label="4", style=discord.ButtonStyle.green, row=2)
    async def song4(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[3]
        await interaction.response.defer()
        await self.message.edit(embed=await self.queue_song(4), view=None)
        await asyncio.sleep(3)
        select_and_queue(4)
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.edit(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**", suppress=True)
        session.set_someone_using(False)

    @button(label="5", style=discord.ButtonStyle.green, row=2)
    async def song5(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results[4]
        await interaction.response.defer()
        await self.message.edit(embed=await self.queue_song(5), view=None)
        await asyncio.sleep(3)
        select_and_queue(5)
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.edit(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**", suppress=True)
        session.set_someone_using(False)
