import pygame


class Text:
    def __init__(self, font, content, size, color):
        self.content = content
        self.size = size
        self.color = color

        self.font = font

        self.text = font.render(content, size, color)
        self.rect = self.text.get_rect()

    def set_center(self, center_x, center_y):
        self.rect = self.text.get_rect(center=(center_x, center_y))

    def draw(self, screen):
        screen.blit(self.text, self.rect)


class BorderedText(Text):
    def __init__(self, font, content, size, color, border_color):
        super().__init__(font, content, size, color)

        self.border_color = border_color
        self.border_state = False

    def set_border_enable(self, state):
        self.border_state = state

    def draw(self, screen):
        if self.border_state:
            border_rect = self.rect.inflate(5, 5)
            pygame.draw.rect(screen, self.border_color, border_rect)
        super().draw(screen)
