import os

from decouple import config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

REDIS_ADDRESS = config('REDIS_ADDRESS', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379')

LOGGING_LEVEL = config('LOGGING_LEVEL', default='DEBUG')
TEAM_NAME = config('TEAM_NAME')
USER = config('USER')
