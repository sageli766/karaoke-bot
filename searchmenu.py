import discord
from discord.ui import View, button

import damapi
from damcontrol import *
from karaoke import get_current_session
from reservemenu import ReserveMenu

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
            song, author, *_ = self.results['songs'][i % SONGS_PER_PAGE]
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
        def __init__(self, label, song_info, ctx, prev_view):
            super().__init__(label=label)  # set label and super init class
            self.song_info = song_info
            self.ctx = ctx
            self.prev_view = prev_view

        async def callback(self, interaction: discord.Interaction):
            view = ReserveMenu(self.ctx, self.song_info, self.prev_view)
            embed = await view.create_embed()
            await interaction.message.edit(embed=embed, view=view)  # update message
            await interaction.response.defer()

    async def update_buttons(self):
        start_index = (self.page - 1) * SONGS_PER_PAGE
        await self.delete_buttons(start_index)
        # logger.debug(str(start_index) + " " + str(min(start_index + SONGS_PER_PAGE, self.results['totalCount'])))
        for i in range(start_index, min(start_index + SONGS_PER_PAGE, self.results['totalCount'])):
            self.add_item(self.add_number_button(i+1, self.results['songs'][i % 5], self.ctx, self))
    
    async def delete_buttons(self, from_index):

        buttons = [button for button in self.children]

        for button in buttons:
            if isinstance(button.label, int):
                logger.debug("button has int: " + str(button))
                if button.label <= from_index or button.label > from_index + 5:
                    logger.debug("removing " + str(button))
                    self.remove_item(button)

    @button(emoji="⬅️", style=discord.ButtonStyle.gray, row=2, disabled=True)
    async def previous_page(self, button, interaction):
        logger.debug(self.page)
        if self.page > 1:
            self.page -= 1
            for button1 in self.children:
                if button1.emoji and button1.emoji.name == '➡️':
                    button1.disabled = False
            if self.page == 1:
                logger.debug("disabled button")
                button.disabled = True
            await self.update_page(interaction)


    @button(emoji="➡️", style=discord.ButtonStyle.gray, row=2)
    async def next_page(self, button, interaction):
        if self.page < self.results['pageCount']:
            self.page += 1
            for button1 in self.children:
                if button1.emoji and button1.emoji.name == '⬅️':
                    button1.disabled = False
            if self.page == self.results['pageCount']:
                button.disabled = True
            await self.update_page(interaction) #TODO gray out if no results

    async def update_page(self, interaction):
        await self.show_loading_page()
        await interaction.response.defer()
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
        await self.message.edit(embed=embed, view=None)
