import discord
from discord.ui import View, button
import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from damcontrol import *
from karaoke import get_current_session

import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_info(search):
    song_search_results = sp.search(q=search, type='track', limit=1)

    if song_search_results['tracks']['items']:
        track = song_search_results['tracks']['items'][0]
        song_url = track['external_urls']['spotify']
        cover_image_url = track['album']['images'][0]['url']
        artist_url = track['artists'][0]['external_urls']['spotify']
    else:
        song_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHfcxYZjBZ2U3rgSspBSkRWU-Ynyh-P-okUNhnUu0Z3A&s"
        cover_image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHfcxYZjBZ2U3rgSspBSkRWU-Ynyh-P-okUNhnUu0Z3A&s'
        artist_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHfcxYZjBZ2U3rgSspBSkRWU-Ynyh-P-okUNhnUu0Z3A&s"

    return song_url, cover_image_url, artist_url


class ReserveMenu(View):
    def __init__(self, ctx, song_info, prev_view):
        super().__init__()
        self.ctx = ctx
        self.song_info = song_info
        self.prev_view = prev_view
        self.key_mod = '+0'

    async def create_embed(self):
        song_name, artist, release_date, highlight_lyrics, playback_time, guide_vocal_flag, score_flag = self.song_info
        song_url, cover_image_url, artist_url = get_song_info(song_name + " " + artist)

        embed = discord.Embed(title=song_name,
                          description="",
                          colour=0x00b0f4,
                          url=song_url
                          )

        embed.set_author(name=artist,
                         url=artist_url,)

        embed.add_field(name="Lyrics Preview",
                        value=highlight_lyrics[4:] + "...",
                        inline=False)
        embed.add_field(name="Runtime",
                        value=f"{playback_time // 60:02d}:{playback_time % 60:02d}",
                        inline=True)
        embed.add_field(name="Release Date (DAM)",
                        value=release_date,
                        inline=True)

        embed.set_thumbnail(url=cover_image_url)

        embed.set_footer(text="Press \"Reserve\" to add to queue.",
                         icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHfcxYZjBZ2U3rgSspBSkRWU-Ynyh-P-okUNhnUu0Z3A&s")
        
        return embed

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author
    
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Key", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(label="+ 7"),
            discord.SelectOption(label="+ 6"),
            discord.SelectOption(label="+ 5"),
            discord.SelectOption(label="+ 4"),
            discord.SelectOption(label="+ 3"),
            discord.SelectOption(label="+ 2"),
            discord.SelectOption(label="+ 1"),
            discord.SelectOption(label="Key: + 0 (default)", default=True),
            discord.SelectOption(label="- 1"),
            discord.SelectOption(label="- 2"),
            discord.SelectOption(label="- 3"),
            discord.SelectOption(label="- 4"),
            discord.SelectOption(label="- 5"),
            discord.SelectOption(label="- 6"),
            discord.SelectOption(label="- 7"),
        ]
    )
    async def select_callback(self, select, interaction): # the function called when the user is done selecting options
        self.key_mod = ''.join(re.findall(r'[+\-\d]', select.values[0]))
        await interaction.response.defer()

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @button(label='Back', style=discord.ButtonStyle.gray)
    async def previous_page(self, button, interaction):
        # await self.prev_view.update_buttons()
        await interaction.response.defer()
        await self.prev_view.update_buttons()
        await self.prev_view.show_results()

    # if backing_vocals == "0" disable the button
    @button(label='Backing Vocals', style=discord.ButtonStyle.gray, disabled=True)
    async def backing(self, button, interaction):
        logger.debug(self.page)
        # if button is clicked make it green, and vice versa
        

    # if backing_vocals == "0" disable the button
    @button(label='Pitch Guide', style=discord.ButtonStyle.green, disabled=True)
    async def pitch(self, button, interaction):
        logger.debug(self.page)
        # if button is clicked make it gray, and vice versa

    @button(label='Reserve', style=discord.ButtonStyle.green)
    async def reserve(self, button, interaction):
        name = self.song_info[0]
        artist = self.song_info[1]
        get_current_session().add_to_queue(name, artist, self.key_mod, self.ctx.author.display_name)
        logger.info(f"Song {name} by {artist} has been added to the queue.")
        if self.key_mod != '+0':
            await self.message.edit(content=f"{self.ctx.author.display_name} reserved: **{name}** by **{artist}** *(" + self.key_mod + ")*", view=None, suppress=True)
        else:
            await self.message.edit(content=f"{self.ctx.author.display_name} reserved: **{name}** by **{artist}**", view=None, suppress=True)
        await interaction.response.defer()

