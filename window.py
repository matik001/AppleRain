import random
from os import path

import arcade
from arcade import Window
from stable_baselines3 import PPO
from environment import AppleRainEnv

MODEL_PATH = path.join('models', f'model')
LOGS_PATH = path.join('logs')

SCREEN_WIDTH = 1600
GAME_WIDTH = SCREEN_WIDTH//2
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Apple Rain by Matik"


class GameWindow:
    def __init__(self) -> None:
        super().__init__()
        self.window = Window(GAME_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, center_window=True)
        self.env = AppleRainEnv(self.window)
        self.model = self._load_or_create_model()
        self.next_move = 0



    def play(self, ai:bool = False, seed = -1):
        self.window.on_key_press = self.window.on_key_release = lambda a, b: None
        if not ai:
            self.window.on_key_press = self._on_key_press
            self.window.on_key_release = self._on_key_release

        done = False
        score = 0
        obs = self.env.reset()

        if seed != -1:
            random.seed(seed)

        while not done:
            if ai:
                action, _ = self.model.predict(obs)
            else:
                action = self.next_move+1
            obs, reward, done, info = self.env.step(action)
            score += reward
            self.env.render(3000)
        print(f'Score: {score}')

    def train_model(self, amount=100000):
        for i in range(100000):
            self.model.learn(total_timesteps=amount)
            self.model.save(MODEL_PATH)

    def _load_or_create_model(self):
        if not path.exists(MODEL_PATH + '.zip'):
            model = PPO('MlpPolicy', self.env, verbose=1, tensorboard_log=LOGS_PATH)
        else:
            model = PPO.load(MODEL_PATH)
            model.set_env(self.env)
        return model


    def _on_key_press(self, symbol: int, modifiers: int):
        if symbol != arcade.key.LEFT and symbol != arcade.key.RIGHT:
            return
        dx = 1
        if symbol == arcade.key.LEFT:
            dx = -dx
        self.next_move += dx

    def _on_key_release(self, symbol: int, _modifiers: int):
        if symbol != arcade.key.LEFT and symbol != arcade.key.RIGHT:
            return
        dx = 1
        if symbol == arcade.key.RIGHT:
            dx = -dx
        self.next_move += dx