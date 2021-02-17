import pygame

from src.client.python.scenes.scene import Scene
from src.client.python.scenes.setting_scene import SettingScene
from src.client.python.utils.group import Group
from src.client.python.utils.utils import terminate
from src.client.python.widgets.text import BorderedText, Text


class MenuScene(Scene):
    def __init__(self, *args, **kwargs):
        constants = {"title_text": "The Ultimate Minesweeper", "font": pygame.font.Font(None, 30)}
        constants.update(**kwargs)
        super().__init__(*args, constants)

        self.labels = None
        self.menu_labels = None

        self.play_label = None
        self.settings_label = None
        self.exit_label = None

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        title_text = getattr(self, "title_text")
        font = getattr(self, "font")

        width = self.game.get_width()
        height = self.game.get_height()

        self.labels = Group("labels")
        self.menu_labels = Group("menu_labels")

        self.play_label = BorderedText(font, "[ИГРАТЬ]", 1, (0, 0, 0), (20, 255, 23), self.labels, self.menu_labels)
        self.settings_label = BorderedText(font, "[НАСТРОЙКИ]", 1, (0, 0, 0), (20, 255, 23), self.labels, self.menu_labels)
        self.exit_label = BorderedText(font, "[ВЫХОД]", 1, (0, 0, 0), (20, 255, 23), self.labels, self.menu_labels)

        title = Text(font, title_text, 1, (0, 0, 0), self.labels)
        title.set_center((width // 2), height // 15)

        for i, string in enumerate(self.menu_labels):
            string.set_center((width // 2), (height // 3 + i * 50))

    def init_signals(self):
        self.play_label.connect("clicked", lambda e: print("No action"))
        self.settings_label.connect("clicked",
                                    lambda e: SettingScene(self.game).run(
                                        self.game.get_screen(), self.game.get_framerate()
                                    ))
        self.exit_label.connect("clicked", lambda e: terminate())
        self.menu_labels.invoke(lambda e: e.connect("focused", lambda k: k.set_border_enable(True)))

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.labels.draw(screen)
        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = event.pos

                    label = self.menu_labels.collidepoint(mouse_position)
                    if label:
                        label.signal("focused", label)
                    else:
                        self.menu_labels.invoke(lambda e: e.set_border_enable(False))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = event.pos
                    label = self.menu_labels.collidepoint(mouse_position)
                    if label:
                        label.signal("clicked", label)

            self.draw(screen)
            clock.tick(framerate)