import pygame
from pygame import Rect

from src.client.python.utils.pobject import Object
from src.client.python.utils.utils import Square, Flag, SquareContent
from src.client.python.widgets.text import Text

NEXT_FLAG_STATE = {Flag.NONE_FLAG: Flag.MINE_FLAG, Flag.MINE_FLAG: Flag.QUESTION_FLAG,
                   Flag.QUESTION_FLAG: Flag.NONE_FLAG}


def get_text_color(square: Square):
    if square.flag != Flag.NONE_FLAG:
        return (255, 255, 0) if square.flag == Flag.QUESTION_FLAG else (255, 0, 0)
    else:
        return (0, 255, 0) if square.content == SquareContent.EMPTY else (255, 0, 0)


def get_text_content(square: Square):
    if square.flag != Flag.NONE_FLAG:
        return "?" if square.flag == Flag.QUESTION_FLAG else "F"
    if not square.visible:
        return " "

    if square.content == SquareContent.EMPTY:
        return str(square.value) if square.value else "."
    else:
        return "*"


class Cell(Object):
    def __init__(self, topleft, size, game, square: Square, font):
        super().__init__(["mouse_down", "mouse_up"])

        self.font = font

        self.connect("mouse_down", lambda event: self.mouse_down_handler(event))
        self.connect("mouse_up", lambda _: self.mouse_up_handler())

        self.connect("mouse_up", lambda event: self.left_click_handler(event) if event.button == 1 else None)
        self.connect("mouse_up", lambda event: self.right_click_handler(event) if event.button == 3 else None)

        self.game = game

        self.border_rect = Rect(topleft, size)
        self.text = None

        self.square = square
        self.update_square()

        self.clicked = False

    def update_square(self):
        self.text = Text(self.font, get_text_content(self.square), 1, get_text_color(self.square))
        self.text.set_center(self.border_rect.centerx, self.border_rect.centery)

    def set_flag(self, flag: Flag):
        self.square.set_flag(flag)
        self.update_square()

    def change_clicked_state(self, state):
        self.clicked = state

    def mouse_down_handler(self, event):
        position = event.pos
        collide = self.border_rect.collidepoint(position)
        if collide:
            self.change_clicked_state(True)
        return collide

    def mouse_up_handler(self):
        if self.clicked:
            return self.change_clicked_state(False) or True
        return False

    def left_click_handler(self, _):
        state = self.game.open_cell(self.square.x, self.square.y)
        return state

    def right_click_handler(self, _):
        self.set_flag(NEXT_FLAG_STATE[self.square.flag])

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            self.border_rect,
            1
        )
        if self.text:
            self.text.draw(screen)
