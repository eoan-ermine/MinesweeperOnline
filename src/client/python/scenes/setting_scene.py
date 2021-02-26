import pygame

from src.client.python.dialogues.edit_playlist import open_playlist_dialog
from src.client.python.scenes.scene import Scene
from src.client.python.utils.event_dispatcher import EventDispatcher
from src.client.python.utils.group import Group
from src.client.python.utils.utils import terminate
from src.client.python.widgets.button import Button
from src.client.python.widgets.slider import Slider
from src.client.python.widgets.text import Text, BorderedText


class SettingScene(Scene):
    def __init__(self, *args, **kwargs):
        constants = {"title_text": "Settings", "font": pygame.font.Font(None, 30)}
        constants.update(**kwargs)

        super().__init__(*args, constants)

        self.volume_slider = None
        self.button = None
        self.back_label = None

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
        volume_text.set_topleft((width // 6) - 40, (height // 4 - 10))
        self.volume_slider = Slider((width // 6 + 70, height // 4 - 10), (300, 20), (255, 0, 0))

        playlist_text = Text(font, "Плейлист", 1, (0, 0, 0), self.labels)
        playlist_text.set_topleft((width // 6) - 40, (height // 4 + 20))
        self.button = Button((width // 6 + 70, height // 4 + 20), (300, 20), "Редактировать")
        self.button.connect("mouse_up", lambda e: open_playlist_dialog(self.game))

        title = Text(font, title_text, 1, (0, 0, 0), self.labels)
        title.set_center((width // 2), height // 15)

        self.back_label = BorderedText(font, "[НАЗАД]", 1, (0, 0, 0), (20, 255, 23), self.labels)
        self.back_label.set_center((width // 2), height - 50)

    def init_signals(self):
        self.volume_slider.connect("value_stabilized", lambda new: self.settings.set_value("music_volume", str(new))
                                                                   or self.music_subsystem.playlist.set_volume(new / 100
                                                                                                               ))
        self.volume_slider.set_volume(int(self.settings.value("music_volume")))

        self.back_label.connect("clicked", lambda e: self.stop())
        self.back_label.connect("focused", lambda k: k.set_border_enable(True))

    def draw(self, screen):
        screen.fill((255, 255, 255))

        self.labels.draw(screen)
        self.volume_slider.draw(screen)
        self.button.draw(screen)

        pygame.display.flip()

    def run(self, screen, framerate):
        clock = pygame.time.Clock()
        dispatcher = EventDispatcher([self.volume_slider, self.button, self.back_label], self.game)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if dispatcher.dispatch_event(event):
                    return

            self.draw(screen)
            clock.tick(framerate)
