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

        self.game = game
        self.music_subsystem = game.get_music_subsystem()

        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi("dialogues/forms/edit_playlist.ui", self)

        self.init_ui()
        self.init_signals()

    def load_playlist(self):
        self.list_widget.clear()
        self.list_widget.addItems([
            *[e.filename for e in self.music_subsystem.sounds]
        ])

    def open_add_dialog(self):
        dialog = AddTrackDialog(self.game)
        dialog.exec_()
        self.load_playlist()

    def delete_music_track(self):
        current_item = self.list_widget.currentItem()
        if current_item:
            self.music_subsystem.remove(current_item.text())
        self.load_playlist()

    def init_ui(self):
        self.load_playlist()

    def init_signals(self):
        self.add_btn.clicked.connect(self.open_add_dialog)
        self.remove_btn.clicked.connect(self.delete_music_track)


class AddTrackDialog(QDialog):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        self.music_subsystem = game.get_music_subsystem()

        self.setAttribute(Qt.WA_DeleteOnClose)

        uic.loadUi("dialogues/forms/add_track_dialog.ui", self)

        self.init_signals()

    def add_music_track(self):
        self.music_subsystem.add(
            self.lineEdit.text(), ""
        )

    def init_signals(self):
        self.buttonBox.accepted.connect(self.add_music_track)
