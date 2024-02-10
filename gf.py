import pygame
from fr import Ship, Explosion, Ball
from math import pi

backgroundColor = (0, 0, 0)
WIDTH = 1200
HEIGHT = 700
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ship = Ship(10, WIDTH // 2, HEIGHT // 2)
move = [0,0]
objects = []

while 1:
    screen.fill(backgroundColor)
    clock.tick(60)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            exit()

        if ev.type == pygame.MOUSEBUTTONDOWN:
            objects.append(Ball(*pygame.mouse.get_pos(), 10, (0, 0)))

    keys = pygame.key.get_pressed()
    move = [0, 0]
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        move[0] = pi / 500
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        move[0] = -pi / 500
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        move[1] = 1
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        move[1] = -1
    i = 0
    while i != len(objects):
        objects[i].update()
        if objects[i].kill:
            del objects[i]
        else:
            i += 1

    for obj in objects:
        obj.draw(pygame.draw, screen)
    ship.draw(pygame.draw, screen)
    ex = ship.update(move, WIDTH, HEIGHT)
    if ex:
        objects.append(Explosion(*ex))
    pygame.display.flip()
