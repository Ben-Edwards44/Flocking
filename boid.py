#https://www.red3d.com/cwr/boids/


import math


class Boid:
    def __init__(self, look_radius, start_x, start_y, vel_x, vel_y, max_speed):
        self.look_radius = look_radius
        self.pos = Vector(start_x, start_y)
        self.vel = Vector(vel_x, vel_y)
        self.speed = max_speed

        self.boids = []

        self.align_limit = 1
        self.cohesion_limit = 1
        self.seperation_limit = 1

    def get_neighbours(self):
        neighbours = []
        for i in self.boids:
            if self.distance(i.pos.x, i.pos.y) <= self.look_radius and i != self:
                neighbours.append(i)

        return neighbours

    def align(self, neighbours):
        if len(neighbours) == 0:
            return Vector(0, 0)

        total_vel = Vector(0, 0)
        for i in neighbours:
            total_vel = Vector.add(total_vel, i.vel)

        desired_vel = Vector.divide(total_vel, len(neighbours))
        new_vel = Vector.subtract(desired_vel, self.vel)
        new_vel.limit_mag(self.align_limit)

        return new_vel

    def cohesion(self, neighbours):
        if len(neighbours) == 0:
            return Vector(0, 0)


        x_pos = [i.pos.x for i in neighbours]
        y_pos = [i.pos.y for i in neighbours]

        avg_pos = Vector(sum(x_pos) / len(x_pos), sum(y_pos) / len(y_pos))

        desired = Vector.subtract(avg_pos, self.pos)
        new_vel = Vector.subtract(desired, self.vel)
        new_vel.limit_mag(self.cohesion_limit)

        return new_vel

    def seperation(self, neighbours):
        if len(neighbours) == 0:
            return Vector(0, 0)

        total = Vector(0, 0)
        for i in neighbours:
            new_vect = Vector.subtract(self.pos, i.pos)

            dist = 0.1 * self.distance(i.pos.x, i.pos.y)
            if dist == 0:
                dist = 1e-10

            new_vect = Vector.divide(new_vect, dist)
            total = Vector.add(new_vect, total)

        desired = Vector.divide(total, len(neighbours))
        new_vel = Vector.subtract(desired, self.vel)
        new_vel.limit_mag(self.seperation_limit)

        return new_vel

    def check_border(self):
        if self.pos.x < 0:
            self.pos.x = 500
        elif self.pos.x > 500:
            self.pos.x = 0

        if self.pos.y < 0:
            self.pos.y = 500
        elif self.pos.y > 500:
            self.pos.y = 0

    def find_future_pos(self):
        vel = Vector(self.vel.x, self.vel.y)
        vel.set_magnitude(10)

        pos_x = self.pos.x + vel.x
        pos_y = self.pos.y + vel.y

        return (pos_x, pos_y)

    def main(self):
        acc = Vector(0, 0)

        neighbours = self.get_neighbours()
        align = self.align(neighbours)
        cohesion = self.cohesion(neighbours)
        seperation = self.seperation(neighbours)

        acc = Vector.add(align, cohesion)
        acc = Vector.add(acc, seperation)

        self.pos = Vector.add(self.pos, self.vel)
        self.vel = Vector.add(self.vel, acc)

        self.vel.set_magnitude(self.speed)

        self.check_border()

    distance = lambda self, x, y: math.sqrt((x - self.pos.x)**2 + (y - self.pos.y)**2)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def add(v1, v2):
        new_x = v1.x + v2.x
        new_y = v1.y + v2.y

        return Vector(new_x, new_y)

    @staticmethod
    def subtract(v1, v2):
        new_x = v1.x - v2.x
        new_y = v1.y - v2.y

        return Vector(new_x, new_y)

    @staticmethod
    def divide(vector, scalar):
        new_x = vector.x / scalar
        new_y = vector.y / scalar

        return Vector(new_x, new_y)

    def set_magnitude(self, magnitude):
        current_mag = math.sqrt(self.x**2 + self.y**2)
        multiplier = magnitude / current_mag

        self.x *= multiplier
        self.y *= multiplier

        """
        if self.x == 0:
            theta = math.atan(self.y / 0.000001)
        else:
            theta = math.atan(self.y / self.x)

        new_x = math.cos(theta) * magnitude
        new_y = math.cos(theta) * magnitude

        if self.x < 0:
            new_x *= -1
        if self.y < 0:
            new_y *= -1

        self.x = new_x
        self.y = new_y
        """

    def limit_mag(self, limit):
        mag = math.sqrt(self.x**2 + self.y**2)

        if mag > limit:
            self.set_magnitude(limit)

    def normalise(self):
        magnitude = math.sqrt(self.x**2 + self.y**2)

        vect = Vector.divide(self, magnitude)
        
        self.x = vect.x
        self.y = vect.y