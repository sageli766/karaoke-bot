import asyncio
import discord
from discord.ui import View, button

import damapi
from damcontrol import *
import damvision
import session

SONGS_PER_PAGE = 5
class SearchMenu(View):
    def __init__(self, ctx, keyword, results, message):
        super().__init__()
        self.ctx = ctx
        self.keyword = keyword
        self.results = results
        self.page = 1
        self.message = message

    async def update_results(self):
        start_index = (self.page - 1) * SONGS_PER_PAGE
        end_index = min(self.page * SONGS_PER_PAGE, self.results['totalCount'])
        
        embed = discord.Embed(title=f'Search Results for {self.keyword}:', color=discord.Color.blue())

        for i in range(start_index, end_index):
            song, author = self.results['songs'][i % 5]
            embed.add_field(name=str(i + 1) + f'. {song}', value=f'by {author}', inline=False)
        
        embed.set_thumbnail(url="https://dan.onl/images/emptysong.jpg")

        page_count = self.results['pageCount']

        embed.set_footer(text=f'Page {self.page} of {page_count}', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHfcxYZjBZ2U3rgSspBSkRWU-Ynyh-P-okUNhnUu0Z3A&s')

        # i hate discord.py i do not know how to make buttons that update with the song numbers
        # for item in self.children:
        #     if isinstance(item, discord.ui.Button) and item.custom_id.startswith("song_"):
        #         self.remove_item(item)

        # for i in range(start_index, end_index):
        #     button_label = str(i + 1)
        #     self.add_item(discord.ui.Button(label=button_label, style=discord.ButtonStyle.green, custom_id=f"song_{i+1}", row=2))
        
        return embed

    async def show_results(self):
        await self.message.edit(content='', embed=await self.update_results(), view=self)
        await self.message.delete(delay=60)

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @button(label="Previous Page", style=discord.ButtonStyle.gray, row=1)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1

            await interaction.response.defer()
            embed = discord.Embed(title=f'Loading page {self.page} for {self.keyword}:', color=discord.Color.yellow())
            start_index = (self.page - 1) * SONGS_PER_PAGE
            end_index = min(self.page * SONGS_PER_PAGE, self.results['totalCount'])
            for i in range(start_index, end_index):
                embed.add_field(name=str(i + 1) + f'. ----', value=f'--', inline=False)
            embed.set_footer(text=f'Page {self.page} of ' + str(self.results['pageCount']))
            await self.message.edit(embed=embed, view=self)

            self.results = damapi.get_song_info(damapi.search_by_keyword(self.keyword, 5, self.page))

            await self.show_results()
        else: await interaction.response.defer()

    @button(label="Next Page", style=discord.ButtonStyle.gray, row=1)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.results['pageCount']:
            self.page += 1

            await interaction.response.defer()
            embed = discord.Embed(title=f'Loading page {self.page} for {self.keyword}:', color=discord.Color.yellow())
            start_index = (self.page - 1) * SONGS_PER_PAGE
            end_index = min(self.page * SONGS_PER_PAGE, self.results['totalCount'])
            for i in range(start_index, end_index):
                embed.add_field(name=str(i + 1) + f'. ----', value=f'--', inline=False)
            embed.set_footer(text=f'Page {self.page} of ' + str(self.results['pageCount']))
            await self.message.edit(embed=embed, view=self)

            self.results = damapi.get_song_info(damapi.search_by_keyword(self.keyword, 5, self.page))

            await self.show_results()
        else: await interaction.response.defer()

    # @button(label="Cancel Search", style=discord.ButtonStyle.red, row=1)
    # async def cancel_search(self, interaction: discord.Interaction, button: discord.ui.Button):
    #     await self.message.delete()

    # too lazy to make a function for these lmao
    @button(label="1", style=discord.ButtonStyle.green, row=2)
    async def song1(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results['songs'][0]
        await interaction.response.defer()
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.delete()
        await self.ctx.send(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**")

    @button(label="2", style=discord.ButtonStyle.green, row=2)
    async def song2(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results['songs'][1]
        await interaction.response.defer()
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.delete()
        await self.ctx.send(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**")

    @button(label="3", style=discord.ButtonStyle.green, row=2)
    async def song3(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results['songs'][2]
        await interaction.response.defer()
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.delete()
        await self.ctx.send(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**")

    @button(label="4", style=discord.ButtonStyle.green, row=2)
    async def song4(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results['songs'][3]
        await interaction.response.defer()
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.delete()
        await self.ctx.send(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**")

    @button(label="5", style=discord.ButtonStyle.green, row=2)
    async def song5(self, interaction: discord.Interaction, button: discord.ui.Button):
        song, author = self.results['songs'][4]
        await interaction.response.defer()
        session.get_current_session().add_to_queue(song, author, self.ctx.author.display_name)
        logger.info("song " + song + " by " + author + " has been added to the queue.")
        await self.message.delete()
        await self.ctx.send(content=self.ctx.author.display_name + " reserved: **" + song + "** by **" + author + "**")
