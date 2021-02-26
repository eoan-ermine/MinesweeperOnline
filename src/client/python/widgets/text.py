import pygame

from src.client.python.utils.pobject import Object


class Text(Object):
    def __init__(self, font, content, size, color, *groups):
        super().__init__(["clicked", "mouse_motion"])
        self.connect("clicked", lambda event: self.check_collide(event))

        for group in groups:
            group.add(self)

        self.content = content
        self.size = size
        self.color = color

        self.font = font

        self.text = font.render(content, size, color)
        self.rect = self.text.get_rect()

    def check_collide(self, event):
        pos = event.pos
        return self.rect.collidepoint(*pos)

    def set_center(self, center_x, center_y):
        self.rect = self.text.get_rect(center=(center_x, center_y))

    def set_topleft(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_content(self, content):
        self.text = self.font.render(content, self.size, self.color)

    def draw(self, screen):
        screen.blit(self.text, self.rect)


class BorderedText(Text):
    def __init__(self, font, content, size, color, border_color, *groups):
        super().__init__(font, content, size, color, *groups)
        self.connect("mouse_motion", lambda event: self.on_focused(event))

        self.border_color = border_color
        self.border_state = False

    def on_focused(self, event):
        self.set_border_enable(self.check_collide(event))

    def set_border_enable(self, state):
        self.border_state = state

    def draw(self, screen):
        if self.border_state:
            border_rect = self.rect.inflate(5, 5)
            pygame.draw.rect(screen, self.border_color, border_rect)
        super().draw(screen)
