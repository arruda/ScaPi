import os.path

import PySimpleGUI as sg

from conf import PROJECT_ROOT


class ClientUIMaker:
    DEFAULT_SIZE = (640, 480)

    def __init__(self):
        sg.theme('DarkAmber')
        self.default_button_color = sg.LOOK_AND_FEEL_TABLE[sg.theme()]['BUTTON']
        self.active_button_color = ('#0000FF', '#FF0000')  # (font color, background color)
        self.title = 'ScaPi Game'
        self.default_board_id = 'board_00'
        self.window = None
        self.create_main_menu()

    def create_window(self, sub_title, layout, size=DEFAULT_SIZE):
        self.window = sg.Window(f'{self.title} - {sub_title}', layout, size=size)
        return self.window

    def create_main_menu(self):
        self.index_img = 1
        self.image_current_images = ['img_01.png' for i in range(3)]
        img_path = os.path.join(PROJECT_ROOT, 'assets', 'img_01.png')
        print(img_path)
        layout = [
            [sg.Text('Loading Images')],
            [sg.Image(img_path, key='img_1'), sg.Image(img_path, key='img_2'), sg.Image(img_path, key='img_3')],
            [sg.Button('Change image')]
        ]
        self.create_window('Testing Show images', layout)

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
    client_ui = ClientUIMaker()
    client_ui.run()
