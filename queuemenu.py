import discord
from discord.ui import View, button

from damcontrol import *
from karaoke import get_current_session

class QueueMenu(View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.page = 1
        self.message = None
        self.update_pagemax()

    def update_pagemax(self):
        session = get_current_session()
        self.pagemax = max(((session.queue_length() + 4) // 5), 1)

    async def update_results(self):
        start_index = (self.page - 1) * 5
        end_index = min(self.page * 5, get_current_session().queue_length())

        embed = discord.Embed(title=f'Queue for {get_current_session().get_title()}:', color=discord.Color.blue())

        for i in range(start_index, end_index):
            song, author, key, user = get_current_session().queue[i % 5]
            if i == 0:
                embed.add_field(name=f'▶️ {get_current_session().now_playing[0]}', value=f'*{get_current_session().now_playing[1]} • Queued by {get_current_session().now_playing[3]} ({key})*', inline=False)
            else:
                embed.add_field(name=str(i + 1) + f'. {song}', value=f'{author} • Queued by {user} *({key})*', inline=False)

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
    async def previous_page(self, button, interaction):
        if self.page > 1:
            self.page -= 1
            await self.show_results()

    @button(emoji="➡️", style=discord.ButtonStyle.gray, row=1)
    async def next_page(self, button, interaction):
        if self.page < self.pagemax:
            self.page += 1
            await self.show_results()
