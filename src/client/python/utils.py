from enum import Enum


class FieldDescription:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines


class SquareContent:
    NONE = 0,
    MINE = 1,
    EMPTY = 2,
    MINE_FLAG = 3,
    QUESTION_FLAG = 4


class Square:
    def __init__(self, content: SquareContent, visible: bool, text: str = ""):
        self.content = content
        self.text = text
        self.visible = visible


class GameState:
    WIN = 0,
    FAIL = 1,
    IDLE = 2
