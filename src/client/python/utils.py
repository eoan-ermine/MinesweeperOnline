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

    def __repr__(self):
        if self == SquareContent.NONE:
            return "NONE"
        elif self == SquareContent.MINE:
            return "MINE"
        elif self == SquareContent.EMPTY:
            return "EMPTY"
        elif self == SquareContent.MINE_FLAG:
            return "MINE_FLAG"
        elif self == SquareContent.QUESTION_FLAG:
            return "QUESTION_FLAG"

    def __str__(self):
        return self.__repr__()


class Square:
    def __init__(self, x, y, content: SquareContent, visible: bool, text: str = ""):
        self.x = x
        self.y = y

        self.content = content
        self.text = text
        self.visible = visible

    def __iter__(self):
        return iter((self.x, self.y))

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"Square({self.x}, {self.y}, {self.content.__str__()}, {self.text}, {self.visible})"


class GameState:
    WIN = 0,
    FAIL = 1,
    IDLE = 2
