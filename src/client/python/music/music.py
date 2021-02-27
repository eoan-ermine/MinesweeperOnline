import pygame

MUSIC_END_EVENT = pygame.USEREVENT + 1


def load_file(filename: str, prefix: str = "resources/music/") -> pygame.mixer.Sound:
    return pygame.mixer.Sound(prefix + filename)


class MusicTrack:
    def __init__(self, filename, prefix: str):
        self.filename = filename
        self.sound = load_file(filename, prefix)


class MusicSubsystem:
    def __init__(self, *args):
        pygame.mixer.init()

        self.playlist = pygame.mixer.Channel(0)
        self.playlist.set_endevent(MUSIC_END_EVENT)

        self.sounds = [
            MusicTrack(filename, "resources/music/") for filename in args
        ]
        self.current_sound = -1
        self.length_of_playlist = len(self.sounds)

        self.queue_next()

    def add(self, filename, prefix):
        self.sounds.append(MusicTrack(filename, prefix))
        self.length_of_playlist += 1

    def remove(self, filename):
        self.sounds = [e for e in self.sounds if e.filename != filename]

    def queue_next(self):
        self.current_sound = (self.current_sound + 1) % self.length_of_playlist
        self.playlist.queue(self.sounds[self.current_sound].sound)
        print(self.sounds[self.current_sound])

    def stop(self):
        self.playlist.stop()
