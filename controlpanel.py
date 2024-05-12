from discord.ui import Button
import discord
from discord import ButtonStyle

class ControlPanelView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(Button(label='Stop', style=ButtonStyle.red, custom_id='stop'))
        self.add_item(Button(label='Pause', style=ButtonStyle.primary, custom_id='pause'))
        self.add_item(Button(label='Restart', style=ButtonStyle.secondary, custom_id='restart'))
        self.add_item(Button(label='Key Up', style=ButtonStyle.blurple, custom_id='keyup'))
        self.add_item(Button(label='Key Down', style=ButtonStyle.blurple, custom_id='keydown'))