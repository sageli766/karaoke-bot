import discord
from discord.ui import View, button

import damapi
from damcontrol import *
from karaoke import get_current_session

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
            song, author = self.results['songs'][i % SONGS_PER_PAGE]
            index = start_index + i % SONGS_PER_PAGE + 1
            embed.add_field(name=f"{index}. {song}", value=f'by {author}', inline=False)
        
        embed.set_thumbnail(url="https://dan.onl/images/emptysong.jpg")

        page_count = self.results['pageCount']

        embed.set_footer(text=f'Page {self.page} of {page_count}', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHfcxYZjBZ2U3rgSspBSkRWU-Ynyh-P-okUNhnUu0Z3A&s')
        
        return embed

    async def show_results(self):
        await self.message.edit(content='', embed=await self.update_results(), view=self)

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author
    
    class add_number_button(discord.ui.Button):  # Button class
        def __init__(self, label, song, author, ctx):
            super().__init__(label=label)  # set label and super init class
            self.song = song
            self.author = author
            self.ctx = ctx

        async def callback(self, interaction: discord.Interaction):
            self.disabled = True
            await interaction.message.edit(view=self.view)  # update message
            await interaction.response.defer()
            get_current_session().add_to_queue(self.song, self.author, self.ctx.author.display_name)
            logger.info(f"Song {self.song} by {self.author} has been added to the queue.")
            await self.message.delete()
            await self.ctx.send(content=f"{self.ctx.author.display_name} reserved: **{self.song}** by **{self.author}**")

    async def update_buttons(self):
        start_index = (self.page - 1) * SONGS_PER_PAGE
        await self.delete_buttons(start_index)
        logger.debug(str(start_index) + " " + str(min(start_index + SONGS_PER_PAGE, self.results['totalCount'])))
        for i in range(start_index, min(start_index + SONGS_PER_PAGE, self.results['totalCount'])):
            song, author = self.results['songs'][i % 5]
            self.add_item(self.add_number_button(i+1, song, author, self.ctx))
    
    async def delete_buttons(self, from_index):

        buttons = [button for button in self.children]

        for button in buttons:
            if isinstance(button.label, int):
                if button.label <= from_index or button.label > from_index + 5:
                    self.remove_item(button)

    @button(emoji="⬅️", style=discord.ButtonStyle.gray, row=2, disabled=True)
    async def previous_page(self, button, interaction):
        logger.debug(self.page)
        if self.page > 1:
            self.page -= 1
            await interaction.response.defer()
            for button1 in self.children:
                if button1.emoji and button1.emoji.name == '➡️':
                    button1.disabled = False
            if self.page == 1:
                logger.debug("disabled button")
                button.disabled = True
            await self.update_page()


    @button(emoji="➡️", style=discord.ButtonStyle.gray, row=2)
    async def next_page(self, button, interaction):
        if self.page < self.results['pageCount']:
            self.page += 1
            await interaction.response.defer()
            for button1 in self.children:
                if button1.emoji and button1.emoji.name == '⬅️':
                    button1.disabled = False
            if self.page == self.results['pageCount']:
                button.disabled = True
            await self.update_page() #TODO gray out if no results

    async def update_page(self):
        await self.show_loading_page()
        self.results = await damapi.get_song_info(await damapi.search_by_keyword(self.keyword, 5, self.page))
        await self.update_buttons()
        await self.show_results()

    async def show_loading_page(self):
        embed = discord.Embed(title=f'Loading page {self.page} for {self.keyword}:', color=discord.Color.yellow())
        start_index = (self.page - 1) * SONGS_PER_PAGE
        end_index = min(self.page * SONGS_PER_PAGE, self.results['totalCount'])
        for i in range(start_index, end_index):
            embed.add_field(name=str(i + 1) + f'. ----', value=f'--', inline=False)
        embed.set_footer(text=f'Page {self.page} of ' + str(self.results['pageCount']))
        await self.message.edit(embed=embed, view=self)
