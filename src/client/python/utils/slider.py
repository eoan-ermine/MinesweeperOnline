import pygame
from pygame import Rect

from utils.pobject import Object


class Slider(Object):
    def __init__(self, topleft, size, color):
        super().__init__(["mouse_down", "mouse_up", "mouse_motion"])
        
        self.connect("mouse_down", lambda event: self.clicked_handler(event))
        self.connect("mouse_motion", lambda event: self.motion_handler(event))
        self.connect("mouse_up", lambda _: self.set_moving(False))

        self.volume = 0
        self.color = color
        self.border_rect = Rect(topleft, size)

        self.moving = False

        self.ppv = self.border_rect.width // 100

    def collidepoint(self, point):
        if self.border_rect.collidepoint(*point):
            return self
        return None

    def set_moving(self, state):
        self.moving = state

    def motion_handler(self, event):
        if self.moving:
            self.clicked_handler(event)

    def clicked_handler(self, event):
        position = event.pos
        self.set_volume((position[0] - self.border_rect.x) // self.ppv)
        self.moving = True

    def set_volume(self, volume):
        self.volume = min(volume if volume >= 0 else 0, 100)

    def add_volume(self, volume):
        self.set_volume(self.volume + volume)

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
