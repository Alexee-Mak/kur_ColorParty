# Color Party

A first-person 3D survival game built with the [Ursina](https://www.ursinaengine.org/) engine.

You stand on a floor made of colored blocks. The bars around the arena show the safe color for the round. When the timer runs out, every block of any other color disappears. Get onto a safe block before that happens, or you fall into the void and the game ends. Survive as many rounds as you can.

## Requirements

- Python 3.10–3.12
- Ursina

```
pip install ursina
```

> [!WARNING]
> Ursina depends on Panda3D, which only publishes builds for certain Python versions. On a newer Python, such as 3.15, `pip install ursina` fails with `ResolutionImpossible` and the message `no matching distributions available for your environment: panda3d`.
>
> To fix this, create a virtual environment with Python 3.12 and install Ursina into it:
>
> ```powershell
> py -3.12 -m venv .venv
> .venv\Scripts\activate
> pip install ursina
> ```
>
> If you use [uv](https://docs.astral.sh/uv/), run this instead:
>
> ```powershell
> uv venv --python 3.12 .venv
> .venv\Scripts\activate
> uv pip install ursina
> ```

## Running

```
python main.py
```

The game opens in fullscreen.

## Controls

| Key | Action |
| --- | --- |
| `W` `A` `S` `D` | Move |
| Mouse | Look around |
| `Space` | Jump |
| `Esc` | Quit the game |

## Game modes

### Infinity mode

Endless rounds. Before the game starts, you can change three settings:

| Setting | Allowed values | Default |
| --- | --- | --- |
| Grid size | 1–30 blocks per side | 15 |
| Block size | any positive whole number | 3 |
| Time limit | 1–30 seconds | 10 |

If you enter a value outside the allowed range, the game uses the default.

### Boss mode

A harder mode with a 20×20 grid of smaller blocks and a 6-second timer. After the first round, a boss appears at the edge of the arena:

- the timer drops to 5 seconds;
- one of the color indicator bars disappears;
- each round, the boss throws a projectile across the arena. If it touches you, you lose.

## Project structure

| File | Purpose |
| --- | --- |
| `main.py` | Entry point: creates the window, lighting and main menu |
| `menu.py` | Main menu, mode selection and settings screens |
| `config.py` | Default settings and shared game state |
| `game_mode.py` | Base game logic: player, timer, rounds, death |
| `infiniti_mode.py` | Infinity mode |
| `boss_mode.py` | Boss mode |
| `3d_model/` | Models and textures |
| `models_compressed/` | Compressed model files that Ursina generates automatically |
