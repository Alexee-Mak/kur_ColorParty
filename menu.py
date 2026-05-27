from ursina import *
import config


class ModeSelect:

    def __init__(self, parent_menu, on_mode_selected):
        self.parent_menu = parent_menu
        self.on_mode_selected = on_mode_selected
        self.ui_parent = Entity(parent=camera.ui, ignore_paused=True)

        self.bg = Entity(parent=self.ui_parent, model='quad', scale=(0.8, 0.7),
                         color=color.rgba(0, 0, 0, 0.9), position=(0, 0))

        self.title = Text("SELECT GAME MODE", parent=self.ui_parent, position=(0, 0.3),
                          scale=2, origin=(0, 0), color=color.white)

        self.infiniti_btn = Button(
            text="INFINITI MODE\nEndless challenge",
            color=color.azure,
            scale=(0.5, 0.15),
            position=(0, 0.1),
            parent=self.ui_parent
        )
        self.infiniti_btn.on_click = lambda: self.select_mode("infiniti")

        self.boss_btn = Button(
            text="BOSS MODE\nHardcore + Boss fights",
            color=color.orange,
            scale=(0.5, 0.15),
            position=(0, -0.1),
            parent=self.ui_parent
        )
        self.boss_btn.on_click = lambda: self.select_mode("boss")

        self.back_btn = Button(
            text="Back",
            color=color.red,
            scale=(0.3, 0.08),
            position=(0, -0.3),
            parent=self.ui_parent
        )
        self.back_btn.on_click = self.back_to_menu

    def select_mode(self, mode):
        self.close()
        self.on_mode_selected(mode)

    def back_to_menu(self):
        self.close()
        self.parent_menu.show()

    def close(self):
        destroy(self.ui_parent)


class SettingsPlay:
    def __init__(self, parent_menu, grid_size, block_size, time_limit, start_game_callback):
        self.parent_menu = parent_menu
        self.start_game_callback = start_game_callback
        self.ui_parent = Entity(parent=camera.ui, ignore_paused=True)

        self.bg = Entity(parent=self.ui_parent, model='quad', scale=(0.7, 0.65),
                         color=color.rgba(0, 0, 0, 0.85), position=(0, 0))

        self.title = Text("GAME SETTINGS", parent=self.ui_parent, position=(0, 0.28),
                          scale=2, origin=(0, 0), color=color.white)

        self.grid_label = Text("Grid Size (1-30):", parent=self.ui_parent, position=(-0.23, 0.12),
                               scale=1, origin=(0, 0), color=color.white)
        self.grid_input = InputField(parent=self.ui_parent, default_value=str(grid_size),
                                     position=(0.15, 0.12), scale_x=0.2, scale_y=0.05, color=color.gray)

        self.block_label = Text("Block Size (>0):", parent=self.ui_parent, position=(-0.23, 0.02),
                                scale=1, origin=(0, 0), color=color.white)
        self.block_input = InputField(parent=self.ui_parent, default_value=str(block_size),
                                      position=(0.15, 0.02), scale_x=0.2, scale_y=0.05, color=color.gray)

        self.time_label = Text("Time Limit (1-30 sec):", parent=self.ui_parent, position=(-0.2, -0.08),
                               scale=1, origin=(0, 0), color=color.white)
        self.time_input = InputField(parent=self.ui_parent, default_value=str(time_limit),
                                     position=(0.15, -0.08), scale_x=0.2, scale_y=0.05, color=color.gray)

        self.start_btn = Button(text="Start Game", parent=self.ui_parent, position=(0.15, -0.25),
                                scale=(0.25, 0.08), color=color.green)
        self.start_btn.on_click = self.start_game

        self.back_btn = Button(text="Back", parent=self.ui_parent, position=(-0.15, -0.25),
                               scale=(0.25, 0.08), color=color.red)
        self.back_btn.on_click = self.back_to_menu

    def start_game(self):
        try:
            new_grid = int(self.grid_input.text)
            new_block = int(self.block_input.text)
            new_time = int(self.time_input.text)

            if not (1 <= new_grid <= 30):
                print("Grid size must be 1-30, using default")
                new_grid = None
            if not (new_block > 0):
                print("Block size must be > 0, using default")
                new_block = None
            if not (1 <= new_time <= 30):
                print("Time limit must be 1-30, using default")
                new_time = None
        except:
            print("Invalid input, using default values")
            new_grid = None
            new_block = None
            new_time = None

        self.close()
        self.parent_menu.hide()
        self.start_game_callback(new_grid, new_block, new_time)

    def back_to_menu(self):
        self.close()
        self.parent_menu.show()

    def close(self):
        destroy(self.ui_parent)


class Menu:
    def __init__(self, on_mode_selected_callback):
        self.on_mode_selected_callback = on_mode_selected_callback
        self.ui_parent = Entity(parent=camera.ui, ignore_paused=True)
        self.title = Text("COLOR PARTY", parent=self.ui_parent, scale=3, origin=(0, 0),
                          position=(0, 0.4), color=color.white)

        self.play_btn = Button(text='Play', color=color.azure, scale=(0.3, 0.1),
                               position=(0, 0), parent=self.ui_parent)
        self.play_btn.on_click = self.open_mode_select

        # Кнопка Exit
        self.exit_btn = Button(text='Exit', color=color.red, scale=(0.3, 0.1),
                               position=(0, -0.15), parent=self.ui_parent)
        self.exit_btn.on_click = application.quit

    def open_mode_select(self):
        self.ui_parent.enabled = False
        self.mode_select = ModeSelect(self, self.on_mode_selected_callback)

    def hide(self):
        self.ui_parent.enabled = False

    def show(self):
        self.ui_parent.enabled = True


def start_game_with_settings(new_grid=None, new_block=None, new_time=None):
    if config.game:
        config.game.start_game(new_grid, new_block, new_time)
    if config.settings_window:
        config.settings_window.close()
        config.settings_window = None


def open_settings(parent_menu):
    if config.settings_window is None and config.game:
        config.settings_window = SettingsPlay(
            parent_menu,
            config.GRID_SIZE,
            config.BLOCK_SIZE,
            config.TRUE_TIME_LIMIT,
            start_game_with_settings
        )