import random

from src.client.python.utils.utils import Square, SquareContent, GameState, FieldDescription, Flag


class Minesweeper:
    def get_neighbourhood(self, x, y):
        neighbourhood = []

        height = self.description.height
        width = self.description.width

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if width > x + dx >= 0 and height > y + dy >= 0:
                    neighbourhood.append((x + dx, y + dy))
        return [self.field[j][i] for i, j in neighbourhood]

    def initialize_field(self):
        self.field = [[Square(i, j, SquareContent.EMPTY, False, 0) for i in range(self.description.width)]
                      for j in range(self.description.height)]

    def initialize_cells(self, exclude):
        positions = [(i, j) for i in range(self.description.width) for j in range(self.description.height)]
        mines = random.sample([e for e in positions if (e[0], e[1]) not in exclude], self.description.mines)

        for x, y in mines:
            self.field[y][x].set_content(SquareContent.MINE)

            for cell_x, cell_y in self.get_neighbourhood(x, y):
                cell = self.field[cell_y][cell_x]
                if cell.content == SquareContent.EMPTY:
                    cell.value = cell.value + 1 if cell.value else 1

    def open_cells(self, predicate, cells):
        cells = filter(predicate, cells)
        for e in cells:
            self.open_cell(e.x, e.y)

    def open_around(self, x, y):
        neighbourhood = self.get_neighbourhood(x, y)
        mines_around = len(list(filter(lambda e: e.content == SquareContent.MINE, neighbourhood)))
        if mines_around == 0:
            self.open_cells(lambda e: e.content == SquareContent.EMPTY and not e.visible, neighbourhood)

    def get_flat_field(self):
        return [item for sublist in self.field for item in sublist]

    def check_win(self):
        not_opened_cells = list(
            filter(lambda e: e.content == SquareContent.EMPTY and not e.visible,
                   self.get_flat_field())
        )
        return len(not_opened_cells) == 0

    def open_cell(self, x, y):
        cell = self.field[y][x]
        content = cell.content

        if self.first_move:
            self.initialize_cells([(e.x, e.y) for e in self.get_neighbourhood(x, y)] + [(x, y)])
            self.first_move = False

        if cell.can_open():
            cell.visible = True
            if content == SquareContent.EMPTY:
                self.open_around(x, y)
                if self.check_win():
                    return GameState.WIN
            elif content == SquareContent.MINE:
                self.open_cells(lambda e: True, self.get_flat_field())
                return GameState.FAIL

        return GameState.IDLE

    def set_flag(self, x, y, flag: Flag):
        cell = self.field[x][y]
        cell.set_flag(flag)

    def at(self, x, y) -> Square:
        return self.field[y][x]

    def __init__(self, description: FieldDescription):
        self.description = description
        self.field = []

        self.initialize_field()
        self.first_move = True
