#!/usr/bin/env python
import PySimpleGUI as sg


class Editor:
    DEFAULT_SIZE = (640, 480)

    def __init__(self):
        sg.theme('Dark Blue 3')
        self.default_button_color = sg.LOOK_AND_FEEL_TABLE[sg.theme()]['BUTTON']
        self.active_button_color = ('#0000FF', '#FF0000')  # (font color, background color)
        self.title = 'ScaPi Editor'
        self.create_main_menu()
        self.active_tool = None

    def create_window(self, sub_title, layout, size=DEFAULT_SIZE):
        self.window = sg.Window(f'{self.title} - {sub_title}', layout, size=size)
        return self.window

    def create_main_menu(self):
        layout = [[sg.Text('Main Menu')],
                  [sg.Text('Available Options:')],
                  [sg.Button('Create New')]]
        self.create_window('Main Menu', layout)
        # self.window = sg.Window(f'{self.title} - Main Menu', layout)

    def update_active_button_color(self, active=False):
        color = self.active_button_color if active else self.default_button_color
        btn = self.window[self.active_tool]
        btn.Update(button_color=color)

    def update_active_tool(self, event):
        if self.active_tool is not None:
            self.update_active_button_color(active=False)

        self.active_tool = event
        self.update_active_button_color(active=True)

    def process_event(self, event, values):
        if event == 'Create New':
            self.window.close()
            self.create_board_options_window()

        if event == 'Create':
            self.window.close()
            width = int(values[0])
            height = int(values[1])

            self.create_board_edit_window(width, height)

        if event in ['.', '#', '|', '@', 'K', '!']:
            self.update_active_tool(event)

    def create_board_options_window(self):
        layout = [[sg.Text('Main Menu')],
                  [sg.Text('Width:'), sg.InputText(default_text='10')],
                  [sg.Text('Height:'), sg.InputText(default_text='10')],
                  [sg.Button('Create')]]

        self.create_window('Board Options', layout)

    def create_board_layout(self, width, height):
        layout = []
        for i in range(width):
            row = []
            for j in range(height):
                button_key = (i, j)
                row.append(sg.Button('.', size=(1, 1), key=button_key))
            layout.append(row)

        return layout

    def create_board_edit_window(self, width, height):
        layout = self.create_board_layout(width, height)
        board_frame = sg.Frame(
            layout=layout,
            title='Board', title_color='red', relief=sg.RELIEF_SUNKEN,
            tooltip='Use these to set flags',
            background_color='white',
        )

        menu_frame = sg.Frame(
            layout=[
                [sg.Text('Walkable Path:'), sg.Button('.', size=(1, 1))],
                [sg.Text('Wall:'), sg.Button('|', size=(1, 1))],
                [sg.Text('Exit:'), sg.Button('@', size=(1, 1))],
                [sg.Text('Key:'), sg.Button('K', size=(1, 1))],
                [sg.Text('Magic Door:'), sg.Button('#', size=(1, 1))],
                [sg.Text('Spawn Point:'), sg.Button('!', size=(1, 1))],
                [sg.Button('Save')]
            ],
            title='Menu', title_color='white', relief=sg.RELIEF_SUNKEN,
            tooltip='Use these to set flags',
            element_justification='right',
        )
        layout = [
            [sg.Text('Edit Board')],
            [
                board_frame,
                menu_frame
            ],
        ]
        self.create_window('Edit Board', layout)

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
    my_editor = Editor()
    my_editor.run()
