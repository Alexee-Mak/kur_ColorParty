from ursina import *
import random

from ursina.shaders import lit_with_shadows_shader

import config
from game_mode import GameMode


class BossMode(GameMode):
    def __init__(self):
        super().__init__()
        config.GRID_SIZE = 20
        config.BLOCK_SIZE = 2
        config.TRUE_TIME_LIMIT = 6
        self.boss = None
        self.boss_rounds = 1
        self.list_bones = []

    def create_field(self):
        if not config.game_active or not config.alive:
            return

        for b in config.blocks:
            destroy(b)
        config.blocks.clear()

        config.round_count += 1
        config.round_text.text = f'Round: {config.round_count}'

        config.safe_color = random.choice(config.ALL_COLORS)
        for ind in config.indicators:
            ind.color = config.safe_color
        if config.round_count > self.boss_rounds:
            destroy(config.indicators[1])

        for x in range(config.GRID_SIZE):
            for z in range(config.GRID_SIZE):
                col = config.safe_color if random.random() < 0.2 else random.choice(config.ALL_COLORS)
                block = Entity(
                    model='cube',
                    texture='white_cube',
                    shader="lit_with_shadows_shader",
                    color=col,
                    position=(
                        x * config.BLOCK_SIZE - config.GRID_SIZE * config.BLOCK_SIZE / 2,
                        0,
                        z * config.BLOCK_SIZE - config.GRID_SIZE * config.BLOCK_SIZE / 2
                    ),
                    scale=config.BLOCK_SIZE,
                    collider='box'
                )
                config.blocks.append(block)

        if config.round_count > self.boss_rounds:

            config.TIME_LIMIT = 5
            self.boss_atak()
            config.timer_text.color = color.red
            self.start_timer()
        else:
            config.TIME_LIMIT = config.TRUE_TIME_LIMIT
            self.start_timer()


    def boss_atak(self):
        bobo =Entity(model = 'sphere',collider="box", position = (
                      random.randint(-config.BLOCK_SIZE*config.GRID_SIZE/2, config.BLOCK_SIZE*config.GRID_SIZE/2), config.BLOCK_SIZE +1, -config.BLOCK_SIZE*config.GRID_SIZE/2 -3 ),
                     scale=(2,2,5),shader="lit_with_shadows_shader",color=color.cyan)
        self.list_bones.append(bobo)
        invoke(destroy,bobo, delay=20)


    def init_game(self):
        config.TIME_LIMIT = config.TRUE_TIME_LIMIT
        config.timer_text = Text(
            text=f'BOSS MODE - Time: {config.TIME_LIMIT}',
            position=(0, 0.45),
            scale=2,
            origin=(0, 0),
            color=color.white
        )
        config.round_text = Text(
            text='Round: 0',
            position=(-0.75, 0.45),
            scale=2,
            origin=(0, 0)
        )
        self.create_indicators()
        self.create_field()

    def die(self):
        if not config.alive:
            return

        config.fl_boss_apiar = False
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

        destroy(self.boss)
        self.boss = None

        for b in self.list_bones:
            destroy(b)
        self.list_bones.clear()

        if config.player:
            destroy(config.player)
            config.player = None

        death_msg = Text(
            text=f"BOSS DEFEATED YOU!\nGAME OVER\nRounds survived: {config.round_count}",
            origin=(0, 0),
            scale=3,
            color=color.red
        )

        invoke(self.return_to_menu, delay=2)
        invoke(destroy, death_msg, delay=2)

    def update(self):
        if config.game_active and config.player and config.player.y < config.DEATH_Y:
            self.die()

        if not config.fl_boss_apiar and config.round_count > self.boss_rounds:
            config.fl_boss_apiar = True
            #self.boss = Entity(model = config.boss_model,collider="mesh", position = (0, config.BLOCK_SIZE +3, -config.BLOCK_SIZE*config.GRID_SIZE/2 -7 ),scale=0.5,shader="lit_with_shadows_shader")
            self.boss = Entity(model = 'sphere', position = (0, config.BLOCK_SIZE +3, -config.BLOCK_SIZE*config.GRID_SIZE/2 -7 ),scale=(7,9,7), texture = "3d_model/qwer.png")
            self.boss.rotation = (0, -90, 0)

        for el in self.list_bones:
            try:
                el.z += 2 * time.dt
                if config.player and config.alive and config.game_active:
                    # Простая проверка расстояния (быстрее, чем intersects)
                    distance = ((el.x - config.player.x) ** 2 +
                                (el.z - config.player.z) ** 2) ** 0.5

                    if distance < 2:  # Если игрок близко к атаке
                        self.die()
                        return
            except:
                # Объект был уничтожен, удаляем из списка
                if el in self.list_bones:
                    self.list_bones.remove(el)

