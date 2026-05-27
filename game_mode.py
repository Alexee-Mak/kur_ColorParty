from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController
import config


class GameMode:
    def __init__(self):
        pass

    def create_indicators(self):
        for ind in config.indicators:
            destroy(ind)
        config.indicators.clear()

        half_size = config.GRID_SIZE * config.BLOCK_SIZE / 2
        offset = 1.5
        y_level = 2 + config.BLOCK_SIZE

        positions = [
            (0, y_level, half_size + offset),
            (0, y_level, -half_size - offset),
            (-half_size - offset, y_level, 0),
            (half_size + offset, y_level, 0)
        ]
        rotations = [(0, 0, 0), (0, 0, 0), (0, 90, 0), (0, -90, 0)]

        for pos, rot in zip(positions, rotations):
            ind = Entity(
                model='cube',
                color=config.safe_color,
                position=pos,
                rotation=rot,
                scale=(0.5 * config.GRID_SIZE * config.BLOCK_SIZE, 0.8, 0.2),
                collider=None
            )
            config.indicators.append(ind)

    def create_field(self):
        raise NotImplementedError("Метод create_field должен быть реализован в наследнике")

    def start_timer(self):
        if not config.game_active or not config.alive:
            return
        if config.TIME_LIMIT > 0:
            config.TIME_LIMIT -= 1
            if config.timer_text:
                config.timer_text.text = f'Time left: {config.TIME_LIMIT}'
            invoke(self.start_timer, delay=1)
        else:
            self.remove_wrong_colors()

    def remove_wrong_colors(self):
        if not config.game_active or not config.alive:
            return

        for b in config.blocks:
            if b.color != config.safe_color:
                destroy(b)

        config.timer_text.text = "New field in 3 seconds..."
        invoke(self.create_field, delay=3)

    def init_game(self):
        raise NotImplementedError("Метод init_game должен быть реализован в наследнике")

    def start_game(self, new_grid=None, new_block=None, new_time=None):
        if new_grid is not None:
            config.GRID_SIZE = new_grid
        if new_block is not None:
            config.BLOCK_SIZE = new_block
        if new_time is not None:
            config.TRUE_TIME_LIMIT = new_time

        config.game_active = True
        config.alive = True
        config.round_count = 0

        config.player = FirstPersonController()
        center_x = (config.GRID_SIZE // 2) * config.BLOCK_SIZE - config.GRID_SIZE * config.BLOCK_SIZE / 2
        center_z = (config.GRID_SIZE // 2) * config.BLOCK_SIZE - config.GRID_SIZE * config.BLOCK_SIZE / 2
        config.player.position = (center_x, config.BLOCK_SIZE + 10, center_z)

        self.init_game()

    def die(self):
        if not config.alive:
            return

        config.alive = False
        config.game_active = False

        for b in config.blocks:
            destroy(b)
        config.blocks.clear()

        for ind in config.indicators:
            destroy(ind)
        config.indicators.clear()

        if config.timer_text:
            destroy(config.timer_text)
            config.timer_text = None

        if config.round_text:
            destroy(config.round_text)
            config.round_text = None

        if config.player:
            destroy(config.player)
            config.player = None

        death_msg = Text(
            text=f"YOU FELL INTO THE VOID\nGAME OVER\nRounds survived: {config.round_count}",
            origin=(0, 0),
            scale=3,
            color=color.red
        )

        invoke(self.return_to_menu, delay=3)
        invoke(destroy, death_msg, delay=3)

    def return_to_menu(self):
        config.round_count = 0
        config.alive = True
        config.game_active = False
        if config.menu:
            config.menu.show()

    def update(self):
        if config.game_active and config.player and config.player.y < config.DEATH_Y:
            self.die()