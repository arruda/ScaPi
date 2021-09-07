#!/usr/bin/env python
"""
Simple Redis server using a Pub/sub comunication, and JSON for the messages serialization.
"""
import datetime
from functools import partial
import json
import logging

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
        self.process_action_mapping = {
            'right': partial(self.process_action_right, value=1),
            'left': partial(self.process_action_right, value=-1),
            'up': partial(self.process_action_down, value=-1),
            'down': partial(self.process_action_down, value=1),
            # 'drop': self.process_action_drop,
            # 'open': self.process_action_open,
        }

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
            spawn_coordinates = [team_id, team_id]
            self.teams[name] = {
                'id': team_id,
                'score': 0,
                'coordinates': spawn_coordinates,
                'last_action': None,
                'left_maze': False,
                'exit_time': None,
            }
            self.update_team_on_board(team_id, spawn_coordinates, spawn_coordinates)

    def setup_game(self, team_names, board_id):
        self.board = [
            ['#', '#', '#', '#', '#', '#', '#'],
            ['#', '.', '.', '.', '.', '.', '#'],
            ['#', '.', '.', '.', '.', '.', '#'],
            ['#', '.', '.', '.', '.', '.', '#'],
            ['#', '.', '.', '.', '.', '.', '#'],
            ['#', '.', '.', '.', '.', '.', '#'],
            ['#', '#', '#', '-', '#', '#', '#'],
        ]
        self.setup_teams(team_names)

    def update_team_on_board(self, team_id, old_coord, new_coord):
        self.board[old_coord[0]][old_coord[1]] = '.'
        self.board[new_coord[0]][new_coord[1]] = str(team_id)

    def show_updated_screen(self):
        self.show_board()
        self.show_last_actions()
        self.show_scores()

    def run(self):
        self.show_updated_screen()
        pubsub = self.redis_db.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe('scapi')
        for message in pubsub.listen():
            try:
                self.process_msg(message['data'].decode('utf-8'))
            except Exception as e:
                self.logger.error(f'Error processing {message}:')
                self.logger.exception(e)
            finally:
                self.show_updated_screen()

    def is_valid_board_move_coordinate(self, coordinates):
        try:
            return self.board[coordinates[0]][coordinates[1]] == '.'
        except IndexError:
            return False

    def move_team_if_valid(self, team, old_coordinates, new_coordinates):
        if self.is_valid_board_move_coordinate(new_coordinates):
            team_id = self.teams[team]['id']
            self.teams[team]['coordinates'] = new_coordinates
            self.update_team_on_board(team_id, old_coordinates, new_coordinates)

    def process_action_right(self, team, value):
        old_coordinates = self.teams[team]['coordinates']
        new_coordinates = [old_coordinates[0], old_coordinates[1] + value]
        self.move_team_if_valid(team, old_coordinates, new_coordinates)

    def process_action_down(self, team, value):
        old_coordinates = self.teams[team]['coordinates']
        new_coordinates = [old_coordinates[0] + value, old_coordinates[1]]
        self.move_team_if_valid(team, old_coordinates, new_coordinates)

    def process_action(self, team, user, action):
        action_mapping = self.process_action_mapping.get(action)
        if action_mapping is None:
            return False
        action_mapping(team)

    def process_msg(self, json_msg):
        msg_data = json.loads(json_msg)
        team = msg_data['team']
        user = msg_data['user']
        action = msg_data['action']
        self.process_action(team, user, action)
        self.teams[team]['last_action'] = msg_data

        self.logger.debug(msg_data)

    def show_board(self):
        print('\n' * 100)
        for row in self.board:
            print(''.join(row))

    def show_last_actions(self):
        print(f'Last Team Action Received:')
        for team, team_data in self.teams.items():
            last_action = team_data['last_action']
            if last_action:
                user = last_action['user']
                action = last_action['action']
                print(f'\t {team}/{user}: {action}')
            else:
                print(f'\t {team}/: None')

    def show_scores(self):
        print(f'Team Scores:')
        for team, team_data in self.teams.items():
            team_id = team_data['id']
            left_maze = team_data['left_maze']
            score = team_data['score']
            if left_maze:
                exit_time = team_data['exit_time']
                print(f'\t ({team_id}){team}\t({exit_time}):\t{score}')
            else:
                print(f'\t ({team_id}){team}\t (On Going):\t{score}')


if __name__ == '__main__':
    scapi_server = ScapiServer(
        redis_address=REDIS_ADDRESS, redis_port=REDIS_PORT,
        logging_level=LOGGING_LEVEL
    )
    try:
        scapi_server.run()
    except KeyboardInterrupt:
        pass
