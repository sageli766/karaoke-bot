import discord
from discord.ui import View, button

from damcontrol import *
import damvision
from karaoke import get_current_session

SONGS_PER_PAGE = 5
class ControlMenu(View):
    def __init__(self, ctx, message):
        super().__init__()
        self.ctx = ctx
        self.page = 1
        self.pagemax = (get_current_session().queue_length() + SONGS_PER_PAGE - 1) // SONGS_PER_PAGE
        self.message = message

    async def check_valid(self):

        if not damvision.playing_song():
            return False
        
        return True

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @button(label="Stop", style=discord.ButtonStyle.red, row=1)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.check_valid:
            self.message.edit(content='Skipping song...', view=None)
            self.message.delete(delay=5)
            click_button(Button.SKIP)
            time.sleep(5)
            click_button(Button.RESTART_CONFIRM)
            click_button(Button.MOUSE_RESET)
        else:
            self.message.edit(content="Error: different song. Retry $c", view=None)

    @button(label="Restart", style=discord.ButtonStyle.red, row=1, disabled=True)
    async def restart(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.check_valid:
            click_button(Button.RESTART)
        else:
            self.message.edit(content="Error: different song. Retry $c", view=None)

    @button(label="Close Menu", style=discord.ButtonStyle.grey, row=1)
    async def close_menu(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        click_button(Button.TOP)
        await self.message.delete()
    
    @button(label="Key -", style=discord.ButtonStyle.blurple, row=2)
    async def key_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.check_valid:
            click_button(Button.KEYDOWN)
        else:
            self.message.edit(content="Error: different song. Retry $c", view=None)

    @button(label="Key +", style=discord.ButtonStyle.blurple, row=2)
    async def key_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.check_valid:
            click_button(Button.KEYUP)
        else:
            self.message.edit(content="Error: different song. Retry $c", view=None)