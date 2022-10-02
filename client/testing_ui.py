import os.path

import PySimpleGUI as sg

from conf import PROJECT_ROOT, WIDTH, HEIGHT, IMG_FOLDER, SPRITE_DICT, FONT_HEADER


class ClientUIMaker:
    DEFAULT_SIZE = (WIDTH, HEIGHT)

    def __init__(self, board):
        sg.theme('DarkAmber')
        self.board = board
        self.default_button_color = sg.LOOK_AND_FEEL_TABLE[sg.theme()]['BUTTON']
        self.active_button_color = ('#0000FF', '#FF0000')  # (font color, background color)
        self.title = 'ScaPi Game'
        self.window = None
        self.board_width = len(board[0])
        self.board_height = len(board)
        self.create_main_screen()

    def create_window(self, sub_title, layout, size=DEFAULT_SIZE):
        self.window = sg.Window(f'{self.title} - {sub_title}', layout, size=size)
        return self.window

    def create_main_menu_testing(self):
        self.index_img = 1
        self.image_current_images = ['img_01.png' for i in range(3)]
        img_path = os.path.join(IMG_FOLDER, 'img_01.png')
        layout = [
            [sg.Text('Loading Images')],
            [sg.Image(img_path, key='img_1', pad=0), sg.Image(img_path, key='img_2', pad=0),
             sg.Image(img_path, key='img_3', pad=0)],
            [sg.Image(img_path, key='img_1', pad=0), sg.Image(img_path, key='img_2', pad=0),
             sg.Image(img_path, key='img_3', pad=0)],
            [sg.Image(img_path, key='img_1', pad=0), sg.Image(img_path, key='img_2', pad=0),
             sg.Image(img_path, key='img_3', pad=0)],
            [sg.Button('Change image')]
        ]
        self.create_window('Testing Show images', layout)

    def create_board_layout(self):
        layout = []

        for i in range(self.board_height):
            current_row = []
            for j in range(self.board_width):
                tile = self.board[i][j]
                img_name = SPRITE_DICT[tile]
                img_path = os.path.join(IMG_FOLDER, img_name)
                img = sg.Image(img_path, key=(i, j), pad=0)
                current_row.append(img)
            layout.append(current_row)
        return layout

    def create_main_screen(self):
        board_layout = self.create_board_layout()
        title_layout = [[sg.Text('ScaPi Game - Level 1', font=FONT_HEADER)]]
        time_layout = [[sg.Text('Time Left: 150s', font=FONT_HEADER)]]
        team_layout = [[sg.Text('Team Information:', font=FONT_HEADER)]]
        actions_layout = [[sg.Text('Your Actions:', font=FONT_HEADER)]]

        layout = [
            [sg.Column(title_layout, expand_x=True, element_justification='left'),
             sg.Column(time_layout, expand_x=True, element_justification='right')],
            [sg.Column(board_layout, expand_x=True),
             sg.Column(team_layout, expand_x=True, element_justification='right', vertical_alignment='top')],
            [sg.Column(actions_layout, expand_x=True)]

        ]
        self.create_window('Playing Board', layout)

    def process_event(self, event, values):
        if event == 'Change image':
            if self.index_img > 3:
                self.index_img = 1
            img_change = self.window[f'img_{self.index_img}']

            img_file_name = self.image_current_images[self.index_img - 1]
            if img_file_name == 'img_01.png':
                img_file_name = 'img_02.png'
            elif img_file_name == 'img_02.png':
                img_file_name = 'img_03.png'
            else:
                img_file_name = 'img_01.png'
            self.image_current_images[self.index_img - 1] = img_file_name
            img_change.Update(os.path.join(PROJECT_ROOT, 'assets', img_file_name))
            self.index_img += 1

        if event == 'Create':
            self.window.close()
            width = int(values[0])
            height = int(values[1])

            self.create_board_edit_window(width, height)

        if event in ['.', '#', '|', '@', 'K', '!']:
            self.update_active_tool(event)

        if event == 'Save':
            self.window.close()
            self.save_board_window()

        if event == 'Save File':
            self.window.close()
            board_id = values[0]
            self.save_board_as_file(board_id)

        if isinstance(event, tuple):
            self.write_on_board(event)

    def run(self):
        # Event Loop to process "events"
        try:
            while True:
                event, values = self.window.read()
                print(f'{event}, {values}')
                if event in (sg.WIN_CLOSED, 'Cancel'):
                    break
                self.process_event(event, values)
        # except Exception:
        #     pass
        finally:
            self.window.close()


if __name__ == '__main__':
    board_example = [
        ['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '@', '|', '|', '|', '|'],
        ['|', 'K', '.', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
        ['|', '.', '.', '.', '|', '.', '.', '.', '|', '.', '|', '.', '.', '.', '.', '|'],
        ['|', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
        ['|', '.', '.', '.', '1', '2', '3', '4', '5', '.', '.', '.', '.', '.', '.', '|'],
        ['|', '|', '.', '.', '.', '.', '|', '.', '.', '.', '.', '|', '.', '.', '.', '|'],
        ['|', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
        ['|', '.', '|', 'K', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
        ['#', '.', '.', '|', '|', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '|'],
        ['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '#', '|']
    ]

    client_ui = ClientUIMaker(board_example)
    client_ui.run()
