import pygame
from pygame import Rect

from utils.pobject import Object


class Slider(Object):
    def __init__(self, topleft, size, color):
        super().__init__(["clicked"])
        self.clicked = lambda event: self.clicked_handler(event)

        self.volume = 0
        self.color = color
        self.border_rect = Rect(topleft, size)

        self.moving = False

        self.ppv = self.border_rect.width // 100

    def collidepoint(self, point):
        if self.border_rect.collidepoint(*point):
            return self
        return None

    def clicked_handler(self, event):
        position = event.pos
        self.set_volume((position[0] - self.border_rect.x) // self.ppv)

    def set_volume(self, volume):
        self.volume = min(volume if volume >= 0 else 0, 100)

    def add_volume(self, volume):
        self.volume = min(self.volume + volume, 100)

    def draw(self, screen):
        volume_rect = self.border_rect.copy()
        volume_rect.width = self.ppv * self.volume
        pygame.draw.rect(
            screen,
            self.color,
            volume_rect,
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            self.border_rect,
            1
        )
