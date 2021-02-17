class Scene:
    def __init__(self, game, constants):
        for ident, value in constants.items():
            setattr(self, ident, value)
        self.game = game

    def run(self, screen, framerate):
        pass
