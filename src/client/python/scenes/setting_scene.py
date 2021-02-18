import pygame

from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher
from src.client.python.utils.group import Group
from src.client.python.utils.utils import terminate
from src.client.python.widgets.slider import Slider
from src.client.python.widgets.text import Text


class SettingScene(Scene):
    def __init__(self, *args, **kwargs):
        constants = {"title_text": "Settings", "font": pygame.font.Font(None, 30)}
        constants.update(**kwargs)

        super().__init__(*args, constants)

        self.volume_slider = None
        self.labels = None
        self.menu_labels = None

        self.settings = self.game.get_settings()
        self.music_subsystem = self.game.get_music_subsystem()

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        title_text = getattr(self, "title_text")
        font = getattr(self, "font")

        width = self.game.get_width()
        height = self.game.get_height()

        self.labels = Group("labels")

        volume_text = Text(font, "Музыка", 1, (0, 0, 0), self.labels)
        volume_text.set_center((width // 6), (height // 4))

        self.volume_slider = Slider((width // 6 + 70, height // 4 - 10), (300, 20), (255, 0, 0))

        title = Text(font, title_text, 1, (0, 0, 0), self.labels)
        title.set_center((width // 2), height // 15)

    def init_signals(self):
        self.volume_slider.connect("value_stabilized", lambda new: self.settings.set_value("music_volume", str(new))
                                                                   or self.music_subsystem.playlist.set_volume(
            new / 100))
        self.volume_slider.set_volume(int(self.settings.value("music_volume")))

    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.labels.draw(screen)
        self.volume_slider.draw(screen)

        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        dispatcher = EventDispatcher([self.volume_slider])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                dispatcher.dispatch_event(event)

            self.draw(screen)
            clock.tick(framerate)
