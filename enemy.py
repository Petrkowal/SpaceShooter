import pygame
from typing import Tuple
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple, vel: Tuple, img):
        super(Enemy, self).__init__()
        self.const_image = pygame.transform.scale(img, (
            img.get_width() * 0.05, img.get_height() * 0.05))
        self.angle = 90
        self.image = pygame.transform.rotate(self.const_image, -self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=pos)
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.vel = pygame.Vector2(vel[0], vel[1])
        self.cooldown = 0

    def update(self, dt, player_pos):
        self.cooldown += dt
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        self.angle = math.degrees(math.atan2(dy, dx)) + 90
        self.image = pygame.transform.rotate(self.const_image, -self.angle)
        self.pos += self.vel * dt
        self.rect = self.mask.get_rect(center=self.pos)

    def draw(self, screen):
        pos_img = self.pos[0] - self.image.get_width() // 2, self.pos[1] - self.image.get_height() // 2
        screen.blit(self.image, pos_img)
