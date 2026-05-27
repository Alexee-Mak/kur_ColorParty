from ursina import *
import random
import config
from game_mode import GameMode


class InfinitiMode(GameMode):
    def __init__(self):
        super().__init__()

    def create_field(self):
        if not config.game_active or not config.alive:
            return

        for b in config.blocks:
            destroy(b)
        config.blocks.clear()

        config.round_count += 1
        if config.round_text:
            config.round_text.text = f'Round: {config.round_count}'

        config.safe_color = random.choice(config.ALL_COLORS)
        for ind in config.indicators:
            ind.color = config.safe_color

        for x in range(config.GRID_SIZE):
            for z in range(config.GRID_SIZE):
                col = config.safe_color if random.random() < 0.2 else random.choice(config.ALL_COLORS)
                block = Entity(
                    model='cube',
                    color=col,
                    texture='white_cube',
                    position=(
                        x * config.BLOCK_SIZE - config.GRID_SIZE * config.BLOCK_SIZE / 2,
                        0,
                        z * config.BLOCK_SIZE - config.GRID_SIZE * config.BLOCK_SIZE / 2
                    ),
                    scale=config.BLOCK_SIZE,
                    collider='box',
                    shader="lit_with_shadows_shader"
                )
                config.blocks.append(block)

        config.TIME_LIMIT = config.TRUE_TIME_LIMIT
        if config.timer_text:
            config.timer_text.text = f'Time left: {config.TIME_LIMIT}'
        self.start_timer()

    def init_game(self):
        config.TIME_LIMIT = config.TRUE_TIME_LIMIT
        config.timer_text = Text(
            text=f'Time left: {config.TIME_LIMIT}',
            position=(0, 0.45),
            scale=2,
            origin=(0, 0)
        )
        config.round_text = Text(
            text='Round: 0',
            position=(-0.75, 0.45),
            scale=2,
            origin=(0, 0)
        )
        self.create_indicators()
        self.create_field()

