from math import sin, cos, pi
import pygame


class Ship:
    def __init__(self, size, x, y, color=(255, 255, 255)):
        self.size = size
        if size < 5:
            self.size = 5
        self.x = x
        self.y = y
        self.color = color
        self.velocity = (0, 0)
        self.angular_velocity = 0
        self.speed = 0.2
        self.angel = -pi / 2
        self.f = [0, 0]
        self.drag = 0.95
        self.torqle = 0

    def draw(self, drawer, surface):
        drawer.circle(surface, self.color, (
            self.x + int(self.size * 2 * cos(self.angel)),
            self.y + int(self.size * 2 * sin(self.angel))), self.size, 1)
        drawer.line(surface, self.color,
                    (self.x + int(self.size * 2 * cos(self.angel - pi / 6)),
                     self.y + int(self.size * 2 * sin(self.angel - pi / 6))),
                    (self.x - int(self.size * cos(self.angel + pi / 3)),
                     self.y - int(self.size * sin(self.angel + pi / 3))), 1)
        drawer.line(surface, self.color,
                    (self.x + int(self.size * 2 * cos(self.angel + pi / 6)),
                     self.y + int(self.size * 2 * sin(self.angel + pi / 6))),
                    (self.x - int(self.size * cos(self.angel - pi / 3)),
                     self.y - int(self.size * sin(self.angel - pi / 3))), 1)
        drawer.circle(surface, self.color, (self.x + int(self.size * 2 * cos(self.angel - 5 * pi / 6)), self.y + int(self.size * 2 * sin(self.angel - 5 * pi / 6))), self.size, 1)
        drawer.circle(surface, self.color, (self.x + int(self.size * 2 * cos(self.angel + 5 * pi / 6)), self.y + int(self.size * 2 * sin(self.angel + 5 * pi / 6))), self.size, 1)
        drawer.circle(surface, self.color, (self.x, self.y), 3, 1)

    def update(self, move, w, h):
        ex = None
        self.get_force(self.speed * move[1])
        self.torqle += move[0]
        self.angel -= self.torqle
        self.torqle *= self.drag
        if self.x + self.f[0] < 0 or self.x + self.f[0] > w:

            if self.f[0] + self.x < 0:
                self.torqle += pi / 60 if self.f[1] > 0 else -pi / 60
            else:
                self.torqle -= pi / 60 if self.f[1] > 0 else -pi / 60
            self.f[0] *= -2
            ex = (self.x, self.y, self.size,
                  (self.f[0] ** 2 + self.f[1] ** 2) ** 0.5 * 2)

        self.x += self.f[0]
        self.f[0] *= self.drag
        if self.y + self.f[1] < 0 or self.y + self.f[1] > h:
            if self.f[1] + self.y < 0:
                self.torqle -= pi / 60 if self.f[0] > 0 else -pi / 60
            else:
                self.torqle += pi / 60 if self.f[0] > 0 else -pi / 60
            self.f[1] *= -2
            ex = (self.x, self.y, self.size,
                  (self.f[0] ** 2 + self.f[1] ** 2) ** 0.5)
        self.y += self.f[1]
        self.f[1] *= self.drag
        return ex

    def get_force(self, force):
        sum_force = (self.f[0] ** 2 + self.f[1] ** 2 + 1) ** 0.2
        self.f[0] += force * cos(self.angel) * sum_force
        self.f[1] += force * sin(self.angel) * sum_force


class Explosion:
    def __init__(self, x, y, size, force):
        self.x = x
        self.y = y
        self.size = size
        self.force = int(force * 2.55)
        self.kill = 0
        self.color = [255, 255, 255, self.force]

    def update(self):

        # print(self.color)
        if self.force == 0:
            self.kill = 1
        else:
            self.size += 1
            self.force -= 1
            self.color[-1] = self.force

    def draw(self, drawer, surface):
        target_rect = pygame.Rect((self.x, self.y), (0, 0)).inflate(
            (self.size, self.size))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        drawer.circle(shape_surf, self.color, (self.size // 2, self.size // 2),
                      self.size // 2)
        surface.blit(shape_surf, target_rect)


class GameObject:
    def __init__(self, x, y, size, force):
        self.x = x
        self.y = y
        self.size = size
        self.force = force
        self.kill = 0
        self.drag = 1 / size ** 2
        self.color = (255, 255, 255)

    def update(self):
        self.x += self.force[0]
        self.y += self.force[1]
        self.force = (self.drag * self.force[0], self.drag * self.force[1])

    def add_force(self, force):
        self.force = self.force[0] + force[0], self.force[1] + self.force[1]


class Ball(GameObject):
    def draw(self, drawer, surface):
        drawer.circle(surface, self.color, (self.x, self.y), self.size)

    def collide(self, rect=None, circle=None):
        if rect:
            pass
        elif circle:
            x, y, r = circle
            l = ((self.x - x) ** 2 + (self.y - y) ** 2) ** 0.5 - (r + self.size)
            if l < 0:
                return l
            else:
                return False
        else:
            return False

