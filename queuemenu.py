import discord
from discord.ui import View, button

from damcontrol import *
from karaoke import get_current_session

SONGS_PER_PAGE = 5
class QueueMenu(View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.page = 1
        if get_current_session().queue_length() % 5 == 0:
            self.pagemax = max(((get_current_session().queue_length() + SONGS_PER_PAGE - 1) // SONGS_PER_PAGE), 1)
        else: 
            self.pagemax = (get_current_session().queue_length() + SONGS_PER_PAGE - 1) // SONGS_PER_PAGE
    async def update_results(self):

        start_index = (self.page - 1) * SONGS_PER_PAGE
        end_index = min(self.page * SONGS_PER_PAGE, get_current_session().queue_length())
        
        embed = discord.Embed(title=f'Queue for {get_current_session().get_title()}:', color=discord.Color.blue())

        for i in range(start_index, end_index):
            song, author, key, user = get_current_session().queue[i % 5]
            if i == 0:
                embed.add_field(name=f'▶️ {song}', value=f'{author} • Queued by {user} *(' + key + ')*', inline=False)
            else:
                embed.add_field(name=str(i + 1) + f'. {song}', value=f'{author} • Queued by {user} *(' + key + ')*', inline=False)

        embed.set_footer(text=f'Page {self.page} of {self.pagemax}', icon_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhAS56v4R95lmRkF0Z9oqZH66WiBT8MSVWibktrMNzqw&s')
        
        return embed

    async def show_results(self):
        if self.message:
            await self.message.edit(embed=await self.update_results(), view=self)
        else:
            self.message = await self.ctx.send(embed=await self.update_results(), view=self)
            await self.message.delete(delay=30)


    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @button(emoji="⬅️", style=discord.ButtonStyle.gray, row=1)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
        
            await self.show_results()

    @button(emoji="➡️", style=discord.ButtonStyle.gray, row=1)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page < self.pagemax:
            self.page += 1

            await self.show_results()
