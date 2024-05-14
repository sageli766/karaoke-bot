import discord
from discord.ui import View, button
from fuzzywuzzy import fuzz

import damvision
from damcontrol import *
import session

SONGS_PER_PAGE = 5
class QueueMenu(View):
    def __init__(self, ctx, message):
        super().__init__()
        self.ctx = ctx
        self.page = 1
        self.pagemax = (session.get_current_session().queue_length() + SONGS_PER_PAGE - 1) // SONGS_PER_PAGE
        self.message = message

    async def update_results(self):

        updated = False

        if not damvision.playing_song():
            pass
        else:
            while session.get_current_session().queue and fuzz.ratio(session.get_current_session().queue[0][0], damvision.playing_song()) < 80: #TODO give more datapoints later, like combine author
                session.get_current_session().queue.pop(0)
            updated = True


        start_index = (self.page - 1) * SONGS_PER_PAGE
        end_index = min(self.page * SONGS_PER_PAGE, session.get_current_session().queue_length())
        
        embed = discord.Embed(title=f'Queue for {session.get_current_session().get_title()}:', color=discord.Color.blue())

        for i in range(start_index, end_index):
            song, author, user = session.get_current_session().queue[i % 5]
            if i == 0:
                embed.add_field(name=f'▶️ {song}', value=f'{author} • Queued by {user}', inline=False)
            else:
                embed.add_field(name=str(i + 1) + f'. {song}', value=f'{author} • Queued by {user}', inline=False)
        
        if updated:
            embed.set_footer(text=f'Page {self.page} of {self.pagemax}', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhAS56v4R95lmRkF0Z9oqZH66WiBT8MSVWibktrMNzqw&s')
        else: 
            embed.set_footer(text=f'Page {self.page} of {self.pagemax} • May not be up to date.', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTabSf_3_hGEf6urhOIK38T0P6nj3NrBkyBaba8TmGKXg&s')
        
        return embed

    async def show_results(self):
        if self.message:
            await self.message.edit(embed=await self.update_results(), view=self)
        else:
            self.message = await self.ctx.send(embed=await self.update_results(), view=self)
            await self.message.delete(delay=30)
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

            await self.show_results()

    @button(label="Close", style=discord.ButtonStyle.red, row=1)
    async def cancel_search(self, interaction: discord.Interaction, button: discord.ui.Button):
        damvision.click_button(Button.TOP)
        await self.message.delete()