from utils import FieldDescription, SquareContent, Square,\
    GameState


class Minesweeper:
    def get_neighbourhood(self, x, y):
        neighbourhood = []

        height = self.description.height
        width = self.description.width

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                if height > x >= 0 and width > y >= 0:
                    neighbourhood.append((x + dx, y + dy))
        return [self.field[i][j] for i, j in neighbourhood]

    def initialize_field(self):
        self.field = [[Square(SquareContent.NONE, False) for _ in range(self.description.width)]
                      for _ in range(self.description.height)]

    def initialize_cells(self):
        positions = [(i, j) for i in range(self.description.width) for j in range(self.description.height)]
        mines = random.sample(positions, self.description.mines)

        for x, y in mines:
            self.field[x][y] = Square(SquareContent.MINE, False, "*")

            for cell_x, cell_y in self.get_neighbourhood(x, y):
                cell = self.field[cell_x][cell_y]
                if cell.content == SquareContent.NONE:
                    cell.content = SquareContent.EMPTY
                    cell.text = str(int(cell.text) + 1) if cell.text else "0"

    def open_cell(self, x, y):
        cell = self.field[x][y]
        content = cell.content

        if content == SquareContent.MINE_FLAG or content == SquareContent.QUESTION_FLAG:
            return GameState.IDLE

        if content == SquareContent.EMPTY:
            cell.visible = True
            self.open_cells(filter(
                lambda e: e.content == SquareContent.EMPTY,
                self.get_neighbourhood(x, y)
            ))
        elif content == SquareContent.MINE:
            self.open_cells(filter(
                lambda e: e.content == SquareContent.MINE,
                self.field
            ))

    def __init__(self, description: FieldDescription):
        self.description = description
        self.field = []

        self.initialize_field()
        self.initialize_cells()
