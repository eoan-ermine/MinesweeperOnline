import pygame

from src.client.python.minesweeper import Minesweeper
from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher, RETURN_FROM_DISPATCHER
from src.client.python.utils.group import Group
from src.client.python.utils.utils import GameState
from src.client.python.widgets.cell import Cell
from src.client.python.widgets.text import Text, BorderedText

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
        self.original_size = self.game.screen.get_size()

        self.width = self.description.width
        self.height = self.description.height

        self.squares_width_x = self.width * 50
        self.width_x = self.squares_width_x + 220

        self.height_y = self.height * 50

        self.current_status = None
        self.status_label = None

        self.restart_label = None
        self.exit_label = None

        self.cells = None
        self.labels = None

        self.init_ui()
        self.init_signals()

    def update_square(self, x, y):
        self.cells[y][x].update_square()

    def update_current_status(self, new_state):
        self.current_status.set_content(STATUS_MACHINE[new_state])

    def init_ui(self):
        self.game.screen = pygame.display.set_mode((self.width_x, self.height_y))

        self.cells = []
        self.labels = Group("labels")

        self.current_status = Text(self.indicator_font, "None", 1, (0, 0, 0), self.labels)
        self.status_label = Text(self.indicator_font, "Статус:", 1, (0, 0, 0), self.labels)

        self.restart_label = BorderedText(self.indicator_font, "[Рестарт]", 1, (0, 0, 0), (20, 255, 23),
                                          self.labels)
        self.exit_label = BorderedText(self.indicator_font, "[Вернуться в меню]", 1, (0, 0, 0), (20, 255, 23),
                                       self.labels)

        for j in range(self.height):
            self.cells.append([Cell((i * 50, j * 50), (50, 50), self.minesweeper, self.minesweeper.at(i, j), self.font)
                               for i in range(self.width)])

        self.status_label.set_topleft(self.squares_width_x + 10, 20)
        self.current_status.set_topleft(self.squares_width_x + 90, 20)

        self.restart_label.set_topleft(self.squares_width_x + 10, self.height_y - 60)
        self.exit_label.set_topleft(self.squares_width_x + 10, self.height_y - 30)

    def init_signals(self):
        self.restart_label.connect("clicked", lambda e: self.restart())
        self.exit_label.connect("clicked", lambda e: self.stop())

    def restart(self):
        self.minesweeper = Minesweeper(self.description, self)

        self.init_ui()
        self.init_signals()

        pygame.event.post(pygame.event.Event(RETURN_FROM_DISPATCHER))

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for sublist in self.cells:
            for cell in sublist:
                cell.draw(screen)
        self.labels.draw(screen)

        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        dispatcher = EventDispatcher(
            [item for sublist in self.cells for item in sublist] + list(self.labels.__iter__()), self.game)
        while True:
            for event in pygame.event.get():
                dispatcher_answer = dispatcher.dispatch_event(event)
                if dispatcher_answer == RETURN_FROM_DISPATCHER:
                    return self.run(screen, framerate)
                elif dispatcher.dispatch_event(event):
                    self.game.screen = pygame.display.set_mode(self.original_size)
                    return

            self.draw(screen)
            clock.tick(framerate)
