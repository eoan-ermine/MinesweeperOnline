from utils import FieldDescription
from text import Text, BorderedText

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

    def start_menu(self):
        clock = pygame.time.Clock()

        title_text = "The Ultimate Minesweeper"
        menu_text = [
            "[ИГРАТЬ]",
            "[НАСТРОЙКИ]",
            "[ВЫХОД]"
        ]

        background_color = (255, 255, 255)
        font = pygame.font.Font(None, 30)

        title = Text(font, title_text, 1, (0, 0, 0))
        title.set_center((self.width // 2), self.height // 15)

        menu_labels = []
        for i, line in enumerate(menu_text):
            string = BorderedText(font, line, 1, (0, 0, 0), (20, 255, 23))
            string.set_center((self.width // 2), (self.height // 3 + i * 50))
            menu_labels.append(string)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()
                    for label in menu_labels:
                        if label.rect.collidepoint(*mouse_position):
                            label.set_border_enable(True)
                        else:
                            label.set_border_enable(False)

            self.screen.fill(background_color)

            title.draw(self.screen)
            for label in menu_labels:
                label.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.framerate)

    @staticmethod
    def terminate():
        clock = pygame.time.Clock()
        pygame.mixer.music.load("final_message.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            clock.tick(30)

        pygame.mixer.music.load("ending.mp3")
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
