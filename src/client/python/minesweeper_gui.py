import pygame

from src.client.python.scenes.menu_scene import MenuScene
from src.client.python.scenes.setting_scene import SettingScene
from src.client.python.settings.settings import Format, Settings
from src.client.python.utils.group import Group
from src.client.python.widgets.text import BorderedText, Text
from src.client.python.utils.utils import terminate, FieldDescription

presets = {
    "Simple": FieldDescription(9, 9, 10),
    "Intermediate": FieldDescription(16, 16, 40),
    "Expert": FieldDescription(30, 16, 99),
}


class MinesweeperGUI:
    def __init__(self, width, height, framerate):
        self.width = width
        self.height = height
        self.framerate = framerate

        self.screen = None
        self.settings = Settings(Format.IniFormat, "settings.ini")

        self.settings.set_value("music_volume", self.settings.value("music_volume", "100"))

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Ultimate Minesweeper")

        MenuScene(self).run(self.screen, self.framerate).run()

    def single_game(self):
        pass

    def start_menu(self):
        clock = pygame.time.Clock()

        title_text = "The Ultimate Minesweeper"

        font = pygame.font.Font(None, 30)

        labels = Group("labels")
        menu_labels = Group("menu_labels")

        play_label = BorderedText(font, "[ИГРАТЬ]", 1, (0, 0, 0), (20, 255, 23), labels, menu_labels)
        play_label.connect("clicked", lambda e: self.single_game())

        settings_label = BorderedText(font, "[НАСТРОЙКИ]", 1, (0, 0, 0), (20, 255, 23), labels, menu_labels)
        settings_label.connect("clicked",
                               lambda e: SettingScene(width=self.width, height=self.height, settings=self.settings).run(
                                   self.screen,
                                   self.framerate))

        exit_label = BorderedText(font, "[ВЫХОД]", 1, (0, 0, 0), (20, 255, 23), labels, menu_labels)
        exit_label.connect("clicked", lambda e: terminate())

        menu_labels.invoke(lambda e: e.connect("focused", lambda k: k.set_border_enable(True)))

        background_color = (255, 255, 255)

        title = Text(font, title_text, 1, (0, 0, 0), labels)
        title.set_center((self.width // 2), self.height // 15)

        for i, string in enumerate(menu_labels):
            string.set_center((self.width // 2), (self.height // 3 + i * 50))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = event.pos

                    label = menu_labels.collidepoint(mouse_position)
                    if label:
                        label.signal("focused", label)
                    else:
                        menu_labels.invoke(lambda e: e.set_border_enable(False))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = event.pos
                    label = menu_labels.collidepoint(mouse_position)
                    if label: label.signal("clicked", label)

            self.screen.fill(background_color)
            labels.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.framerate)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_screen(self):
        return self.screen

    def get_framerate(self):
        return self.framerate

    def get_settings(self):
        return self.settings
