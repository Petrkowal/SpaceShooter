import math
import pygame
import threading

from SpaceShooter import Game
from player import Player
from enemy import Enemy
from bullet import Bullet

class Helper:
    def __init__(self, game):
        self.game = game


    def main_loop(self):
        dt = self.game.clock.tick(60) / 1000
        

if __name__ == "__main__":
    pygame.init()

    game = Game(1280, 720)
    game.main_loop()
    game_thread = threading.Thread(target=game.main_loop)
    game_thread.start()
    helper_thread = threading.Thread(target=Helper(game).main_loop)
    helper_thread.start()

