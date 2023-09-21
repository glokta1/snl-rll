import numpy as np
import random
import gymnasium as gym
import pygame


class SNLGym(gym.Env):
    def __init__(self, max_position):
        self.max_position = max_position
        self.state = 1  # initial state is position 1
        self.snakes = [(3, 97), (47, 74), (57, 71)]
        self.ladders = [(6, 23), (12, 37), (43, 61)]
        self.ladder = True

    def reset(self):
        self.state = 1

    def step(self, action):
        # roll the die and move the player forward
        steps = random.randint(1, 6)
        self.state += steps

        # check if the player landed on a snake or ladder
        if self.state in snakes:
            self.state = snakes[self.state]
        elif self.state in ladders:
            self.state = ladders[self.state]

        # check if the game has ended
        done = self.state >= self.max_position

        # compute the reward
        if done:
            reward = 100.0  # the agent wins the game
        elif not done:
            reward = -100  # agent loses the game
        elif self.ladder:
            reward = 10  # reward for landing on ladder
        elif self.snake:
            reward = -10  # penalty for landing on snake

        return self.state, reward, done, {}

    def render(self):
        # render game using pygame
        snl.play()

    def close(self):
        pygame.quit()
