#!/usr/bin/env python
import json
import time

import redis

from conf import REDIS_ADDRESS, REDIS_PORT


def send_message(redis_db, msg_data):
    json_msg = json.dumps(msg_data)
    redis_db.publish('scapi', json_msg)
    time.sleep(1)


if __name__ == '__main__':
    redis_db = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)

    send_message(redis_db, {'user': 'someone1', 'team': 'HotJava', 'action': 'drop'})
    msg_data = {
        'user': 'someone1',
        'team': 'HotJava',
        'action': 'drop'
    }
    send_message(redis_db, msg_data)
    msg_data = {
        'user': 'someone1',
        'team': 'PythonTamers',
        'action': 'use'
    }
    send_message(redis_db, msg_data)
    msg_data = {
        'user': 'someone1',
        'team': 'Disassembly',
        'action': 'use'
    }
    # send_message(redis_db, msg_data)
    # msg_data = {
    #     'user': 'someone1',
    #     'team': 'PythonTamers',
    #     'action': 'drop'
    # }
    send_message(redis_db, msg_data)

    # msg_data = {
    #     'user': 'someone2',
    #     'team': 'PythonTamers',
    #     'action': 'right'
    # }

    # send_message(redis_db, msg_data)

    # msg_data = {
    #     'user': 'student1',
    #     'team': 'SeeMoreAndMore',
    #     'action': 'up'
    # }

    # send_message(redis_db, msg_data)

    # msg_data = {
    #     'user': 'student2',
    #     'team': 'SeeSharp',
    #     'action': 'down'
    # }

    # send_message(redis_db, msg_data)
