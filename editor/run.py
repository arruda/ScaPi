#!/usr/bin/env python
import PySimpleGUI as sg


class Editor:
    DEFAULT_SIZE = (640, 480)

    def __init__(self):
        sg.theme('DarkAmber')
        self.title = 'ScaPi Editor'
        self.create_main_menu()

    def create_window(self, sub_title, layout, size=DEFAULT_SIZE):
        self.window = sg.Window(f'{self.title} - {sub_title}', layout, size=size)
        return self.window

    def create_main_menu(self):
        # sg.theme('DarkAmber')
        layout = [[sg.Text('Main Menu')],
                  [sg.Text('Available Options:')],
                  [sg.Button('Create New')]]
        self.create_window('Main Menu', layout)
        # self.window = sg.Window(f'{self.title} - Main Menu', layout)

    def process_event(self, event, values):
        if event == 'Create New':
            self.window.close()
            self.create_board_options_window()

        if event == 'Create':
            self.window.close()
            self.create_board_edit_window()

    def create_board_options_window(self):
        layout = [[sg.Text('Main Menu')],
                  [sg.Text('Width:'), sg.InputText()],
                  [sg.Text('Height:'), sg.InputText()],
                  [sg.Button('Create')]]

        self.create_window('Board Options', layout)

    def create_board_edit_window(self):
        layout = [[sg.Text('Edit Board')],
                  [sg.Button('Save')]]
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
        except Exception:
            pass
        finally:
            self.window.close()


if __name__ == '__main__':
    my_editor = Editor()
    my_editor.run()
