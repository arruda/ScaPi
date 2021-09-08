#!/usr/bin/env python
"""
Simple Redis server using a Pub/sub comunication, and JSON for the messages serialization.
"""
import datetime
from functools import partial
import json
import logging
import os
import random
import time

import logzero
import redis

from conf import (
    REDIS_ADDRESS,
    REDIS_PORT,
    TEAM_NAMES,
    BOARD_ID,
    BOARDS_DIR,
    LOGGING_LEVEL,
    ADMIN_PASS
)


class ScapiServer():
    KEY = 'K'
    PORTAL = '@'
    LOCKED_DOOR = '#'
    SPAWN_POINT = '!'

    def __init__(self, redis_address, redis_port, admin_pass, logging_level):
        self.redis_db = redis.Redis(host=redis_address, port=redis_port)
        self.logging_level = logging_level
        self.logger = self._setup_logging()
        self.admin_pass = admin_pass

        self.process_action_mapping = {
            'right': partial(self.process_action_right, value=1),
            'left': partial(self.process_action_right, value=-1),
            'up': partial(self.process_action_down, value=-1),
            'down': partial(self.process_action_down, value=1),
            'use': self.process_action_use,
            'drop': self.process_action_drop,
        }

        self.setup_game(TEAM_NAMES, board_id=BOARD_ID)

    def _setup_logging(self):
        log_format = (
            '%(color)s[%(levelname)1.1s %(name)s %(asctime)s:%(msecs)d '
            '%(module)s:%(funcName)s:%(lineno)d]%(end_color)s %(message)s'
        )
        formatter = logzero.LogFormatter(fmt=log_format)
        return logzero.setup_logger(
            name=self.__class__.__name__, level=logging.getLevelName(self.logging_level), formatter=formatter)

    def load_board(self, board_id):
        file_path = os.path.join(BOARDS_DIR, f'board_{board_id}')
        board = []
        with open(file_path, 'r') as f:
            for line in f.readlines():
                board.append(list(line.replace('\n', '')))
        return board

    def get_spawn_points(self):
        points = []
        for row, row_el in enumerate(self.board):
            for col, col_el in enumerate(row_el):
                if col_el == self.SPAWN_POINT:
                    points.append([row, col])

        return points

    def setup_teams(self, team_names, spawn_points):
        self.teams = {}
        self.teams_on_maze = len(team_names)
        team_names = random.sample(team_names, len(team_names))
        self.teams_left_by_magic_dor = 0
        for team_id, name in enumerate(team_names, 1):
            spawn_coordinates = spawn_points[team_id - 1]
            self.teams[name] = {
                'id': team_id,
                'score': 0,
                'coordinates': spawn_coordinates,
                'last_action': None,
                'left_maze': False,
                'exit_time': None,
                'users': {},
                'keys': 0
            }
            self.update_team_on_board(team_id, spawn_coordinates, spawn_coordinates)

    def show_team_users(self):
        print('\n' * 100)
        print('Teams:')
        for team, team_data in self.teams.items():
            print(f'\t {team}')
            for user in team_data['users'].keys():
                print(f'\t\t {user}')

    def process_registration_msg(self, json_msg):
        msg_data = json.loads(json_msg)
        team = msg_data['team']
        user = msg_data['user']
        self.teams[team]['users'][user] = []

    def board_has_keys(self):
        for row, row_el in enumerate(self.board):
            for col, col_el in enumerate(row_el):
                if col_el == self.KEY:
                    return True
        return False

    def randomize_user_actions(self):
        available_actions = list(self.process_action_mapping.keys())
        if not self.has_keys:
            available_actions.remove('drop')
        for team, team_data in self.teams.items():
            team_users = list(team_data['users'].keys())
            team_users = random.sample(team_users, len(team_users))
            num_users = len(team_users)
            if num_users == 0:
                continue
            for i_action, action in enumerate(available_actions):
                user_index = i_action % num_users
                user = team_users[user_index]
                team_data['users'][user].append(action)

    def notify_team_users_actions(self):
        for team, team_data in self.teams.items():
            for user, actions in team_data['users'].items():
                user_topic = f'{team}/{user}'
                json_msg = json.dumps(actions)
                self.redis_db.publish(user_topic, json_msg)

    def get_admin_msg_data_if_secure(self, json_msg):
        msg_data = json.loads(json_msg)
        msg_admin_pass = msg_data['admin']
        if msg_admin_pass != ADMIN_PASS:
            return False
        return msg_data

    def process_admin_msg_game_over(self, json_msg):
        msg_data = self.get_admin_msg_data_if_secure(json_msg)
        return msg_data and msg_data.get('gameover', False)

    def process_admin_msg_game_ready(self, json_msg):
        msg_data = self.get_admin_msg_data_if_secure(json_msg)
        return msg_data and msg_data.get('ready', False)

    def setup_game(self, team_names, board_id):
        self.board = self.load_board(board_id)
        self.has_keys = self.board_has_keys()
        spawn_points = self.get_spawn_points()
        self.setup_teams(team_names, spawn_points)
        pubsub = self.redis_db.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe('scapi-setup')
        pubsub.subscribe('scapi-admin')
        self.show_team_users()
        for message in pubsub.listen():
            try:
                if message['channel'].decode('utf-8') == 'scapi-admin':
                    setup_ready = self.process_admin_msg_game_ready(message['data'].decode('utf-8'))
                    if setup_ready:
                        break
                else:
                    self.process_registration_msg(message['data'].decode('utf-8'))
            except Exception as e:
                self.logger.warning(f'Error processing {message}:')
                self.logger.exception(e)
            finally:
                self.show_team_users()
        self.randomize_user_actions()
        self.notify_team_users_actions()
        pubsub.unsubscribe('scapi-setup')
        pubsub.unsubscribe('scapi-admin')

    def update_team_on_board(self, team_id, old_coord, new_coord):
        self.board[old_coord[0]][old_coord[1]] = '.'
        self.board[new_coord[0]][new_coord[1]] = str(team_id)

    def get_open_option_if_valid_use_coordinate(self, coordinates):
        try:
            use_option = self.board[coordinates[0]][coordinates[1]]
            if use_option in [self.PORTAL, self.LOCKED_DOOR, self.KEY]:
                return use_option
        except IndexError:
            pass
        return False

    def is_valid_board_move_coordinate(self, coordinates):
        try:
            return self.board[coordinates[0]][coordinates[1]] in ['.']
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

    def process_action_drop(self, team):
        if self.teams[team]['keys'] == 0:
            return False

        old_coordinates = self.teams[team]['coordinates']

        drop_choices = {
            'left': [old_coordinates[0], old_coordinates[1] - 1],
            'right': [old_coordinates[0], old_coordinates[1] + 1],
            'up': [old_coordinates[0] - 1, old_coordinates[1]],
            'down': [old_coordinates[0] + 1, old_coordinates[1]],
        }
        choices_rand_sorted = random.sample(drop_choices.keys(), len(drop_choices.keys()))
        for choice in choices_rand_sorted:
            drop_coordinates = drop_choices[choice]
            if self.is_valid_board_move_coordinate(drop_coordinates):
                self.board[drop_coordinates[0]][drop_coordinates[1]] = self.KEY
                self.teams[team]['keys'] -= 1
                break

    def use_on_key(self, team, coordinates):
        self.teams[team]['keys'] += 1
        self.board[coordinates[0]][coordinates[1]] = '.'

    def set_team_score(self, team, is_portal=False):
        max_scoring_teams = 2
        score = (max_scoring_teams - self.teams_left_by_magic_dor) * 100
        if is_portal:
            if not self.has_keys:
                number_of_teams_left = len([team for team, data in self.teams if data['left_maze']])
                score = 10 + (number_of_teams_left * 10)
            else:
                score = 30
        else:
            self.teams_left_by_magic_dor += 1
        self.teams[team]['score'] = score

    def exit_maze(self, team, use_option):
        exit_maze = False
        if use_option == self.PORTAL:
            exit_maze = True
            self.set_team_score(team, is_portal=True)
        else:
            if self.teams[team]['keys'] > 1:
                exit_maze = True
                self.set_team_score(team, is_portal=False)

        if exit_maze:
            self.teams[team]['exit_time'] = datetime.datetime.now()
            self.teams[team]['left_maze'] = True
            coordinates = self.teams[team]['coordinates']
            self.board[coordinates[0]][coordinates[1]] = '.'

    def process_action_use(self, team):
        old_coordinates = self.teams[team]['coordinates']
        use_choices = {
            'left': [old_coordinates[0], old_coordinates[1] - 1],
            'right': [old_coordinates[0], old_coordinates[1] + 1],
            'up': [old_coordinates[0] - 1, old_coordinates[1]],
            'down': [old_coordinates[0] + 1, old_coordinates[1]],
        }
        choices_rand_sorted = random.sample(use_choices.keys(), len(use_choices.keys()))
        for choice in choices_rand_sorted:
            use_coordinates = use_choices[choice]
            use_option = self.get_open_option_if_valid_use_coordinate(use_coordinates)
            if use_option is not False:
                if use_option == self.KEY:
                    self.use_on_key(team, use_coordinates)
                else:
                    self.exit_maze(team, use_option)

    def process_action(self, team, user, action, msg_data):
        action_mapping = self.process_action_mapping.get(action)
        team_exit_maze = self.teams[team]['left_maze']
        user_has_action = action in self.teams[team]['users'][user]
        if action_mapping is None or team_exit_maze or not user_has_action:
            return False
        action_mapping(team)
        self.teams[team]['last_action'] = msg_data

    def process_msg(self, json_msg):
        msg_data = json.loads(json_msg)
        team = msg_data['team']
        user = msg_data['user']
        action = msg_data['action']
        self.process_action(team, user, action, msg_data)

        self.logger.debug(msg_data)

    def run(self):
        pubsub = self.redis_db.pubsub(ignore_subscribe_messages=True)
        self.show_updated_screen()
        pubsub.subscribe('scapi')
        pubsub.subscribe('scapi-admin')
        for message in pubsub.listen():
            try:
                if message['channel'].decode('utf-8') == 'scapi-admin':
                    game_over = self.process_admin_msg_game_over(message['data'].decode('utf-8'))
                    if game_over:
                        break
                else:
                    self.process_msg(message['data'].decode('utf-8'))
            except Exception as e:
                self.logger.warning(f'Error processing {message}:')
                self.logger.exception(e)
            finally:
                self.show_updated_screen()

    def show_updated_screen(self):
        self.show_board()
        self.show_last_actions()
        self.show_scores()

    def show_board(self):
        print('\n' * 100)
        for row in self.board:
            print(''.join(row))

    def show_last_actions(self):
        print(f'Last Team Action:')
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
            keys = team_data['keys']
            if left_maze:
                exit_time = team_data['exit_time']
                print(f'\t({team_id}){team}\t({exit_time}) ({keys} Keys):\t{score}')
            else:
                print(f'\t({team_id}){team}\t(On Going) ({keys} Keys):\t{score}  ')


if __name__ == '__main__':
    scapi_server = ScapiServer(
        redis_address=REDIS_ADDRESS, redis_port=REDIS_PORT,
        admin_pass=ADMIN_PASS,
        logging_level=LOGGING_LEVEL
    )
    try:
        scapi_server.run()
    except KeyboardInterrupt:
        pass
