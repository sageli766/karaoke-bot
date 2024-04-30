import discord

class Karaoke():
    queue = []
    queue_embed = None
    title = ''

    def __init__(self, title):
        self.queue_embed = discord.Embed(
            title=f'{title}',
            color=discord.Color.blue()
        )
        self.title = title

    def add_to_queue(self, song_title, user):
        self.queue.append(song_title)
        self.queue_embed.add_field(name = f'{song_title}', value=f'Queued by: {user}')

    def remove_from_queue(self, pos):
        self.queue.pop(pos)

    def clear(self):
        self.queue = []
        self.queue_embed.clear_fields()

    def completed(self):
        self.queue.pop()

    def get_queue(self):
        return self.queue

