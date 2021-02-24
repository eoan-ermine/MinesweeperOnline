import pygame

from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher
from src.client.python.utils.utils import terminate


class PlayScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        dispatcher = EventDispatcher([], self.game)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                dispatcher.dispatch_event(event)

            self.draw(screen)
            clock.tick(framerate)
