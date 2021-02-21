import pygame

MUSIC_END_EVENT = pygame.USEREVENT + 1


class MusicSubsystem:
    def __init__(self, *args):
        pygame.mixer.init()

        self.playlist = pygame.mixer.Channel(0)
        pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

        self.sounds = [
            self.load_file(filename) for filename in args
        ]
        self.current_sound = -1
        self.length_of_playlist = len(self.sounds)

        self.queue_next()

    @staticmethod
    def load_file(filename: str) -> pygame.mixer.Sound:
        return pygame.mixer.Sound("resources/music/" + filename)

    def add(self, filename):
        self.sounds.append(self.load_file(filename))
        self.length_of_playlist += 1

    def queue_next(self):
        self.current_sound = (self.current_sound + 1) % self.length_of_playlist
        self.playlist.queue(self.sounds[self.current_sound])
