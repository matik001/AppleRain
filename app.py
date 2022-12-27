import random
import time
from os import path
from random import seed

import arcade
from stable_baselines3 import PPO

from environment import AppleRainEnv
from game import AppleRainGame
from window import GameWindow

def main():

    window = GameWindow()
    seed = random.randint(1, 1000000)
    print(f'Seed={seed}')
    window.play(False, seed)
    window.play(True, seed)
    # window.train_model()


if __name__ == "__main__":
    main()