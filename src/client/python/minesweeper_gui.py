class FieldDescription:
    def __init__(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines


presets = {
    "Simple": FieldDescription(9, 9, 10),
    "Intermediate": FieldDescription(16, 16, 40),
    "Expert": FieldDescription(30, 16, 99),
}


class MinesweeperGUI:
    pass
