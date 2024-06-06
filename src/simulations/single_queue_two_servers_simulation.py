from simulation import Event, Simulation
from math import floor
from random import expovariate
import csv

class CarWash(Simulation):
    def __init__(self, interarrival_distro, service_distro, maximum_queue_length = 9, duration = 36000) -> None:
        super().__init__()
        # Simulation times distributions
        self._interarrival_distro = interarrival_distro
        self._service_distro = service_distro

        # Simulation properties
        self._queue = []
        self._serving_1 = False
        self._serving_2 = False
        self._maximum_queue_length = maximum_queue_length
        self._duration = duration

    def _simulate_day(self, initial_state: tuple[list[int], tuple[bool, bool], list[Event]] = [[], (False, False), [Event("arrival", 0)]]):
        # Reset clock
        self._clock = 0

        # Set initial state
        self._queue = initial_state[0] # Initial queue state
        self._serving_1 = initial_state[1][0] # Initial serving state
        self._serving_2 = initial_state[1][1] # Initial serving state
        self._future_events = initial_state[2] # Initial future event list

        _arrival_index = 0
        # Update arrival index
        for _ in self._queue:
            _arrival_index += 1

        delay_times :dict[int, int] = {}
        effective_arrival_times = []
        service_usage = 0
        lost_cars = 0
        while True:
            # Pop imminent event
            current_event = self._future_events.pop(0)
            # Store inter-event elapsed time
            delay = current_event.time - self._clock
            # Update clock
            self._clock = current_event.time

            # Statistical step
            if self._serving_1 == True or self._serving_2 == True:
                service_usage += delay
                # Service usage cannot be greater than simulation duration
                if service_usage > self._duration:
                    service_usage = self._duration

            # Stop simulation
            if self._clock >= self._duration:
                break

            # Simulation steps
            if current_event.type == "arrival":
                # Create an arrival event
                self._future_events.append(
                    Event("arrival", self._interarrival_distro() + self._clock)
                )

                if len(self._queue) >= self._maximum_queue_length: # Increase lost cars if there's no space available
                    lost_cars += 1
                else: # Add car to queue if there is space available
                    self._queue.append(_arrival_index)
                    # Add customer's delay time
                    delay_times[_arrival_index] = 0
                    _arrival_index += 1
                    effective_arrival_times.append(self._clock)
                
            # Set serving to false if customer left server
            if current_event.type == "departure":
                if self._serving_1:
                    self._serving_1 = False
                else:
                    self._serving_2 = False

            # Pop customer from queue if server is idle and queue is not empty
            if (self._serving_1 == False or self._serving_2 == False) and len(self._queue) > 0:
                self._queue.pop(0) # Pop car from queue
                
                # Start washing the car
                if self._serving_1:
                    self._serving_2 = True
                else:
                    self._serving_1 = True

                # Create a departure event for popped car
                self._future_events.append(
                    Event("departure", self._service_distro() + self._clock)
                )

            # Statistical step
            for car in self._queue:
                delay_times[car] += delay

            # Sort events by their time
            self._future_events.sort(key=lambda event: event.time)

        # Calculate mean delay time
        mean_delay_time = 0
        for car in delay_times:
            mean_delay_time += delay_times[car]
        mean_delay_time = mean_delay_time / _arrival_index

        # Calculate mean of effective interarrival time
        effective_interarrival_mean = 0
        for i in range(0, len(effective_arrival_times) - 1):
            effective_interarrival_mean += effective_arrival_times[i + 1] - effective_arrival_times[i]
        effective_interarrival_mean = effective_interarrival_mean / (len(effective_arrival_times) - 1) 

        return [self._duration, service_usage, lost_cars, mean_delay_time, effective_interarrival_mean]
    
    def simulate(self, days : int):
        column_names = ['duration', 'service_usage', 'lost_cars', 'mean_delay_time', 'effective_interarrival_mean']
        file_name = "single_queue_two_servers.csv"

        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(column_names)

            for _ in range(0, days):
                writer.writerow(self._simulate_day([[], (False, False), [Event("arrival", self._interarrival_distro())]]))

def arrival_distro():
    return floor(expovariate(20 / 3600))
def service_distro():
    return floor(expovariate(1 / 720))

car_wash = CarWash(arrival_distro, service_distro, 18)
car_wash.simulate(1000)