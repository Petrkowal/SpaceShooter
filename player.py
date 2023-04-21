import pygame
from typing import Tuple


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple, img, img_acc):
        super(Player, self).__init__()
        img_resize_factor = 0.05
        self.const_img = pygame.transform.scale(img, (
            img.get_width() * img_resize_factor, img.get_height() * img_resize_factor))
        self.const_img_acc = pygame.transform.scale(img_acc, (
            img_acc.get_width() * img_resize_factor, img_acc.get_height() * img_resize_factor))
        self.selected_image = self.const_img
        self.mask = pygame.mask.from_surface(self.selected_image)
        self.rect = self.mask.get_rect(center=pos)
        self.image = self.selected_image
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.vel = pygame.Vector2(0, 0)
        self.angle = 0
        self.acceleration = 2
        self.ang_vel = 90
        self.max_speed = 3
        self.cooldown = 0
        self.hp = 100

    def get_cooldown(self):
        return self.cooldown

    def reset_cooldown(self):
        self.cooldown = 0

    def update(self, dt, keys, borders):
        self.cooldown += dt
        if keys[pygame.K_w]:
            self.vel += pygame.Vector2(0, -self.acceleration).rotate(self.angle) * dt
            self.selected_image = self.const_img_acc
        else:
            self.selected_image = self.const_img
        if keys[pygame.K_a]:
            self.angle -= self.ang_vel * dt

        if keys[pygame.K_d]:
            self.angle += self.ang_vel * dt

        if self.vel.x != 0 or self.vel.y != 0:
            self.vel = self.vel.normalize() * min(self.vel.length(), self.max_speed)

        self.pos = self.pos[0] + self.vel[0], self.pos[1] + self.vel[1]
        self.mask = pygame.mask.from_surface(pygame.transform.rotate(self.const_img, -self.angle))
        self.rect = self.mask.get_rect(center=self.pos)

        if self.pos[0] - self.image.get_width() // 2 <= borders[0]:
            self.pos = borders[0] + self.image.get_width() // 2 + 1, self.pos[1]
            self.vel[0] = self.vel[0] / 10
        if self.pos[0] + self.image.get_width() // 2 >= borders[2]:
            self.pos = borders[2] - self.image.get_width() // 2 - 1, self.pos[1]
            self.vel[0] = self.vel[0] / 10
        if self.pos[1] - self.image.get_height() // 2 <= borders[1]:
            self.pos = self.pos[0], borders[1] + self.image.get_height() // 2 + 1
            self.vel[1] = self.vel[1] / 10
        if self.pos[1] + self.image.get_height() // 2 >= borders[3]:
            self.pos = self.pos[0], borders[3] - self.image.get_height() // 2 - 1
            self.vel[1] = self.vel[1] / 10

    def draw(self, screen):
        self.image = pygame.transform.rotate(self.selected_image, -self.angle)
        pos_img = self.pos[0] - self.image.get_width() // 2, self.pos[1] - self.image.get_height() // 2
        screen.blit(self.image, pos_img)
        pygame.draw.rect(screen, (255, 0, 0), (
            self.pos[0] - self.const_img.get_width() // 2, self.pos[1] - self.const_img.get_height() // 2 - 10,
            self.const_img.get_width(), 5))
        pygame.draw.rect(screen, (0, 255, 0), (
            self.pos[0] - self.const_img.get_width() // 2, self.pos[1] - self.const_img.get_height() // 2 - 10,
            self.const_img.get_width() * self.hp / 100, 5))
