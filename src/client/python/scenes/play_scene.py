import pygame

from src.client.python.minesweeper import Minesweeper
from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher
from src.client.python.utils.utils import terminate
from src.client.python.widgets.cell import Cell


class PlayScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)

        self.minesweeper = Minesweeper(self.description, self)

        self.width = self.description.width
        self.height = self.description.height

        self.width_x = self.width * 50 + 200
        self.height_y = self.height * 50

        self.cells = []

        self.init_ui()

    def update_square(self, x, y):
        self.cells[y][x].update_square()

    def init_ui(self):
        self.game.screen = pygame.display.set_mode((self.width_x, self.height_y))
        for j in range(self.height):
            self.cells.append([Cell((i * 50, j * 50), (50, 50), self.minesweeper, self.minesweeper.at(i, j))
                               for i in range(self.width)])

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for sublist in self.cells:
            for cell in sublist:
                cell.draw(screen)

        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        dispatcher = EventDispatcher([item for sublist in self.cells for item in sublist], self.game)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                dispatcher.dispatch_event(event)

            self.draw(screen)
            clock.tick(framerate)
