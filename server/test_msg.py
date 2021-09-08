#!/usr/bin/env python
import json
import time

import redis

from conf import REDIS_ADDRESS, REDIS_PORT


def send_message_reg(redis_db, msg_data):
    json_msg = json.dumps(msg_data)
    redis_db.publish('scapi-register', json_msg)
    time.sleep(1)


def send_message(redis_db, msg_data):
    json_msg = json.dumps(msg_data)
    redis_db.publish('scapi', json_msg)
    time.sleep(1)


if __name__ == '__main__':
    redis_db = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT)

    pubsub = redis_db.pubsub(ignore_subscribe_messages=True)
    send_message_reg(redis_db, {'user': 'someone1', 'team': 'HotJava'})
    send_message_reg(redis_db, {'user': 'someone2', 'team': 'HotJava'})
    send_message_reg(redis_db, {'user': 'someone3', 'team': 'HotJava'})
    send_message_reg(redis_db, {'user': 'someone4', 'team': 'HotJava'})
    send_message_reg(redis_db, {'user': 'someone5', 'team': 'HotJava'})
    send_message_reg(redis_db, {'user': 'someone1', 'team': 'SeeSharp'})
    send_message_reg(redis_db, {'user': 'someone2', 'team': 'SeeSharp'})

    pubsub.subscribe('HotJava/someone1')
    pubsub.subscribe('HotJava/someone2')
    pubsub.subscribe('HotJava/someone3')
    pubsub.subscribe('HotJava/someone4')
    pubsub.subscribe('HotJava/someone5')
    time.sleep(6)
    for i in range(100):
        msg = pubsub.get_message()
        if msg:
            print(msg)
        time.sleep(0.1)
    # print(pubsub.get_message())
    # print(pubsub.get_message())
    # print(pubsub.get_message())
    # print(pubsub.get_message())
    # for msg in pubsub.get_message():

    import pdb; pdb.set_trace()
    send_message(redis_db, {'user': 'someone1', 'team': 'HotJava', 'action': 'down'})
    send_message(redis_db, {'user': 'someone2', 'team': 'HotJava', 'action': 'down'})
    send_message(redis_db, {'user': 'someone3', 'team': 'HotJava', 'action': 'down'})
    send_message(redis_db, {'user': 'someone4', 'team': 'HotJava', 'action': 'down'})
    send_message(redis_db, {'user': 'someone5', 'team': 'HotJava', 'action': 'down'})
    # msg_data = {
    #     'user': 'someone1',
    #     'team': 'HotJava',
    #     'action': 'drop'
    # }
    # send_message(redis_db, msg_data)
    # msg_data = {
    #     'user': 'someone1',
    #     'team': 'PythonTamers',
    #     'action': 'use'
    # }
    # send_message(redis_db, msg_data)
    # msg_data = {
    #     'user': 'someone1',
    #     'team': 'Disassembly',
    #     'action': 'use'
    # }
    # # send_message(redis_db, msg_data)
    # # msg_data = {
    # #     'user': 'someone1',
    # #     'team': 'PythonTamers',
    # #     'action': 'drop'
    # # }
    # send_message(redis_db, msg_data)

    # # msg_data = {
    # #     'user': 'someone2',
    # #     'team': 'PythonTamers',
    # #     'action': 'right'
    # # }

    # # send_message(redis_db, msg_data)

    # # msg_data = {
    # #     'user': 'student1',
    # #     'team': 'SeeMoreAndMore',
    # #     'action': 'up'
    # # }

    # # send_message(redis_db, msg_data)

    # # msg_data = {
    # #     'user': 'student2',
    # #     'team': 'SeeSharp',
    # #     'action': 'down'
    # # }

    # # send_message(redis_db, msg_data)
