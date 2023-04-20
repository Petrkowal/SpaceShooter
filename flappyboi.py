import math
from time import time
import random

import pygame


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, rhs):
        if not isinstance(rhs, Vector):
            raise ValueError()
        return Vector(self.x + rhs.x, self.y + rhs.y, self.z + rhs.z)

    def __sub__(self, rhs):
        if not isinstance(rhs, Vector):
            raise ValueError()
        return Vector(self.x - rhs.x, self.y - rhs.y, self.z - rhs.z)

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, rhs):
        if isinstance(rhs, int) or isinstance(rhs, float):
            return Vector(self.x * rhs, self.y * rhs, self.z * rhs)
        else:
            raise ValueError()

    def __truediv__(self, rhs):
        if isinstance(rhs, int) or isinstance(rhs, float):
            return Vector(self.x / rhs, self.y / rhs, self.z / rhs)
        else:
            raise ValueError()

    def __eq__(self, rhs):
        if not isinstance(rhs, Vector):
            return False
        return self.x == rhs.x and self.y == rhs.y and self.z == rhs.z

    @property
    def unit(self):
        if self.x == 0 and self.y == 0 and self.z == 0:
            return Vector(0, 0, 0)
        return self / self.length()

    def __getitem__(self, index):
        return (self.x, self.y, self.z)[index]

    def __setitem__(self, index, val):
        if index == 0:
            self.x = val
        elif index == 1:
            self.y = val
        elif index == 2:
            self.z = val
        else:
            raise IndexError()

        """
        or replace conditions with table lookup:
        mapping = {
            0: 'x',
            1: 'y',
            2: 'z'
        }
        self.__dict__[mapping[index]] = val
        """

    def __iter__(self):
        for attribute in (self.x, self.y, self.z):
            yield attribute
        """
        or
        yield from iter((self.x, self.y, self.z))
        or simply
        yield self.x
        yield self.y
        yield self.z
        """

    def __str__(self):
        return "({}, {}, {})".format(self.x, self.y, self.z)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pos

    def update(self, delta):
        self.pos = (self.pos[0] + 100 * delta, self.pos[1])

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class Engine:
    def __init__(self, width=800, height=600):
        pygame.init()
        pygame.key.set_repeat(500, 300)
        pygame.display.set_caption("SKJ game")

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.image = pygame.image.load("images/bird.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.pos = (random.randint(0, self.width), random.randint(0, self.height))

        self.rotation = 0
        self.cooldown = 0

        self.bullets = pygame.sprite.Group()

    def main_loop(self):
        while True:
            self.handle_keys()
            self.update()
            self.draw()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.target = event.pos

    def update(self):
        delta = self.clock.tick(60) / 1000  # 0.016
        self.cooldown += delta

        x, y = self.pos
        speed = 100

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= speed * delta
        if keys[pygame.K_RIGHT]:
            x += speed * delta
        if keys[pygame.K_UP]:
            y -= speed * delta
        if keys[pygame.K_DOWN]:
            y += speed * delta
        if keys[pygame.K_SPACE] and self.cooldown >= 0.5:
            image = pygame.image.load("images/bird.png")
            image = pygame.transform.scale(image, (25, 25))
            bullet = Bullet(image, self.pos)
            self.bullets.add(bullet)
            self.cooldown = 0

        self.pos = (x, y)

        self.bullets.update(delta)

        for bullet in self.bullets:
            if bullet.pos[0] >= self.width:
                bullet.kill()
                print("bullet disappeared")

    def draw(self):
        self.screen.fill((0, 0, 0))

        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.screen.blit(self.image, self.pos)

        pygame.display.flip()


if __name__ == '__main__':
    engine = Engine()
    engine.main_loop()
