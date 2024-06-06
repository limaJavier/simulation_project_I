class Event:
    def __init__(self, type: str, time: int) -> None:
        self.type = type
        self.time = time

class Simulation:
    def __init__(self) -> None:
        self._clock = 0
        self._future_events : list[Event]= []