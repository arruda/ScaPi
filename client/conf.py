import os

from decouple import config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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

