import pygame

from src.client.python.scenes.play_scene import PlayScene
from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher
from src.client.python.utils.group import Group
from src.client.python.utils.utils import presets
from src.client.python.widgets.text import BorderedText, Text


class SetupScene(Scene):
    def __init__(self, *args, **kwargs):
        constants = {"title_text": "Выберите сложность", "font": pygame.font.Font(None, 30)}
        constants.update(**kwargs)
        super().__init__(*args, constants)

        self.labels = None
        self.menu_labels = None

        self.simple_label = None
        self.intermediate_label = None
        self.expert_label = None

        self.back_label = None

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        title_text = getattr(self, "title_text")
        font = getattr(self, "font")

        width = self.game.get_width()
        height = self.game.get_height()

        self.labels = Group("labels")
        self.menu_labels = Group("menu_labels")

        self.simple_label = BorderedText(font, "[Simple]", 1, (0, 0, 0), (20, 255, 23), self.labels, self.menu_labels)
        self.intermediate_label = BorderedText(font, "[Intermediate]", 1, (0, 0, 0), (20, 255, 23), self.labels,
                                               self.menu_labels)
        self.expert_label = BorderedText(font, "[Expert]", 1, (0, 0, 0), (20, 255, 23), self.labels, self.menu_labels)

        title = Text(font, title_text, 1, (0, 0, 0), self.labels)
        title.set_center((width // 2), height // 15)

        for i, string in enumerate(self.menu_labels):
            string.set_center((width // 2), (height // 3 + i * 50))

        self.back_label = BorderedText(font, "[НАЗАД]", 1, (0, 0, 0), (20, 255, 23), self.labels)
        self.back_label.set_center((width // 2), height - 50)

    def init_signals(self):
        screen = self.game.get_screen()
        framerate = self.game.get_framerate()

        self.simple_label.connect("clicked", lambda e: PlayScene(self.game, description=presets["Simple"]).run(
            screen, framerate
        ))
        self.intermediate_label.connect("clicked",
                                        lambda e: PlayScene(self.game, description=presets["Intermediate"]).run(
                                            screen, framerate
                                        ))
        self.expert_label.connect("clicked", lambda e: PlayScene(self.game, description=presets["Expert"]).run(
            screen, framerate
        ))
        self.menu_labels.invoke(lambda e: e.connect("focused", lambda k: k.set_border_enable(True)))

        self.back_label.connect("clicked", lambda e: self.stop())
        self.back_label.connect("focused", lambda k: k.set_border_enable(True))

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.labels.draw(screen)
        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        dispatcher = EventDispatcher(self.labels, self.game)
        while True:
            for event in pygame.event.get():
                if dispatcher.dispatch_event(event):
                    return

            self.draw(screen)
            clock.tick(framerate)
