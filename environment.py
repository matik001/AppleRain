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


class AppleRainEnv(Env):
    def __init__(self, window:Window):
        self.game: AppleRainGame = None
        self.action_space = Discrete(3)
        self.observation_space = Box(0, 1, (10, 2))
        self.window: Window = window

    def step(self, action: int):
        score = self.game.score

        self.window.dispatch_events()
        self.game.move_player(MoveType(action))
        self.game.on_update(1 / 60)
        reward = self.game.score - score
        terminated = self.game.is_finished()
        obs = self._game_to_obs()
        info = self._get_info()
        return obs, reward, terminated, info

    def _normalize_pos(self, pos: Tuple[float, float]):
        return [pos[0] / self.window.width, pos[1] / self.window.height]

    def _game_to_obs(self):
        obs_arr = [self._normalize_pos(self.game.get_player_pos())]
        obs_arr.extend([self._normalize_pos(p) for p in self.game.get_apples_pos()])
        while len(obs_arr) < 10:
            obs_arr.append([0.5,1])

        return np.array(obs_arr)

    def _get_info(self):
        return {}

    def reset(self):
        self.game = AppleRainGame(self.window.width, self.window.height)
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
