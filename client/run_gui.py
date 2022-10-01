#!/usr/bin/env python
import json
import os
import logging
import sys
import time
import threading

import logzero
import redis
import PySimpleGUI as sg

from conf import *


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER_PROJECT_ROOT = os.path.join(PROJECT_ROOT, 'server')
BOARDS_DIR = os.path.join(SERVER_PROJECT_ROOT, 'boards')


class GameGUI:

    def __init__(self):
        self.logging_level = 'DEBUG'
        self.logger = self._setup_logging()
        sg.theme('Dark Blue 3')
        self.default_button_color = sg.LOOK_AND_FEEL_TABLE[sg.theme()]['BUTTON']
        self.active_button_color = ('#0000FF', '#FF0000')  # (font color, background color)
        self.title = TITLE
        self.default_board_id = 'board_00'
        self.window = None
        self.active_tool = None
        self.board_content = None
        # self.redis_connection_info = (redis_address, redis_port)
        self.redis_db = None
        self.pubsub = None
        # self.scapi_team = scapi_team
        # self.scapi_user = scapi_user
        self.user_actions = []
        self.create_main_menu()

    def _setup_logging(self):
        log_format = (
            '%(color)s[%(levelname)1.1s %(name)s %(asctime)s:%(msecs)d '
            '%(module)s:%(funcName)s:%(lineno)d]%(end_color)s %(message)s'
        )
        formatter = logzero.LogFormatter(fmt=log_format)
        return logzero.setup_logger(
            name=self.__class__.__name__, level=logging.getLevelName(self.logging_level), formatter=formatter)


    def connect_to_server(self, redis_address, redis_port):
        print(f'connect_to_server: {redis_address}, {redis_port}')
        self.redis_db = redis.Redis(host=redis_address, port=redis_port)

    def setup_user_pubsub(self, scapi_team, scapi_user):
        print('setup_user_pubsub')

        if self.redis_db is None:
            raise Exception('No connection to server when setting up user!')
        self.scapi_team = scapi_team
        self.scapi_user = scapi_user
        self.pubsub = self.redis_db.pubsub(ignore_subscribe_messages=True)
        user_topic = f'{self.scapi_team}/{self.scapi_user}'
        self.pubsub.subscribe(user_topic)

    def send_registration_msg(self):
        msg_data = {
            'team': self.scapi_team,
            'user': self.scapi_user
        }
        json_msg = json.dumps(msg_data)
        self.redis_db.publish('scapi-setup', json_msg)

    # def try_register_loop(self):
    #     self.send_registration_msg()
    #     self.logger.info((
    #         f'Waiting for list of user actions on game start...'
    #     ))
    #     for message in self.pubsub.listen():
    #         try:
    #             self.process_receive_user_action_msg(message['data'].decode('utf-8'))
    #             return True
    #         except Exception as e:
    #             self.logger.error(f'Error processing {message}:')
    #             self.logger.exception(e)
    #             self.logger.error(
    #                 f'Will exit client. Contact ScaPi ADMIN of the issue, with the exception stack trace information'
    #             )
    #             return False

    def create_window(self, sub_title, layout, size=DEFAULT_WINDOW_SIZE):
        self.window = sg.Window(f'{self.title} - {sub_title}', layout, size=size)
        return self.window

    def create_main_menu(self):
        layout = [[sg.Text('Main Menu')],
                  [sg.Text('Available Options:')],
                  [sg.Button('Join Game')]]
        self.create_window('Main Menu', layout)

    def create_register_player_window(self):
        layout = [[sg.Text('Join Game')],
                  [sg.Text('Server address:'), sg.InputText(default_text=REDIS_ADDRESS)],
                  [sg.Text('Server port:'), sg.InputText(default_text=REDIS_PORT)],
                  [sg.Text('Team Name:'), sg.InputText(default_text=TEAM_NAME)],
                  [sg.Text('User:'), sg.InputText(default_text=USER)],
                  [sg.Button('Join')]]

        self.create_window('Join Game', layout)

    def create_joining_game_window(self, redis_addres, redis_port, scapi_team, scapi_user):
        self.connect_to_server(redis_addres, redis_port)
        self.setup_user_pubsub(scapi_team, scapi_user)

        print('finished setup pubsub will create window')

        layout = [[sg.Text('Waiting for server to start game...')]]
        self.create_window('Joining Game...', layout)
        self.send_registration_msg()

    def create_game_window(self):
        layout = [[sg.Text('Game has started...')]]
        self.create_window('Game Running', layout)

        # time.sleep(10)
        # if self.try_register_loop():
        #     pass

    def process_client_event(self, event, values):
        if event == 'Join Game':
            self.window.close()
            self.create_register_player_window()

        if event == 'Join':
            self.window.close()
            self.create_joining_game_window(*values.values())

    def run_client_event_loop(self):
        event, values = self.window.read(timeout=10)
        if event != sg.TIMEOUT_KEY:
            print(f'{event}, {values}')
            if event in (sg.WIN_CLOSED, 'Cancel'):
                self.game_is_running = False
            self.process_client_event(event, values)


    def process_game_starting_event(self, event):
        board = event.get('board')
        actions = event.get('actions')
        players = event.get('player')
        self.window.close()
        self.create_game_window(board, )


    def process_server_event(self, event):
        print(f'processing server event: {event}')
        # import pdb;pdb.set_trace()
        if event['type'] == 'game_starting':
            self.process_game_starting_event(event)

    def run_connection_event_loop(self):
        if self.pubsub is None:
            return

        message = self.pubsub.get_message()
        if message:
            self.process_server_event(json.loads(message['data'].decode('utf-8')))

            # try:
            #     self.process_receive_user_action_msg(message['data'].decode('utf-8'))
            #     return True
            # except Exception as e:
            #     self.logger.error(f'Error processing {message}:')
            #     self.logger.exception(e)
            #     self.logger.error(
            #         f'Will exit client. Contact ScaPi ADMIN of the issue, with the exception stack trace information'
            #     )
            #     return False

    def run(self):
        # Event Loop to process "events"
        self.game_is_running = True
        try:
            while self.game_is_running:
                self.run_connection_event_loop()
                self.run_client_event_loop()
        except Exception as e:
            self.logger.error(e)
            self.logger.exception(e)
        finally:
            self.window.close()
            sys.exit()

        # self.client_loop = threading.Thread(target=self.run_client_loop, args=())
        # # self.connection_loop = threading.Thread(target=self.run_connection_loop, args=())

        # # self.connection_loop.start()
        # self.client_loop.start()

        # self.client_loop.join()
        # # self.connection_loop.join()

    def write_on_board(self, event):
        i, j = event
        self.board_content[i][j] = self.active_tool
        if self.active_tool:
            btn = self.window[event]
            btn.Update(text=self.active_tool)


if __name__ == '__main__':
    my_cli = GameGUI()
    my_cli.run()
