#!/usr/bin/env python
import time
import json
import redis

from conf import REDIS_ADDRESS, REDIS_PORT, USER, TEAM_NAME, GREEN


def send_message_redis(redis_db, msg_data):
    json_msg = json.dumps(msg_data)
    redis_db.publish(f'{TEAM_NAME}/{USER}', json_msg)


BOARD_EXAMPLE = [
    ['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '@', '|'],
    ['|', '.', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', '|'],
    ['|', '.', '.', '.', '|', '.', '.', '.', '|', '.', '|', '.', '|'],
    ['|', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
    ['|', '.', '.', '.', '1', '2', '3', '4', '5', '.', '.', '.', '|'],
    ['|', '|', '.', '.', '.', '.', '|', '.', '.', '.', '.', '|', '|'],
    ['|', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
    ['|', '.', '|', '.', '.', '.', '|', '.', '.', '.', '.', '.', '|'],
    ['@', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.', '|'],
    ['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|']
]


def send_game_starting_msg(redis_db):
    event_msg = {
        'type': 'game_starting',
        'board': BOARD_EXAMPLE,
        'actions': ['right', 'left', 'up', 'down', 'use'],
        'teams': {
            TEAM_NAME: {
                'id': 1,
                'name': TEAM_NAME,
                # ...
            },
            'OtherTeam': {
                'id': 2,
                'name': 'OtherTeam',
                # ...
            }
        }
    }

    send_message_redis(redis_db, event_msg)


def send_board_change_msg(redis_db):
    event_msg = {
        'type': 'board_change',
        'change': {
            'a_coord_val': [4, 8, '.'],
            'b_coord_val': [3, 8, '5'],
        }
    }
    send_message_redis(redis_db, event_msg)


if __name__ == '__main__':
    redis_db = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)
    send_game_starting_msg(redis_db)
    # time.sleep(5)
    # send_board_change_msg(redis_db)
