import discord

class Karaoke():
    queue = []
    title = ''

    def __init__(self, title):
        self.title = title

    def add_to_queue(self, song_title, user):
        for i in song_title:
            self.queue.append((song_title, user))

    def remove_from_queue(self, pos):
        self.queue.pop(pos)

    def clear(self):
        self.queue = []