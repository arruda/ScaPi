#!/usr/bin/env python
import json
import redis

from conf import REDIS_ADDRESS, REDIS_PORT


def send_message(redis_db, msg_data):
    json_msg = json.dumps(msg_data)
    redis_db.publish('scapi', json_msg)


if __name__ == '__main__':
    redis_db = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)
    msg_data = {
        'user': 'someone1',
        'team': 'PythonTamers',
        'action': 'left'
    }
    send_message(redis_db, msg_data)

    msg_data = {
        'user': 'someone2',
        'team': 'PythonTamers',
        'action': 'right'
    }

    send_message(redis_db, msg_data)

    msg_data = {
        'user': 'student1',
        'team': 'SeeMoreAndMore',
        'action': 'up'
    }

    send_message(redis_db, msg_data)

    msg_data = {
        'user': 'student2',
        'team': 'Disassembly',
        'action': 'down'
    }

    send_message(redis_db, msg_data)
