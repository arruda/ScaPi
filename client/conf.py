from ast import Pass
import os

from decouple import config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_FOLDER = os.path.join(PROJECT_ROOT, 'assets')

REDIS_ADDRESS = config('REDIS_ADDRESS', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379')

LOGGING_LEVEL = config('LOGGING_LEVEL', default='DEBUG')
TEAM_NAME = config('TEAM_NAME')
USER = config('USER')

KEY_UP = config('KEY_UP', 'Up:111')
KEY_DOWN = config('KEY_DOWN', 'Down:116')
KEY_LEFT = config('KEY_LEFT', 'Left:113')
KEY_RIGHT = config('KEY_RIGHT', 'Right:114')
KEY_USE = config('KEY_USE', 'e')
KEY_DROP = config('KEY_DROP', 'q')

KEY_ACTIONS_MAP = {
    KEY_UP: 'up',
    KEY_DOWN: 'down',
    KEY_LEFT: 'left',
    KEY_RIGHT: 'right',
    KEY_USE: 'use',
    KEY_DROP: 'drop',
}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

TITLE = "ScaPi Client"

WIDTH = 1024
HEIGHT = 768
DEFAULT_WINDOW_SIZE = (WIDTH, HEIGHT)

TILE_SIZE = 32

SPRITE_DICT = {
    '|': os.path.join(IMG_FOLDER, 'img_wall.png'),
    '.': os.path.join(IMG_FOLDER, 'img_path.png'),
    '@': os.path.join(IMG_FOLDER, 'img_unlocked_door.png'),
    '#': os.path.join(IMG_FOLDER, 'img_locked_door.png'),
    'K': os.path.join(IMG_FOLDER, 'img_key.png'),
    '1': os.path.join(IMG_FOLDER, 'img_01.png'),
    '2': os.path.join(IMG_FOLDER, 'img_02.png'),
    '3': os.path.join(IMG_FOLDER, 'img_03.png'),
    '4': os.path.join(IMG_FOLDER, 'img_04.png'),
    '5': os.path.join(IMG_FOLDER, 'img_05.png'),
}

FONT_HEADER = ("Arial", 30)
