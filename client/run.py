#!/usr/bin/env python
"""
Simple Redis client using a Pub/sub comunication, and JSON for the messages serialization.
"""

import json
import logging
import time

import logzero
import redis

from conf import (
    REDIS_ADDRESS,
    REDIS_PORT,
    TEAM_NAME,
    USER,
    LOGGING_LEVEL,
)


class ScapiClient():
    def __init__(self, redis_address, redis_port, scapi_team, scapi_user, logging_level):
        self.redis_connection_info = (redis_address, redis_port)
        self.redis_db = redis.Redis(host=redis_address, port=redis_port)
        self.scapi_team = scapi_team
        self.scapi_user = scapi_user
        self.user_actions = []
        self.logging_level = logging_level
        self.logger = self._setup_logging()
        self.setup_user_pubsub()

    def setup_user_pubsub(self):
        self.pubsub = self.redis_db.pubsub(ignore_subscribe_messages=True)
        user_topic = f'{self.scapi_team}/{self.scapi_user}'
        self.pubsub.subscribe(user_topic)

    def _setup_logging(self):
        log_format = (
            '%(color)s[%(levelname)1.1s %(name)s %(asctime)s:%(msecs)d '
            '%(module)s:%(funcName)s:%(lineno)d]%(end_color)s %(message)s'
        )
        formatter = logzero.LogFormatter(fmt=log_format)
        return logzero.setup_logger(
            name=self.__class__.__name__, level=logging.getLevelName(self.logging_level), formatter=formatter)

    def send_registration_msg(self):
        msg_data = {
            'team': self.scapi_team,
            'user': self.scapi_user
        }
        json_msg = json.dumps(msg_data)
        self.redis_db.publish('scapi-setup', json_msg)

    def try_register_loop(self):
        is_correct_info = input((
            f'will send registration information "{self.scapi_team}"/"{self.scapi_user}" (team/user) to '
            f'"{self.redis_connection_info}". \n'
            'If this is correct? [y]/n'
        ))
        if is_correct_info.lower() == 'n':
            self.logger.info('Client exiting. Check your credentials in the .env file before running again.')
            return False
            exit()

        self.send_registration_msg()
        self.logger.info((
            f'Waiting for list of user actions on game start...'
        ))
        for message in self.pubsub.listen():
            try:
                self.process_receive_user_action_msg(message['data'].decode('utf-8'))
                return True
            except Exception as e:
                self.logger.error(f'Error processing {message}:')
                self.logger.exception(e)
                self.logger.error(
                    f'Will exit client. Contact ScaPi ADMIN of the issue, with the exception stack trace information'
                )
                return False

    def process_receive_user_action_msg(self, json_msg):
        msg_data = json.loads(json_msg)
        self.user_actions = sorted(msg_data)

    def send_action_msg(self, action):
        msg_data = {
            'team': self.scapi_team,
            'user': self.scapi_user,
            'action': action
        }
        json_msg = json.dumps(msg_data)
        self.redis_db.publish('scapi', json_msg)

    def process_game_over_msg(self, msg_json):
        msg_data = json.loads(msg_json)
        return msg_data.get('game-over', False)

    def start_round(self):
        input_text = 'Input the number of the desired action from the list bellow, and then press enter: \n'
        for i, action in enumerate(self.user_actions, 1):
            input_text += f'[{i}] - {action}\n'
        while True:
            try:
                action_input = input(input_text)
                action_index = int(action_input) - 1
                action = self.user_actions[action_index]
                self.send_action_msg(action)
                print('\n' * 100)
                self.logger.info(f'Action Sent: {action}')
            except Exception:
                print('\n' * 100)
                self.logger.warning(f'Invalid action input, ignoring last input...')
            finally:
                message = self.pubsub.get_message()
                if message and self.process_game_over_msg(message['data'].decode('utf-8')):
                    self.logger.info('Game-Over')
                    return
                # adding this here just to avoid users spamming too much
                # not really necessary though...
                time.sleep(0.25)

    def run(self):
        if self.try_register_loop():
            self.start_round()
        exit()


if __name__ == '__main__':

    scapi_server = ScapiClient(
        redis_address=REDIS_ADDRESS, redis_port=REDIS_PORT,
        scapi_team=TEAM_NAME,
        scapi_user=USER,
        logging_level=LOGGING_LEVEL
    )
    try:
        scapi_server.run()
    except KeyboardInterrupt:
        pass
