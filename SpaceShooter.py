import math
from typing import Tuple

import pygame
from pygame.examples.aliens import load_image


class CollisionDetector:
    @staticmethod
    def detect_collision(ships, bullets):
        collisions = []
        for ship in ships:
            for bullet in bullets:
                if pygame.sprite.collide_mask(ship, bullet):
                    collisions.append((ship, bullet))
        return collisions


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple, img):
        super().__init__()
        self.image = img
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.acceleration = 1
        self.ang_vel = 1
        self.max_speed = 10

    def update(self, dt, keys):
        if keys[pygame.K_w]:
            self.vel += pygame.Vector2(0, -self.acceleration).rotate(self.angle) * dt
        if keys[pygame.K_a]:
            self.angle += self.ang_vel * dt

        if keys[pygame.K_d]:
            self.angle -= self.ang_vel * dt

        self.vel = self.vel.normalize() * min(self.vel.length(), self.max_speed)

        self.pos = self.pos.x + self.vel.x, self.pos.y + self.vel.y
        # self.velocity = self.velocity.normalize() * min(self.velocity.length(), self.max_speed)
        # self.rect.move_ip(self.velocity.x, self.velocity.y)
        # self.image = pygame.transform.rotate(self.original_image, self.angle)
        # self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos: pygame.Vector2, vel: pygame.Vector2):
        super().__init__()
        self.image = image
        self.pos: pygame.Vector2 = pos
        self.vel: pygame.Vector2 = vel

    def update(self, dt):
        self.pos = self.vel * dt

    def draw(self, screen):
        screen.blit(self.image, self.pos)


class Game:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.cooldown = 0
        self.bullets = []
        self.ships = []
        self.player = Player((self.screen.get_width() // 2, self.screen.get_height() // 2))

    def main_loop(self):
        while True:
            self.handle_keys()
            self.update()
            self.draw()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def update(self):
        dt = self.clock.tick(60) / 1000
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     x -= speed * delta
        # if keys[pygame.K_RIGHT]:
        #     x += speed * delta
        # if keys[pygame.K_UP]:
        #     y -= speed * delta
        # if keys[pygame.K_DOWN]:
        #     y += speed * delta
        # if keys[pygame.K_SPACE] and self.cooldown >= 0.5:
        #     pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg_image, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    game = Game(1920, 1080)
    game.main_loop()
