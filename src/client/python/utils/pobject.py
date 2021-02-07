class Object:
    def __init__(self, available_signals: list[str]):
        self.available_signals = available_signals
        for signal in available_signals:
            setattr(self, signal, None)

    def connect(self, signal, slot):
        if signal in self.available_signals:
            setattr(self, signal, slot)