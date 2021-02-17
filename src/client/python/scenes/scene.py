class Scene:
    def __init__(self, constants):
        for ident, value in constants.items():
            setattr(self, ident, value)

    def run(self, screen, framerate):
        pass
