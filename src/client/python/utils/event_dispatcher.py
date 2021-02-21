import pygame

from src.client.python.music.music import MUSIC_END_EVENT


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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.dispatch_signal(event, "mouse_down")
            self.dispatch_signal(event, "clicked")
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dispatch_signal(event, "mouse_up")
        elif event.type == MUSIC_END_EVENT:
            self.music_subsystem.queue_next()
