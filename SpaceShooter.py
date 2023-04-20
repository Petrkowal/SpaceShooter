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
    def __init__(self, pos: Tuple, img, img_acc):
        super().__init__()
        img_resize_factor = 0.1
        self.const_img = pygame.transform.scale(img, (
        img.get_width() * img_resize_factor, img.get_height() * img_resize_factor))
        self.const_img_acc = pygame.transform.scale(img_acc, (
        img_acc.get_width() * img_resize_factor, img_acc.get_height() * img_resize_factor))
        self.image = self.const_img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rot_img = self.image
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.acceleration = 2
        self.ang_vel = 90
        self.max_speed = 3

    def update(self, dt, keys, bounds):
        if keys[pygame.K_w]:
            self.vel += pygame.Vector2(0, -self.acceleration).rotate(self.angle) * dt
            self.image = self.const_img_acc
        else:
            self.image = self.const_img
        if keys[pygame.K_a]:
            self.angle -= self.ang_vel * dt

        if keys[pygame.K_d]:
            self.angle += self.ang_vel * dt

        if self.vel.x != 0 or self.vel.y != 0:
            self.vel = self.vel.normalize() * min(self.vel.length(), self.max_speed)

        self.pos = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
        self.rect = self.rot_img.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.rot_img)
        border_collisions = CollisionDetector.detect_collision([self], bounds)

        if bounds[0] in border_collisions:
            self.pos = bounds[0], self.pos[1]
            self.vel[0] = self.vel[0] / 10
        if bounds[2] in border_collisions:
            self.pos = bounds[2], self.pos[1]
            self.vel[0] = self.vel[0] / 10
        if bounds[1] in border_collisions:
            self.pos = self.pos[0], bounds[1]
            self.vel[1] = self.vel[1] / 10
        if bounds[3] in border_collisions:
            self.pos = self.pos[0], bounds[3]
            self.vel[1] = self.vel[1] / 10
        # self.velocity = self.velocity.normalize() * min(self.velocity.length(), self.max_speed)
        # self.rect.move_ip(self.velocity.x, self.velocity.y)
        # self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen):
        self.rot_img = pygame.transform.rotate(self.image, -self.angle)
        pos_img = self.pos[0] - self.rot_img.get_width() // 2, self.pos[1] - self.rot_img.get_height() // 2
        screen.blit(self.rot_img, pos_img)


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
        self.player = Player((self.screen.get_width() // 2, self.screen.get_height() // 2),
                             pygame.image.load('images/ship.png'), pygame.image.load('images/ship_acc.png'))
        self.edges = [
            pygame.Rect(0, 0, self.screen.get_width(), 1),
            pygame.Rect(0, 0, 1, self.screen.get_height()),
            pygame.Rect(self.screen.get_width() - 1, 0, 1, self.screen.get_height()),
            pygame.Rect(0, self.screen.get_height() - 1, self.screen.get_width(), 1)
        ]

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
        self.player.update(dt, keys, (0, 0, self.edges))

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
        # self.screen.blit(self.bg_image, (0, 0))
        self.player.draw(self.screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    game = Game(1280, 720)
    game.main_loop()
