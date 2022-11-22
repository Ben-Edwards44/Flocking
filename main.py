import boid
import pygame
import random


pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flocking Simulation")


boids = []


def create_boids(num):
    for _ in range(num):
        new = boid.Boid(60, random.randint(0, 500), random.randint(0, 500), random.uniform(-1, 1), random.uniform(-1, 1), 4)
        boids.append(new)

    for i in boids:
        i.boids = boids


def draw_boids():
    window.fill((0, 0, 0))

    for i in boids:
        pygame.draw.circle(window, (255, 255, 255), (int(i.pos.x), int(i.pos.y)), 5)
        pygame.draw.line(window, (255, 255, 255), (int(i.pos.x), int(i.pos.y)), i.find_future_pos(), 2)

    pygame.display.update()


def main():
    create_boids(75)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        for i in boids:
            i.main()

        draw_boids()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()


main()