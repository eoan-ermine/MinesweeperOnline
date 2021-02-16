import pygame
from pygame import Rect

from src.client.python.utils.pobject import Object


class Slider(Object):
    def __init__(self, topleft, size, color):
        super().__init__(["mouse_down", "mouse_up", "mouse_motion", "value_changed"])
        
        self.connect("mouse_down", lambda event: self.clicked_handler(event))
        self.connect("mouse_motion", lambda event: self.motion_handler(event))
        self.connect("mouse_up", lambda _: self.set_moving(False))

        self.volume = 0
        self.color = color
        self.border_rect = Rect(topleft, size)

        self.moving = False

        self.ppv = self.border_rect.width // 100

    def set_moving(self, state):
        self.moving = state

    def motion_handler(self, event):
        if self.moving:
            self.change_volume_by_pos(event.pos)

    def change_volume_by_pos(self, pos):
        self.set_volume((pos[0] - self.border_rect.x) // self.ppv)

    def clicked_handler(self, event):
        position = event.pos
        if self.border_rect.collidepoint(position):
            self.moving = True
            self.change_volume_by_pos(position)

    def set_volume(self, volume):
        self.volume = min(volume if volume >= 0 else 0, 100)
        self.signal("value_changed", self.volume)

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
