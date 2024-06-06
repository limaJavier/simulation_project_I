from simulation import Event, Simulation
from math import floor
from random import expovariate

class CarWash(Simulation):
    def __init__(self, interarrival_distro, service_distro) -> None:
        super().__init__()
        # Simulation times distributions
        self._interarrival_distro = interarrival_distro
        self._service_distro = service_distro

        # Simulation properties
        self._arrival_index = 0
        self._queue_size = 0
        self._serving = False
        self._maximum_queue_length = 9

    def _simulate_day(self, initial_state: tuple[int, bool, list[Event]] = [0, False, [Event("arrival", 0)]]):
        self._queue_size = initial_state[0] # Initial queue state
        self._serving = initial_state[1] # Initial serving state
        self._future_events = initial_state[2] # Initial future event list

        lost_cars = 0
        while True:
            # Pop imminent event
            current_event = self._future_events.pop(0)
            # Update clock
            self._clock = current_event.time

            if current_event.type == "arrival":
                self._future_events.append(
                    Event("arrival", self._interarrival_distro() + self._clock)
                )

                # Increase lost cars if there's no space available
                if self._queue_size >= self._maximum_queue_length:
                    lost_cars += 1
                else:
                    self._queue_size += 1
                
            # Set serving to false if customer left server
            if current_event.type == "departure":
                self._serving = False

            # Pop customer from queue if server is idle and queue is not empty
            if self._serving == False and self._queue_size > 0:
                self._queue_size -= 1
                self._serving = True
                # Create a departure event for popped customer
                self._future_events.append(
                    Event("departure", self._service_distro() + self._clock)
                )

            # Sort event by their time
            self._future_events.sort(key=lambda event: event.time)

            if self._clock >= 36000:
                break
        
        return lost_cars
    
    def simulate(self, days : int):
        mean = 0
        for _ in range(0, days):
            mean += self._simulate_day([0, False, [Event("arrival", self._interarrival_distro())]])
        mean = mean / days
        print(f"La media de coches perdidos es de {mean}")

def arrival_distro():
    return floor(expovariate(20 / 3600))
def service_distro():
    return floor(expovariate(1 / 720))

car_wash = CarWash(arrival_distro, service_distro)
car_wash.simulate(1000)