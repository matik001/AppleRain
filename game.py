import random
from enum import Enum, IntEnum
from typing import Tuple, cast

import arcade
import os

from arcade import Sprite, SpriteList


class Player(arcade.Sprite):
    def __init__(self, screen_width: int):
        super().__init__('assets/man.png')
        self.screen_width = screen_width
        self.set_hit_box([(-self.width/2, self.height/2), (self.width/2, self.height/2),
                          (self.width/2, self.height/2-20), (-self.width/2, self.height/2-20)])
    def on_update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y * delta_time

        if self.left < 0:
            self.left = 0
        elif self.right >= self.screen_width:
            self.right = self.screen_width - 1

class Apple(arcade.Sprite):
    FALL_SPEED = 300
    def __init__(self, screen_height: int):
        super().__init__('assets/apple.png')
        self.screen_height = screen_height
        self.change_y = -Apple.FALL_SPEED
        self.scale = 0.6
    def on_update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x * delta_time
        self.center_y += self.change_y* delta_time
    def is_outside_screen(self):
        return self.top < 0


SHOW_HITBOX = False

class MoveType(IntEnum):
    LEFT = 0
    NOTHING = 1
    RIGHT = 2
class AppleRainGame(arcade.View):
    APPLE_CREATE_INTERVAL = 0.5
    MAX_GAME_TIME = 30
    PLAYER_SPEED = 400
    def __init__(self, width:int, height:int):
        super().__init__()
        self.width = width
        self.height = height
        self.player:Player = None
        self.score = 0
        self.total_game_time = 0
        self.amount_of_created_apples = 0

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.player = Player(self.width)
        self.player.set_position(self.width/2, 70)
        self.apples = SpriteList()
        self.score = 0

        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        self.player.draw()
        self.apples.draw()
        if SHOW_HITBOX:
            self.apples.draw_hit_boxes(line_thickness=3)
            self.player.draw_hit_box((255, 255, 255), 3)
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

    def _create_apple(self):
        self.amount_of_created_apples += 1

        new_apple = Apple(self.height)
        min_x = new_apple.width // 2
        max_x = self.width - new_apple.width // 2
        y = self.height + new_apple.height // 2
        new_apple.set_position(random.uniform(min_x, max_x), y)

        self.apples.append(new_apple)

    def _create_apples(self):
        new_amount = self.total_game_time // AppleRainGame.APPLE_CREATE_INTERVAL
        while new_amount > self.amount_of_created_apples:
            self._create_apple()

    def _handle_catch(self):
        caught_apples = arcade.check_for_collision_with_list(self.player, self.apples)
        for apple in caught_apples:
            apple.remove_from_sprite_lists()
            self.score += 1
    def _remove_off_screen_apples(self):
        for apple in self.apples:
            apple = cast(Apple, apple)
            if apple.is_outside_screen():
                apple.remove_from_sprite_lists()
                # self.score -= 1

    def move_player(self, type:MoveType):
        self.player.change_x = (type-1) * AppleRainGame.PLAYER_SPEED
    def on_update(self, delta_time):
        if self.is_finished():
            return
        self.total_game_time += delta_time
        self._create_apples()

        self._remove_off_screen_apples()
        self._handle_catch()
        self.player.on_update(delta_time)
        self.apples.on_update(delta_time)

    def get_player_pos(self):
        return self.player.position
    def get_apples_pos(self):
        return [apple.position for apple in self.apples]
    def is_finished(self):
        return self.total_game_time >= AppleRainGame.MAX_GAME_TIME
