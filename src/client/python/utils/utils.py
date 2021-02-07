from enum import Enum


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
    def __init__(self, x, y, content: SquareContent, visible: bool, value: int=None):
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
