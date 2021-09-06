#!/usr/bin/env python
import json
import redis

from conf import REDIS_ADDRESS, REDIS_PORT


def send_messages(redis_db, msg_data):
    json_msg = json.dumps(msg_data)
    redis_db.publish('scapi', json_msg)


if __name__ == '__main__':
    redis_db = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)
    msg_data = {
        'user': 'someone',
        'team': 'TheTop25',
        'action': 'left'
    }
    send_messages(redis_db, msg_data)
