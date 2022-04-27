import pygame
import random
import numpy as np
from collections import namedtuple
from enum import Enum

pygame.init()
font = pygame.font.Font('OpenSans-Regular.ttf', 20)


# reset
# reward
# play(action) -> direction
# iteration_of_game
# is_collide

class Direction(Enum):
    RIGHT = 1
    UP = 3
    DOWN = 4
    LEFT = 2


point = namedtuple('point', ('x', 'y'))
BLOCK_SIZE = 20
SPEED = 10

# rgb colors

BLACK = (0, 0, 0)
GREEN = (173, 202, 21)
WHITE = (255, 255, 255)
CYAN = (191, 250, 243)


class SnakeGame:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = point(self.w / 2, self.h / 2)
        self.snake = [self.head,
                      point(self.head.x - BLOCK_SIZE, self.head.y),
                      point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = point(x, y)
        if self.food in self.snake:
            self._place_food()

    def step_play(self, action):
        self.frame_iteration += 1

        # Collect User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move
        self._move(action)  # update head
        self.snake.insert(0, self.head)

        # Check if game over
        reward = 0
        game_Over = False
        if self._is_collide() or self.frame_iteration > 100*len(self.snake):
            reward = -10
            game_Over = True
            return reward, game_Over, self.score

        # place food or move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # update Ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # return game over and score
        return reward, game_Over, self.score

    def _is_collide(self, pt=None):
        if pt in None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > pt - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(CYAN)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLACK, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, WHITE, pygame.Rect(pt.x + 3, pt.y + 4, 14, 14))

        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        index = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[index]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_index = (index + 1) % 4
            new_dir = clock_wise[next_index]  # right turn  r -> d -> l -> u
        else:
            next_index = (index + 1) % 4
            new_dir = clock_wise[next_index]  # left turn  r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = point(x, y)


