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
        pass

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
