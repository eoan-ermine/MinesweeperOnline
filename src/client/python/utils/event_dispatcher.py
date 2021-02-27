import pygame

from src.client.python.music.music import MUSIC_END_EVENT
from src.client.python.scenes.scene import CLOSE_SCENE_EVENT
from src.client.python.utils.utils import terminate

RETURN_FROM_DISPATCHER = pygame.USEREVENT + 3


class EventDispatcher:
    def __init__(self, subscribers, game):
        self.subscribers = subscribers
        self.signal_to_subscribers = {}

        self.music_subsystem = game.get_music_subsystem()

        for subscriber in self.subscribers:
            for signal in subscriber.available_signals:
                self.signal_to_subscribers[signal] = self.signal_to_subscribers.get(signal, []) + [subscriber]

    def dispatch_signal(self, event, signal):
        subscribers = self.signal_to_subscribers.get(signal, [])
        for subscriber in subscribers:
            subscriber.signal(signal, event)

    def dispatch_event(self, event):
        event_type = event.type

        if event_type == pygame.MOUSEMOTION:
            self.dispatch_signal(event, "mouse_motion")
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.dispatch_signal(event, "mouse_down")
            self.dispatch_signal(event, "clicked")
        elif event_type == pygame.MOUSEBUTTONUP:
            self.dispatch_signal(event, "mouse_up")
        elif event_type == MUSIC_END_EVENT:
            self.music_subsystem.queue_next()
        elif event_type == CLOSE_SCENE_EVENT:
            return True
        elif event_type == RETURN_FROM_DISPATCHER:
            return RETURN_FROM_DISPATCHER
        elif event_type == pygame.QUIT:
            self.music_subsystem.stop()
            terminate()
