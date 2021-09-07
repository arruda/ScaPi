#!/usr/bin/env python
"""
Simple Redis server using a Pub/sub comunication, and JSON for the messages serialization.
"""
import json
import logging
import pprint

import logzero
import redis

from conf import (
    REDIS_ADDRESS,
    REDIS_PORT,
    TEAM_NAMES,
    BOARD_ID,
    LOGGING_LEVEL
)


class ScapiServer():
    def __init__(self, redis_address, redis_port, logging_level):
        self.redis_db = redis.Redis(host=redis_address, port=redis_port)
        self.logging_level = logging_level
        self.logger = self._setup_logging()

        self.setup_game(TEAM_NAMES, board_id=BOARD_ID)

    def _setup_logging(self):
        log_format = (
            '%(color)s[%(levelname)1.1s %(name)s %(asctime)s:%(msecs)d '
            '%(module)s:%(funcName)s:%(lineno)d]%(end_color)s %(message)s'
        )
        formatter = logzero.LogFormatter(fmt=log_format)
        return logzero.setup_logger(
            name=self.__class__.__name__, level=logging.getLevelName(self.logging_level), formatter=formatter)

    def setup_teams(self, team_names):
        self.teams = {}
        for team_id, name in enumerate(team_names, 1):
            self.teams[name] = {
                'id': team_id,
                'score': 0,
                'coordinates': [0, 0],
                'last_action': None,
                'left_maze': False,
                'exit_time': None,
            }

    def setup_game(self, team_names, board_id):
        self.setup_teams(team_names)
        self.board = [
            ['#', '#', '#', '#', '#', '#', '#'],
            ['#', '.', '.', '.', '.', '5', '#'],
            ['#', '.', '.', '.', '4', '.', '#'],
            ['#', '.', '.', '3', '.', '.', '#'],
            ['#', '.', '2', '.', '.', '.', '#'],
            ['#', '1', '.', '.', '.', '.', '#'],
            ['#', '#', '#', '-', '#', '#', '#'],
        ]
        self.game_state = {
            'last_teams_action': [None for i in range(len(self.teams))],
            'team_scores': [0 for i in range(len(self.teams))]
        }

    def run(self):
        pubsub = self.redis_db.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe('scapi')
        for message in pubsub.listen():
            try:
                self.process_msg(message['data'].decode('utf-8'))
            except Exception as e:
                self.logger.error(f'Error processing {message}:')
                self.logger.exception(e)
            finally:
                self.show_board()
                self.show_state()

    def process_msg(self, json_msg):
        msg_data = json.loads(json_msg)

        self.logger.debug(msg_data)

    def show_board(self):
        for row in self.board:
            print(''.join(row))

    def show_last_actions(self):
        last_teams_action = self.game_state['last_teams_action']
        print(f'Last Team Action:')
        for team_index, team_action in enumerate(last_teams_action):
            team = self.teams[team_index]
            user = team_action['user']
            action = team_action['action']
            print(f'\t {team}/{user}: {action}')

    def show_state(self):
        # teams_left = self.game_state['teams_left']
        # print(f'Teams Scores: {teams_left}')
        self.show_last_actions()


if __name__ == '__main__':
    scapi_server = ScapiServer(
        redis_address=REDIS_ADDRESS, redis_port=REDIS_PORT,
        logging_level=LOGGING_LEVEL
    )
    try:
        scapi_server.run()
    except KeyboardInterrupt:
        pass
