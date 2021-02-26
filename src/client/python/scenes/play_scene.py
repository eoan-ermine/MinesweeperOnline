import pygame

from src.client.python.minesweeper import Minesweeper
from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher
from src.client.python.utils.group import Group
from src.client.python.utils.utils import terminate
from src.client.python.widgets.cell import Cell


class PlayScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)

        self.minesweeper = Minesweeper(self.description)

        self.width = self.description.width
        self.height = self.description.height

        self.width_x = self.width * 50
        self.height_y = self.height * 50

        self.cells = Group("cells")

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        self.game.screen = pygame.display.set_mode((self.width_x, self.height_y))
        for i in range(self.width):
            for j in range(self.height):
                self.cells.add(Cell((i * 50, j * 50), (50, 50), self.minesweeper, self.minesweeper.at(i, j)))

    def init_signals(self):
        self.cells.invoke(lambda e: e.connect("mouse_up", lambda _: self.cells.invoke(lambda j: j.update_square())))

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.cells.draw(screen)
        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        dispatcher = EventDispatcher(self.cells, self.game)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                dispatcher.dispatch_event(event)

            self.draw(screen)
            clock.tick(framerate)
