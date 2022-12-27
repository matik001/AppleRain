import random
import time
from enum import Enum
from typing import Literal, Tuple

import arcade
import numpy as np
from arcade import Window
from gym import Env
from gym.spaces import Discrete, Box, Dict

from game import AppleRainGame, MoveType

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Super Apple Rain"


class AppleRainEnv(Env):
    def __init__(self):
        self.game: AppleRainGame = None
        self.action_space = Discrete(3)
        # self.observation_space = Dict({
        #     'player_pos': Box(0, 1, (2,)),
        #     'apples': Box(0, 1, (10, 2))
        # })
        self.observation_space = Box(0, 1, (10, 2))
        self.window: Window = None

    def step(self, action: int):
        score = self.game.score
        # if self.window:
        #     self.window.dispatch_events()
        self.game.move_player(MoveType(action))
        self.game.on_update(1 / 60)
        reward = self.game.score - score
        terminated = self.game.is_finished()
        obs = self._game_to_obs()
        info = self._get_info()
        return obs, reward, terminated, info

    # def _game_to_obs(self):
    #     return {
    #         'player_pos': np.array(self.game.get_player_pos()),
    #         'apples': np.array(self.game.get_apples_pos())
    #     }
    def _normalize_pos(self, pos: Tuple[float, float]):
        return [pos[0] / SCREEN_WIDTH, pos[1] / SCREEN_HEIGHT]

    def _game_to_obs(self):
        obs_arr = [self._normalize_pos(self.game.get_player_pos())]
        obs_arr.extend([self._normalize_pos(p) for p in self.game.get_apples_pos()])
        while len(obs_arr) < 10:
            obs_arr.append([0.5,1])

        return np.array(obs_arr)

    def _get_info(self):
        return {}

    def reset(self):
        if not self.window:
            self.window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game = AppleRainGame(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.game.setup()
        self.window.show_view(self.game)

        obs = self._game_to_obs()
        info = self._get_info()
        return obs

    def render(self, speed=200):
        time.sleep(1 / speed)
        arcade.start_render()
        self.game.on_draw()
        arcade.finish_render()

    def close(self):
        super().close()
        self.window.close()
