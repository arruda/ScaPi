import os

from decouple import config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BOARDS_DIR = os.path.join(PROJECT_ROOT, 'boards')

REDIS_ADDRESS = config('REDIS_ADDRESS', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379')

DATABASE_URL = config('DATABASE_URL', default='sqlite:///scapi.db')

LOGGING_LEVEL = config('LOGGING_LEVEL', default='DEBUG')
TEAM_NAMES = config('TEAM_NAMES', cast=lambda s: s.split('/'))
BOARD_ID = config('BOARD_ID', default=1)
