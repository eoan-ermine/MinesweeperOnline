import pygame
from pygame import Rect

from src.client.python.utils.pobject import Object
from src.client.python.widgets.text import Text


class Button(Object):
    def __init__(self, topleft, size, text=None, text_color=(0, 0, 0)):
        super().__init__(["mouse_down", "mouse_up"])

        self.connect("mouse_down", lambda event: self.mouse_down_handler(event))
        self.connect("mouse_up", lambda _: self.mouse_up_handler())

        self.color_light = (170, 170, 170)
        self.color_dark = (100, 100, 100)
        self.color = self.color_dark

        self.border_rect = Rect(topleft, size)

        self.text = None
        self.text_color = text_color
        if text:
            self.text = Text(pygame.font.Font(None, 30), text, 1, text_color)
            self.text.set_center(self.border_rect.centerx, self.border_rect.centery)

        self.clicked = False

    def change_clicked_state(self, state):
        self.clicked = state
        if state:
            self.color = self.color_light
        else:
            self.color = self.color_dark

    def mouse_down_handler(self, event):
        position = event.pos
        collide = self.border_rect.collidepoint(position)
        if collide:
            self.change_clicked_state(True)
        return collide

    def mouse_up_handler(self):
        if self.clicked:
            self.change_clicked_state(False)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.color,
            self.border_rect
        )
        if self.text:
            self.text.draw(screen)
