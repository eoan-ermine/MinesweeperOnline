import pygame


class MusicSubsystem:
    def __init__(self, *args):
        pygame.mixer.init()
        self.playlist = pygame.mixer.Channel(0)
        for filename in args:
            self.load(filename)

    def load(self, filename):
        self.playlist.queue(
            pygame.mixer.Sound("resources/music/" + filename)
        )
