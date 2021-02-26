import pygame

from src.client.python.minesweeper import Minesweeper
from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher
from src.client.python.utils.group import Group
from src.client.python.utils.utils import terminate, GameState
from src.client.python.widgets.cell import Cell
from src.client.python.widgets.text import Text

STATUS_MACHINE = {
    GameState.IDLE: "В игре",
    GameState.WIN: "Победа",
    GameState.FAIL: "Поражение"
}


class PlayScene(Scene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, kwargs)

        self.font = pygame.font.Font(None, 60)
        self.indicator_font = pygame.font.Font(None, 30)

        self.minesweeper = Minesweeper(self.description, self)
        self.original_screen = self.game.screen

        self.width = self.description.width
        self.height = self.description.height

        self.squares_width_x = self.width * 50
        self.width_x = self.squares_width_x + 220

        self.height_y = self.height * 50

        self.cells = []
        self.labels = Group("labels")

        self.current_status = Text(self.indicator_font, "None", 1, (0, 0, 0), self.labels)
        self.status_label = Text(self.indicator_font, "Статус:", 1, (0, 0, 0), self.labels)

        self.exit_label = Text(self.indicator_font, "Вернуться в меню", 1, (0, 0, 0), self.labels)

        self.init_ui()

    def update_square(self, x, y):
        self.cells[y][x].update_square()

    def update_current_status(self, new_state):
        self.current_status.set_content(STATUS_MACHINE[new_state])

    def init_ui(self):
        self.game.screen = pygame.display.set_mode((self.width_x, self.height_y))
        for j in range(self.height):
            self.cells.append([Cell((i * 50, j * 50), (50, 50), self.minesweeper, self.minesweeper.at(i, j), self.font)
                               for i in range(self.width)])
        self.status_label.set_topleft(self.squares_width_x + 10, 20)
        self.current_status.set_topleft(self.squares_width_x + 90, 20)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for sublist in self.cells:
            for cell in sublist:
                cell.draw(screen)
        self.labels.draw(screen)

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
