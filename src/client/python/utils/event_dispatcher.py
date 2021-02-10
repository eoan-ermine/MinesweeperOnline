import pygame

class EventDispatcher:
    def __init__(self, subscribers):
        self.subscribers = subscribers
        self.signal_to_subscribers = {}

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