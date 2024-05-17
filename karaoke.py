class Karaoke():
    queue = []
    now_playing = None
    title = ''

    def __init__(self, title):
        self.title = title
        self.new_song_playing = False
        self.results_shown = False
        self.first_song = True

    def update_new_song_playing(self, new_song_playing):
        self.new_song_playing = new_song_playing

    def update_results_shown(self, results_shown):
        self.results_shown = results_shown

    def update_first_song(self, first_song):
        self.first_song = first_song

    def is_new_song_playing(self):
        return self.new_song_playing

    def is_results_shown(self):
        return self.results_shown

    def is_first_song(self):
        return self.first_song

    def get_title(self):
        return self.title

    def queue_length(self):
        return len(self.queue)
    
    def get_current_song(self):
        return self.queue[0]
    
    def add_to_queue(self, song_title, author, key, user):
        self.queue.append((song_title, author, key, user))

    def remove_from_queue(self, pos=0):
        self.now_playing = self.queue.pop(pos)
        return self.now_playing
    
    def clear(self):
        self.queue.clear()

    def remove_first_n_from_queue(self, n):
        if n <= 0:
            return
        
        if len(self.queue) <= n:
            self.queue = []
        else:
            self.queue = self.queue[n:]

# Singleton for Karaoke session
class SessionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_session = None
        return cls._instance

    def get_current_session(self):
        return self.current_session

    def set_current_session(self, session):
        self.current_session = session

session_manager = SessionManager()

def get_current_session():
    return session_manager.get_current_session()

def set_current_session(session):
    session_manager.set_current_session(session)