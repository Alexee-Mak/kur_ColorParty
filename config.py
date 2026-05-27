from ursina import color, load_model


#boss_model = load_model("3d_model/Sans.obj")
#atak_moel = load_model("3d_model/qwe.obj")

DEFAULT_GRID_SIZE = 15
DEFAULT_BLOCK_SIZE = 3
DEFAULT_TIME_LIMIT = 10

GRID_SIZE = DEFAULT_GRID_SIZE
BLOCK_SIZE = DEFAULT_BLOCK_SIZE
TRUE_TIME_LIMIT = DEFAULT_TIME_LIMIT
TIME_LIMIT = TRUE_TIME_LIMIT
DEATH_Y = -10

ALL_COLORS = [color.red, color.blue, color.yellow,  color.magenta, color.cyan, color.green]

blocks = []
indicators = []
timer_text = None
safe_color = color.green
round_count = 0
round_text = None
alive = True
player = None
game_active = False
settings_window = None
menu = None
game = None
fl_boss_apiar = False