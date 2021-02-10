from typing import List


class Object:
    def __init__(self, available_signals: List[str]):
        self.available_signals = available_signals
        self.installed_slots = {}
        for signal in available_signals:
            setattr(self, signal, [])

    def signal(self, signal, *args, **kwargs):
        if getattr(self, "signal_filter", False):
            if not self.signal_filter(signal, *args, **kwargs):
                return
        for slot in self.installed_slots.get(signal, []):
            slot(*args, **kwargs)

    def connect(self, signal, slot):
        if signal in self.available_signals:
            self.installed_slots[signal] = self.installed_slots.get(signal, []) + [slot]
