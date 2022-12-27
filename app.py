import time
from os import path
from random import seed

import arcade
from stable_baselines3 import PPO

from environment import AppleRainEnv
from game import AppleRainGame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Sprites and Bullets Example"

MODEL_PATH = path.join('models', f'model')
LOGS_PATH = path.join('logs')

def main():
    env = AppleRainEnv()

    def train_and_save_model(model):
        model.learn(total_timesteps=3000000)
        model.save(MODEL_PATH)

    if not path.exists(MODEL_PATH + '.zip'):
        model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=LOGS_PATH)
        train_and_save_model(model)
    else:
        model = PPO.load(MODEL_PATH)
        model.set_env(env)
    #     train_and_save_model(model)

    seed(1)

    for i in range(1):
        done = False
        score = 0
        obs = env.reset()
        while not done:
            # action = env.action_space.sample()
            action, _ = model.predict(obs)

            obs, reward, done, info = env.step(action)
            score += reward
            env.render(3000)
        print(score)
    env.close()


    # window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # game = AppleRainGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    # window.show_view(game)
    # game.setup()

    # while True:
    #     time.sleep(1/100)
    #     game.on_update(1/60)
    #
    #     window.dispatch_events()
    #
    #     arcade.start_render()
    #     game.on_draw()
    #     arcade.finish_render()
    # arcade.run()


if __name__ == "__main__":
    main()