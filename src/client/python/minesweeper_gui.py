from utils.utils import FieldDescription
from utils.text import Text, BorderedText
from utils.group import Group
from utils.slider import Slider
from utils.event_dispatcher import EventDispatcher

import sys
import pygame

import win32api
import win32gui
import win32con

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

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("The Ultimate Minesweeper")

        self.start_menu()

    def single_game(self):
        pass

    def settings_menu(self):
        clock = pygame.time.Clock()

        title_text = "Settings"
        font = pygame.font.Font(None, 30)

        labels = Group("labels")
        menu_labels = Group("menu_labels")

        title = Text(font, title_text, 1, (0, 0, 0), labels)
        title.set_center((self.width // 2), self.height // 15)

        slider = Slider((self.width // 2, self.height // 2), (100, 100), (255, 0, 0))
        dispatcher = EventDispatcher([slider])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                dispatcher.dispatch_event(event)
                
            self.screen.fill((255, 255, 255))
            
            labels.draw(self.screen)
            slider.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.framerate)


    def start_menu(self):
        clock = pygame.time.Clock()

        title_text = "The Ultimate Minesweeper"

        font = pygame.font.Font(None, 30)

        labels = Group("labels")
        menu_labels = Group("menu_labels")

        play_label = BorderedText(font, "[ИГРАТЬ]", 1, (0, 0, 0), (20, 255, 23), labels, menu_labels)
        play_label.clicked = lambda e: self.single_game()

        settings_label = BorderedText(font, "[НАСТРОЙКИ]", 1, (0, 0, 0), (20, 255, 23), labels, menu_labels)
        settings_label.clicked = lambda e: self.settings_menu()

        exit_label = BorderedText(font, "[ВЫХОД]", 1, (0, 0, 0), (20, 255, 23), labels, menu_labels)
        exit_label.clicked = lambda e: self.terminate()

        menu_labels.invoke(lambda e: e.connect("focused", lambda k: k.set_border_enable(True)))

        background_color = (255, 255, 255)

        title = Text(font, title_text, 1, (0, 0, 0), labels)
        title.set_center((self.width // 2), self.height // 15)

        for i, string in enumerate(menu_labels):
            string.set_center((self.width // 2), (self.height // 3 + i * 50))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = event.pos

                    label = menu_labels.collidepoint(mouse_position)
                    if label:
                        label.focused(label)
                    else:
                        menu_labels.invoke(lambda e: e.set_border_enable(False))

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = event.pos
                    label = menu_labels.collidepoint(mouse_position)
                    if label: label.clicked(label)

            self.screen.fill(background_color)
            labels.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.framerate)
    
    @staticmethod
    def terminate():
        clock = pygame.time.Clock()
        pygame.mixer.music.load("src/client/python/resources/final_message.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            clock.tick(30)

        pygame.mixer.music.load("src/client/python/resources/ending.mp3")
        pygame.mixer.music.play()

        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)

        clock = pygame.time.Clock()
        i = 255
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pass
            win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), round(i), win32con.LWA_ALPHA)
            i = max(0, i - 1.5)
            if i == 0:
                break
            clock.tick(30)
            pygame.display.update()

        pygame.quit()
        sys.exit(0)
