from utils import FieldDescription


class Minesweeper:
    def initialize_field(self):
        self.field = [[-1 for _ in range(self.description.width)] for _ in range(self.description.height)]

    def initialize_mines(self):
        positions = [(i, j) for i in range(self.description.width) for j in range(self.description.height)]
        mines = random.sample(positions, self.description.mines)

        for mine in mines:
            self.field[mine[0]][mine[1]] = 1

    def __init__(self, description: FieldDescription):
        self.description = description
        self.field = []

        self.initialize_field()
        self.initialize_mines()
