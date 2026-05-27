from ursina import *
from infiniti_mode import InfinitiMode
from boss_mode import BossMode
from menu import *
import config

app = Ursina()


def on_mode_selected(mode):
    global current_mode_type

    if mode == "infiniti":
        config.game = InfinitiMode()
        current_mode_type = "infiniti"
        config.menu.ui_parent.enabled = False
        open_settings(config.menu)

    elif mode == "boss":
        config.game = BossMode()
        current_mode_type = "boss"
        config.menu.hide()
        config.game.start_game()

sun = DirectionalLight(shadows=True)
AmbientLight(color=color.rgb(80, 80, 80))
sun.look_at(Vec3(1, -1, 1))

window.fullscreen = True

def update():
    if held_keys["escape"]:
        application.quit()

    if config.game:
        config.game.update()

    if held_keys["p"]:
        bobo = Entity(model='sphere', collider="mesh", position=(0,3,0), scale=(1,3,1))

# Создаем меню и сохраняем в глобальную переменную
config.menu = Menu(on_mode_selected)

app.run()
#  523