import pygame
import random
from collections import namedtuple
from enum import Enum

pygame.init()


class Direction(Enum):
    RIGHT = 1
    UP = 3
    DOWN = 4
    LEFT = 2


point = namedtuple('point', ('x', 'y'))
BLOCK_SIZE = 20


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      point(self.head.x - BLOCK_SIZE, self.head.y),
                      point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # Collect User Input
        # Move
        # Check if game over
        # update Ui and clock
        # return game over and score
        game_Over = False
        return game_Over, self.score


if __name__ == '__main__':
    game = SnakeGame()

    # game Loop
    while True:
        game_Over, score = game.play_step()

        # break if game over
        if game_Over:
            break

    print('Final Score: ', score)

    pygame.quit()
