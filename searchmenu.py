import discord
from discord.ui import View, button

import damapi
from damcontrol import *
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

    async def update_embed(self):
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
        await self.message.edit(content='', embed=await self.update_embed(), view=self)

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

    class add_prev_page_button(discord.ui.Button):
        def __init__(self, view, emoji, disabled):
            super().__init__(emoji=emoji, style=discord.ButtonStyle.gray, row=2, disabled=disabled)
            self.search_view = view  # Use a different attribute name
    
        async def callback(self, interaction: discord.Interaction):
            self.search_view.page -= 1
            await self.search_view.update_page(interaction)
    
    class add_next_page_button(discord.ui.Button):
        def __init__(self, view, emoji, disabled):
            super().__init__(emoji=emoji, style=discord.ButtonStyle.gray, row=2, disabled=disabled)
            self.search_view = view  # Use a different attribute name
    
        async def callback(self, interaction: discord.Interaction):
            self.search_view.page += 1
            await self.search_view.update_page(interaction)
    
    async def update_buttons(self):
        self.clear_items()
        start_index = (self.page - 1) * SONGS_PER_PAGE

        for i in range(start_index, min(start_index + SONGS_PER_PAGE, self.results['totalCount'])):
            self.add_item(self.add_number_button(i + 1, self.results['songs'][i % 5], self.ctx, self))
        
        previous_disabled = self.page == 1
        next_disabled = self.page == self.results['pageCount']
        
        self.add_item(self.add_prev_page_button(self, "⬅️", previous_disabled))
        self.add_item(self.add_next_page_button(self, "➡️", next_disabled))


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
        await self.message.edit(embed=embed, view=LoadingView())

class LoadingView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="--", style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def a(self, button, interaction):
        pass
    @discord.ui.button(label="--", style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def b(self, button, interaction):
        pass
    @discord.ui.button(label="--", style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def c(self, button, interaction):
        pass
    @discord.ui.button(label="--", style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def d(self, button, interaction):
        pass
    @discord.ui.button(label="--", style=discord.ButtonStyle.gray, disabled=True, row=1)
    async def e(self, button, interaction):
        pass
    @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.gray, disabled=True, row=2)
    async def f(self, button, interaction):
        pass
    @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.gray, disabled=True, row=2)
    async def g(self, button, interaction):
        pass
