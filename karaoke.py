import discord

class Karaoke():
    queue = []
    title = ''

    def __init__(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def queue_length(self):
        return len(self.queue)
    
    def add_to_queue(self, song_title, author, user):
        self.queue.append((song_title, author, user))

    def remove_from_queue(self, pos):
        self.queue.pop(pos)

    def remove_first_n_from_queue(self, n):
        if n <= 0:
            return
        
        if len(self.queue) <= n:
            self.queue = []
        else:
            self.queue = self.queue[n:]
