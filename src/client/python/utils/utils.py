import sys
import tkinter as tk
from enum import Enum
from tkinter import filedialog

import pygame
import win32api
import win32con
import win32gui


class FieldDescription:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines


class SquareContent(Enum):
    MINE = 1,
    EMPTY = 2,
    MINE_FLAG = 3,
    QUESTION_FLAG = 4

    def describe(self):
        return self.name

    def __repr__(self):
        return self.describe()

    def __str__(self):
        return self.__repr__()


class Square:
    def __init__(self, x, y, content: SquareContent, visible: bool, value: int = None):
        self.x = x
        self.y = y

        self.content = content
        self.content.value = value

        self.visible = visible

    def __iter__(self):
        return iter((self.x, self.y))

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"Square({self.x}, {self.y}, {self.content.__str__()}, {self.visible})"


class GameState:
    WIN = 0,
    FAIL = 1,
    IDLE = 2


def terminate():
    clock = pygame.time.Clock()

    pygame.mixer.music.load("resources/final_message.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        clock.tick(30)

    pygame.mixer.music.load("resources/ending.mp3")
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


def import_music():
    root = tk.Tk()
    root.withdraw()

    filepath = tk.filedialog.askopenfilenames(
        title="Import music", filetypes=[
            ("music", ".mp3"),
            ("music", ".ogg"),
        ]
    )
    return list(filepath)
