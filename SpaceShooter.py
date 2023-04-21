import random
import pygame
from player import Player
from enemy import Enemy
from bullet import Bullet


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
        self.borders = [0, 0, self.screen.get_width(), self.screen.get_height()]
        self.enemy_img = pygame.image.load('images/ship.png')
        self.bullet_img = pygame.image.load('images/bullet.png')
        self.enemies = []
        self.keys = []
        self.score = 0
        self.end = False

    def main_loop(self):
        while True:
            self.handle_keys()
            self.update()
            self.draw()
            if self.end:
                break
        self.game_over()

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_SPACE] and self.player.get_cooldown() > 0.5:
            self.player.reset_cooldown()
            pos = self.player.pos + (self.player.image.get_width() // 2, self.player.image.get_height() // 2)
            pos = pygame.Vector2(pos[0], pos[1])
            self.bullets.append(Bullet(self.bullet_img, pos, self.player.angle, True))

    def new_enemy(self):
        a, b = random.randint(0, 3), random.random()
        if a == 0:
            vel = pygame.Vector2(100, 0).rotate(random.randint(-30, 30))
            self.enemies.append(Enemy((0, self.screen.get_height() * b), (vel[0], vel[1]), self.enemy_img))
        elif a == 1:
            vel = pygame.Vector2(0, 100).rotate(random.randint(-30, 30))
            self.enemies.append(Enemy((self.screen.get_width() * b, 0), (vel[0], vel[1]), self.enemy_img))
        elif a == 2:
            vel = pygame.Vector2(-100, 0).rotate(random.randint(-30, 30))
            self.enemies.append(
                Enemy((self.screen.get_width(), self.screen.get_height() * b), (vel[0], vel[1]), self.enemy_img))
        elif a == 3:
            vel = pygame.Vector2(0, -100).rotate(random.randint(-30, 30))
            self.enemies.append(
                Enemy((self.screen.get_width() * b, self.screen.get_height()), (vel[0], vel[1]), self.enemy_img))

    def update(self):
        dt = self.clock.tick(60) / 1000
        self.player.update(dt, self.keys, self.borders)
        while len(self.enemies) < 3:
            self.new_enemy()
        to_remove = []
        for enemy in self.enemies:
            enemy.update(dt, self.player.pos)
            if enemy.pos[0] < 0 or enemy.pos[0] > self.screen.get_width() or enemy.pos[1] < 0 or enemy.pos[
                1] > self.screen.get_height():
                to_remove.append(enemy)
            if enemy.cooldown > random.randint(1, 10):
                enemy.cooldown = 0
                pos = enemy.pos
                pos = pygame.Vector2(pos[0], pos[1])
                self.bullets.append(Bullet(self.bullet_img, pos, enemy.angle, False))
        for enemy in to_remove:
            self.enemies.remove(enemy)
        for bullet in self.bullets:
            bullet.update(dt)
        for bullet in self.bullets:
            for enemy in self.enemies:
                if pygame.sprite.collide_mask(enemy, bullet):
                    if bullet.player:
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        self.score += 1
            if pygame.sprite.collide_mask(self.player, bullet):
                if not bullet.player:
                    self.bullets.remove(bullet)
                    self.player.hp -= 10
        if self.player.hp <= 0:
            self.end = True

    def game_over(self):
        while True:
            font = pygame.font.SysFont('Arial', 72)
            text = font.render('Game Over', True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
            self.screen.blit(text, text_rect)
            font = pygame.font.SysFont('Arial', 72)
            text = font.render(f'Score: {self.score}', True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 100)
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.clock.tick(10)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for bullet in self.bullets:
            bullet.draw(self.screen)
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        font = pygame.font.SysFont('Arial', 48)
        text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.screen.get_width() // 2, 50)
        self.screen.blit(text, text_rect)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    game = Game(1280, 720)
    game.main_loop()
