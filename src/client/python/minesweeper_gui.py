from os import listdir
from os.path import isfile, join

import pygame

from src.client.python.music.music import MusicSubsystem
from src.client.python.scenes.menu_scene import MenuScene
from src.client.python.settings.settings import Format, Settings
from src.client.python.utils.utils import load_image


class MinesweeperGUI:
    def __init__(self, width, height, framerate):
        self.width = width
        self.height = height
        self.framerate = framerate

        self.screen = None
        self.settings = Settings(Format.IniFormat, "settings.ini")

        self.settings.set_value("music_volume", self.settings.value("music_volume", "100"))

        self.music_subsystem = MusicSubsystem(
            *[f for f in listdir("resources/music") if isfile(join("resources/music", f))]
        )
        self.music_subsystem.playlist.set_volume(int(self.settings.value("music_volume", 100)) / 100)

    def run(self):
        pygame.init()

        pygame.display.set_icon(load_image("icon.png"))
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Ultimate Minesweeper")

        MenuScene(self).run(self.screen, self.framerate).run()

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

    def get_music_subsystem(self):
        return self.music_subsystem
