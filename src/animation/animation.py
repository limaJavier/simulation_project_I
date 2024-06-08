from manim import *
from random import expovariate

class Clock:
    def __init__(self):
        self.time = DecimalNumber()
        self.time.add_updater(lambda t, dt: t.increment_value(dt))
        self.text = Tex("Time = ")
        self.time.next_to(self.text, RIGHT)

    def add(self, scene):
        group = VGroup(self.time, self.text)
        group.color = "RED"
        group.shift(3*UP + 3*LEFT)    
        scene.add(group)

WAITING = WHITE
DONE = GREEN
BUSY = RED
LOST = MAROON_E

lambd = 20 / 6
miu = 10 / 12  

class Simulation(Scene):
    def construct(self):
        time_simulation = 60
        queue_capacity = 10
        clock = Clock()
        clock.add(self)
        lost_clients_tex = Tex("Lost Clients = ").move_to(3*UP + 2*RIGHT).set_color(BLUE)
        lost_clients = DecimalNumber(0).next_to(lost_clients_tex, RIGHT).set_color(BLUE)
        self.add(lost_clients)
        self.add(lost_clients_tex)
        arrivals = []
        arrivals.append(expovariate(lambd))
        while arrivals[-1] < time_simulation:
            next = expovariate(lambd)
            arrivals.append(arrivals[-1] + next)
        arrivals = arrivals[:-1]
        service_times = [expovariate(miu) for i in range(0, len(arrivals))]
        queue = VGroup()
        queue2 = VGroup()
        for i in range(0, queue_capacity):
            rs = Square(1, color = WHITE)
            if i > 0:
                rs.move_to(queue2[len(queue2)-1].get_center()).shift(1*RIGHT)
            queue2.add(rs)
        queue2.shift(4*LEFT)
        self.add(queue)
        self.play(Create(queue2))
        def updaterArrivals(queue : VGroup, dt):
            for i in range(0, len(arrivals)):
                if clock.time.get_value() > arrivals[i]:
                    arrivals[i] = time_simulation + 1
                    car = Circle(1/2)
                    idd = MathTex(i+1).move_to(car.get_center())
                    gr = VGroup(car, idd)
                    gr.color = WAITING
                    if len(queue) >= queue_capacity:
                        gr.move_to(2*LEFT + 2*DOWN)
                        gr.color = LOST
                        lost_clients.increment_value(1)
                    else:
                        gr.move_to(queue2[len(queue)].get_center())
                        queue.add(gr)
        def updaterServing(queue: VGroup, dt):
            if len(queue) > 0:
                if queue[0].color == WAITING:
                    queue[0].set_color(BUSY)
                elif queue[0].color == BUSY:
                    service_times[int(queue[0][1].tex_string)-1] -= dt
                    if service_times[int(queue[0][1].tex_string)-1] < 0:
                        queue[0].set_color(DONE)
                        queue[0].move_to(10*LEFT)
                        queue.remove(queue[0])
                        for el in queue:
                            el.shift(1*LEFT)
        queue.add_updater(updaterArrivals)
        queue.add_updater(updaterServing)
        self.wait(time_simulation)