#!/usr/bin/env python
import json
import time

import redis

from conf import REDIS_ADDRESS, REDIS_PORT, USER, TEAM_NAME, GREEN


def send_message_reg(redis_db, msg_data):
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
        'teams':{
            1: {
                'color': GREEN,
                'name': TEAM_NAME
            },
            2:{
                'color': GREEN,
                'name': 'OtherTeam'
            }
        }
    }

    send_message_reg(redis_db, event_msg)



if __name__ == '__main__':
    redis_db = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)
    send_game_starting_msg(redis_db)