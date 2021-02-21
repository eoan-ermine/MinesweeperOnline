import sys

import pygame
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication


def open_playlist_dialog(game):
    app = QApplication(sys.argv)

    dialog = EditPlaylistDialog(game)
    dialog.show()

    pygame.event.set_blocked(None)
    app.exec()
    pygame.event.set_allowed(None)


class EditPlaylistDialog(QDialog):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.music_subsystem = game.get_music_subsystem()

        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi("dialogues/forms/edit_playlist.ui", self)

        self.init_ui()
        self.init_signals()

    def init_ui(self):
        pass

    def init_signals(self):
        pass
