import discord

class Karaoke():
    queue = []
    title = ''

    def __init__(self, title):
        self.queue_embed = discord.Embed(
            title=f'{title}',
            color=discord.Color.blue()
        )
        self.title = title

    def add_to_queue(self, song_title, user):
        for i in song_title:
            self.queue.append((song_title, user))

    def remove_from_queue(self, pos):
        self.queue.pop(pos)

    def clear(self):
        self.queue = []

    def completed(self):
        self.queue.pop()

    def get_queue(self):
        return self.queue

