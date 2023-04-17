import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
g = 9.81
CIRCLE_WIDTH = 40

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


class Player:
    def __init__(self, pos):
        self.pos = pos
        self.speed = 300
        self.size = 40
        self.vel = pygame.Vector2(0, 0)

    def setpos(self, pos):
        if pos.x < 0 + CIRCLE_WIDTH:
            pos.x = 0 + CIRCLE_WIDTH
            self.vel.x = abs(self.vel.x * 0.8)
        if pos.x > screen.get_width() - CIRCLE_WIDTH:
            pos.x = screen.get_width() - CIRCLE_WIDTH
            self.vel.x = -abs(self.vel.x * 0.8)
        if pos.y < 0 + CIRCLE_WIDTH:
            pos.y = 0 + CIRCLE_WIDTH
            self.vel.y = abs(self.vel.y * 0.8)
        if pos.y > screen.get_height() - CIRCLE_WIDTH:
            pos.y = screen.get_height() - CIRCLE_WIDTH
            self.vel.y = -abs(self.vel.y * 0.8)
        self.pos = pos

    def update(self):
        self.vel.y += g * 100 * dt
        self.vel *= 0.995
        self.pos += self.vel * dt
        self.setpos(self.pos)

    def place(self, pos):
        self.vel = pygame.Vector2(0, 0)
        self.setpos(pos)

    def throw(self, pos, vel):
        self.vel = vel
        self.setpos(pos)


player = Player(pygame.Vector2(100, 100))

mouse_trajectory = []


def calc_mouse_vector(trajectory):
    return pygame.Vector2((trajectory[-1][0] - trajectory[0][0]) / len(trajectory),
                          (trajectory[-1][1] - trajectory[0][1]) / len(trajectory))


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.draw.circle(screen, "red", player.pos, player.size)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt
    #

    mouse_lmb = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    mouse_trajectory.append(mouse_pos)
    if len(mouse_trajectory) > 10:
        mouse_trajectory.pop(0)
    if mouse_lmb:
        player.throw(mouse_pos, calc_mouse_vector(mouse_trajectory) * 100)

    pygame.display.flip()

    player.update()
    dt = clock.tick(60) / 1000

pygame.quit()
