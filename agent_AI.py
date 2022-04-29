import torch
import random
from collections import deque
import numpy as np
from Snake_Game_ai import AISnakeGame, Direction, point

MEMORY_MAX = 100_100
SIZE_BATCH = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.no_game = 0
        self.epsilon = 0  # for randomness
        self.gamma = 0    # discount rate
        self.memory = deque(maxlen=MEMORY_MAX)  #  popleft()
        # Todo: model, trainer

    def state_get(self, game):
        head = game.snake[0]
        point_l = point(head.x-20, head.y)
        point_r = point(head.x+20, head.y)
        point_u = point(head.x, head.y-20)
        point_d = point(head.x, head.y+20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game._is_collide(point_r)) or
            (dir_l and game._is_collide(point_l)) or
            (dir_u and game._is_collide(point_u)) or
            (dir_d and game._is_collide(point_d)),

            # Danger right
            (dir_u and game._is_collide(point_r)) or
            (dir_d and game._is_collide(point_l)) or
            (dir_l and game._is_collide(point_u)) or
            (dir_r and game._is_collide(point_d)),

            # Danger left
            (dir_d and game._is_collide(point_r)) or
            (dir_u and game._is_collide(point_l)) or
            (dir_r and game._is_collide(point_u)) or
            (dir_l and game._is_collide(point_d)),

            # Move Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d

            # Food Location
            game.food.x < game.head.x,    # left food
            game.food.x > game.head.x,    # right food
            game.food.y < game.head.y,    # up food
            game.food.y > game.head.y     # down food
        ]

        return np.array(state, dtype=int)


    def remember(self, state, action, reward, state_next, done):
        pass

    def long_memory_train(self):
        pass

    def short_memory_train(self, state, action, reward, state_next, done):
        pass

    def action_get(self, state):
        pass


 def train():
     scores_plot = []
     mean_scores_plot = []
     scores_total = 0
     record = 0
     agent = Agent()
     game = AISnakeGame()
     while True:
         # get old state
         old_state = agent.state_get(game)

         # get move
         final_move = agent.action_get(old_state)

         # move perfection
         reward, done, score = game.step_play(final_move)
         new_state = agent.state_get(game)

         # train short memory
         agent.short_memory_train(old_state, final_move, reward, new_state, done)

         # remember
         agent.remember(old_state, final_move, reward, new_state, done)

         if done:
             # train the long memory, result plotting
             game.reset()
             agent.no_game += 1
             agent.long_memory_train()

             if score > record:
                 record = score
                 # agent.model.save()

             print('Game', agent.no_game, 'Score', score, 'Record', record)

             # TODO: plotting


if __name__ == '__main__':
    train()
