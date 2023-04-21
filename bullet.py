import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, pos: pygame.Vector2, angle, player: bool):
        super(Bullet, self).__init__()
        self.image = pygame.transform.rotate(
            pygame.transform.scale(image, (image.get_width() // 40, image.get_height() // 40)), -angle)
        self.pos: pygame.Vector2 = pos
        vel = 400 if player else 200
        self.vel = pygame.Vector2(vel, 0).rotate(angle - 90)
        self.player = player
        self.angle = angle
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect(center=self.pos)

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect = self.mask.get_rect(center=self.pos)

    def draw(self, screen):
        screen.blit(self.image, self.pos)
