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

WAITING = GRAY_E
DONE = GREEN_E
BUSY = YELLOW_E
LOST = MAROON_E
REMOVED = PURPLE_E

lambd = 20 / 6
miu = 10 / 12  

class Simulation(Scene):
    def construct(self):
        time_simulation = 5
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

        shiftX = [0 for i in range(0, len(arrivals))]
        shiftY = [0 for i in range(0, len(arrivals))]

        def frX(i):
            j = i
            def f(mobj, dt):
                dt *= 10
                increment = 0
                if shiftX[j] > 0:
                    if shiftX[j] < dt:
                        increment = shiftX[j]
                    else:
                        increment = dt
                    mobj.increment_value(increment)
                    shiftX[j] -= increment
                if shiftX[j] < 0:
                    if -shiftX[j] < dt:
                        increment = -shiftX[j]
                    else:
                        increment = dt
                    mobj.increment_value(-increment)
                    shiftX[j] += increment
            return f
        
        def frY(i):
            j = i
            def f(mobj, dt):
                dt *= 10
                increment = 0
                if shiftY[j] > 0:
                    if shiftY[j] < dt:
                        increment = shiftY[j]
                    else:
                        increment = dt
                    mobj.increment_value(increment)
                    shiftY[j] -= increment
                if shiftY[j] < 0:
                    if -shiftY[j] < dt:
                        increment = -shiftY[j]
                    else:
                        increment = dt 
                    mobj.increment_value(-increment)
                    shiftY[j] += increment
            return f

        posX = [ValueTracker(-1) for i in range(0, len(arrivals))]        
        posY = [ValueTracker(1) for i in range(0, len(arrivals))]

        for i in range(0, len(arrivals)):
            self.add(posX[i])
            self.add(posY[i])
            posX[i].add_updater(frX(i))
            posY[i].add_updater(frY(i))


        queue = VGroup()
        queue2 = VGroup()
        for i in range(0, queue_capacity):
            rs = Square(1.3, color = WHITE)
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
                    time_until_done = DecimalNumber(0).next_to(car.get_center(), DOWN)
                    time_until_done.add_updater(lambda t, dt: t.increment_value(dt))
                    gr = VGroup(car, idd, time_until_done).move_to([posX[i].get_value(), posY[i].get_value(), 0])
                    gr.color = WAITING
                    def updaterCar(obj):
                        j = int(obj[1].tex_string) - 1
                        obj.move_to([posX[j].get_value(), posY[j].get_value(), 0])
                    gr.add_updater(updaterCar)

                    def updaterCar2(obj):
                        j = int(obj[1].tex_string) - 1
                        if obj.color == LOST:
                           shiftX[j] += 10
                           obj.color = REMOVED
                    gr.add_updater(updaterCar2)
                    self.add(gr)
                    if len(queue) >= queue_capacity:
                        shiftX[i] += 2 - gr.get_center()[0]
                        shiftY[i] += -2 - gr.get_center()[1]
                        gr.color = LOST
                        lost_clients.increment_value(1)
                    else:
                        shiftX[i] += queue2[len(queue)].get_center()[0] - gr.get_center()[0]
                        shiftY[i] += queue2[len(queue)].get_center()[1] - gr.get_center()[1]
                        queue.add(gr)
        def updaterServing(queue: VGroup, dt):
            if len(queue) > 0:
                if queue[0].color == WAITING:
                    queue[0].set_color(BUSY)
                elif queue[0].color == BUSY:
                    service_times[int(queue[0][1].tex_string)-1] -= dt
                    if service_times[int(queue[0][1].tex_string)-1] < 0:
                        queue[0].set_color(DONE)
                        queue[0][2].remove_updater(queue[0][2].updaters[0])
                        shiftX[int(queue[0][1].tex_string)-1] -= 10
                        queue.remove(queue[0])
                        for el in queue:
                            shiftX[int(el[1].tex_string)-1] += -1
        queue.add_updater(updaterArrivals)
        queue.add_updater(updaterServing)
        self.wait(time_simulation)