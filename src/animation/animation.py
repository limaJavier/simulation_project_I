from manim import *
from random import expovariate

class Stats:
    def __init__(self):
        self.time = DecimalNumber(0)
        self.time.add_updater(lambda t, dt: t.increment_value(dt))
        self.time_text = Tex("Time = ").next_to(self.time, LEFT)

        self.number_client = DecimalNumber(0)
        self.number_client_text = Tex("Number of Clients = ").next_to(self.number_client, LEFT)

        self.lost_client = DecimalNumber(0)
        self.lost_clients_text = Tex("Lost Clients = ").next_to(self.lost_client, LEFT)

        self.average_time_system = DecimalNumber(0)
        self.average_time_system_show = DecimalNumber(0).add_updater(
            lambda t: t.set_value(
                self.average_time_system.get_value() / ( self.number_client.get_value() - self.lost_client.get_value()) if (self.number_client.get_value() > 0) else 0))
        self.average_time_system_text = Tex("Avg Time in System = ").next_to(self.average_time_system_show, LEFT)

        self.average_attention_time = DecimalNumber(0)
        self.average_attention_time_show = DecimalNumber(0).add_updater(lambda t: t.set_value(self.average_attention_time.get_value() / ( self.number_client.get_value() - self.lost_client.get_value()) if (self.number_client.get_value() > 0) else 0))
        self.average_attention_time_text = Tex("Avg Attention Time = ").next_to(self.average_attention_time_show, LEFT)

        self.average_interarrival_time = DecimalNumber(0)
        self.average_interarrival_time_show = DecimalNumber(0).add_updater(lambda t: t.set_value(
            (self.average_interarrival_time.get_value() / ( self.number_client.get_value())) if (self.number_client.get_value() > 0) else 0))
        self.average_interarrival_time_text = Tex("Avg Interarrival Time = ").next_to(self.average_interarrival_time_show, LEFT)

    def add(self, scene):
        group = VGroup(
            VGroup(self.time, self.time_text).set_color(YELLOW),
            VGroup(self.number_client, self.number_client_text).set_color(BLUE),
            VGroup(self.average_time_system_show, self.average_time_system_text).set_color(PURPLE),
            VGroup(self.average_attention_time_show, self.average_attention_time_text).set_color(GREY_BROWN),
            VGroup(MathTex(r"\mu = \frac{10}{12}")).set_color(GREY_BROWN),
            VGroup(self.average_interarrival_time_show, self.average_interarrival_time_text).set_color(GREEN),
            VGroup(MathTex(r"\lambda = \frac{20}{6}")).set_color(GREEN),
            VGroup(self.lost_client, self.lost_clients_text).set_color(PURPLE_E))
        
        group.arrange(DOWN)    
        group.shift(6*LEFT)
        scene.add(group)

WAITING = BLUE_E
DONE = GREEN_E
BUSY = YELLOW_E
LOST = MAROON_E
REMOVED = PURPLE_E

# this rate is so that 1 minute is equivalent to 10 hours.
lambd = 20 / 6 
miu = 10 / 12  

class Simulation(Scene):
    def construct(self):
        self.camera.frame_width = 19
        time_simulation = 60
        queue_capacity = 10
        stats = Stats()
        stats.add(self)
        arrivals = []
        arrivals.append(expovariate(lambd))
        while arrivals[-1] < time_simulation:
            next = expovariate(lambd)
            arrivals.append(arrivals[-1] + next)
        arrivals = arrivals[:-1]
        service_times = [expovariate(miu) for i in range(0, len(arrivals))]
        time_simulation += 10 * max(service_times)
        marked = [False for i in range(0, len(arrivals))]
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

        posX = [ValueTracker(8) for i in range(0, len(arrivals))]        
        posY = [ValueTracker(2) for i in range(0, len(arrivals))]

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
                rs.move_to(queue2[len(queue2)-1].get_center()).shift(1.3*RIGHT)
            queue2.add(rs)
        queue2.shift(3*LEFT)
        self.add(queue)
        self.play(Create(queue2))
        def updaterArrivals(queue : VGroup, dt):
            for i in range(0, len(arrivals)):
                if not marked[i]  and stats.time.get_value() > arrivals[i]:
                    marked[i] = True
                    stats.number_client.increment_value(1)
                    stats.average_interarrival_time.increment_value(arrivals[i] - arrivals[i-1] if i > 0 else arrivals[i])
                    car = Circle(1/2).set_opacity(0.5)
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
                        stats.lost_client.increment_value(1)
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
                    stats.average_attention_time.increment_value(dt)
                    if service_times[int(queue[0][1].tex_string)-1] < 0:
                        queue[0].set_color(DONE)
                        queue[0][2].remove_updater(queue[0][2].updaters[0])
                        stats.average_time_system.increment_value(queue[0][2].get_value())
                        shiftY[int(queue[0][1].tex_string)-1] -= 10
                        queue.remove(queue[0])
                        for el in queue:
                            shiftX[int(el[1].tex_string)-1] += -(1.3)
        
        queue.add_updater(updaterArrivals)
        queue.add_updater(updaterServing)
        self.wait(time_simulation)