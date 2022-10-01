import os

from decouple import config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_FOLDER = os.path.join(PROJECT_ROOT, 'assets')

REDIS_ADDRESS = config('REDIS_ADDRESS', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379')

LOGGING_LEVEL = config('LOGGING_LEVEL', default='DEBUG')
TEAM_NAME = config('TEAM_NAME')
USER = config('USER')

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
    '|': 'img_wall.png',
    '.': 'img_path.png',
    '@': 'img_unlocked_door.png',
    '#': 'img_locked_door.png',
    'K': 'img_key.png',
    '1': 'img_01.png',
    '2': 'img_02.png',
    '3': 'img_03.png',
    '4': 'img_01.png',
    '5': 'img_01.png'
}

FONT_HEADER = ("Arial", 30)
