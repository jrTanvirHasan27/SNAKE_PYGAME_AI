import pygame
import random
from enum import Enum
pygame.init()


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode(self.w, self.h)
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = "R"

    def play_step(self):
        pass


if __name__ == '__main__':
    game = SnakeGame()

    # game Loop
    while True:
        game.play_step()

        # break if game over

    pygame.quit()
