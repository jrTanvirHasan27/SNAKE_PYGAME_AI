import pygame
import random
from collections import namedtuple
from enum import Enum

pygame.init()
font = pygame.font.Font('OpenSans-Regular.ttf', 20)


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
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = point(x, y)
        if self.food in self.snake:
            self._place_food()

    def step_play(self):
        # Collect User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        # Move
        self._move(self.direction)      # update head
        self.snake.insert(0, self.head)

        # Check if game over
        game_Over = False
        if self._is_collide():
            game_Over = True

        # place food or move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # update Ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # return game over and score
        return game_Over, self.score

    def _is_collide(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
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

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = point(x, y)


if __name__ == '__main__':
    game = SnakeGame()

    # game Loop
    while True:
        game_Over, score = game.step_play()

        # break if game over
        if game_Over:
            break

    print('Your Score:', score)

    pygame.quit()
