import time

DEFAULT_FRICTION = 50


class Scroller:
    def __init__(self) -> None:
        self.position = 0
        self.velocity = 0
        self.dir = 1
        self.start_time = time.time()
        self.saved_velocity = 0

    def update(self, dx: float, height: float):
        now = time.time()
        dt = now - self.start_time
        if dt < 0.01:
            self.saved_velocity += dx
            return

        dx += self.saved_velocity
        self.saved_velocity = 0
        self.start_time = now

        if dx != 0:
            self.dir = 1 if dx > 0 else -1
            self.velocity = 0.8 * self.velocity + 0.2 * abs(dx) / dt
            self.position += dx
        else:
            self.position += self.dir * self.velocity * dt
            self.velocity -= DEFAULT_FRICTION * dt

        if self.position > height:
            self.position = height
            self.dir = -1
            self.velocity = 0
        elif self.position < 0:
            self.position = 0
            self.dir = 1
            self.velocity = 0

        if self.velocity < 0.1:
            self.velocity = 0
