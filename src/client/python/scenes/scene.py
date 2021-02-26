import pygame

CLOSE_SCENE_EVENT = pygame.USEREVENT + 2


class Scene:
    def __init__(self, game, constants):
        for ident, value in constants.items():
            setattr(self, ident, value)
        self.game = game

    def run(self, screen, framerate):
        pass

    def stop(self):
        pygame.event.post(pygame.event.Event(CLOSE_SCENE_EVENT))
