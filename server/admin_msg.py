#!/usr/bin/env python
import json
import time

import redis

from conf import REDIS_ADDRESS, REDIS_PORT, ADMIN_PASS, GAMEOVER_TIME


def send_message_reg(redis_db, msg_data):
    json_msg = json.dumps(msg_data)
    redis_db.publish('scapi-admin', json_msg)


if __name__ == '__main__':
    redis_db = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)

    is_ready = input('Press enter when all teams are ready...')
    send_message_reg(redis_db, {'admin': ADMIN_PASS, 'ready': True})

    is_game_over = False
    seconds_passed = 0
    while not is_game_over:
        time.sleep(1)
        seconds_passed += 1
        time_left = GAMEOVER_TIME - seconds_passed
        print('\n' * 100)
        print(f'Time Left: {time_left}')
        if time_left <= 0:
            is_game_over = True

    send_message_reg(redis_db, {'admin': ADMIN_PASS, 'gameover': True})
    print('GAME OVER!')
