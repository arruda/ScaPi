#!/usr/bin/env python
import PySimpleGUI as sg


class Editor:
    def __init__(self):
        self.title = 'ScaPi Editor'
        self.create_main_menu()

    def create_window(self):
        sg.theme('DarkAmber')
        layout = [[sg.Text('Some text on Row 1')],
                  [sg.Text('Enter something on Row 2'), sg.InputText()],
                  [sg.OK(), sg.Cancel()]]
        self.window = sg.Window(f'{self.title} - Main Window', layout)

    def create_main_menu(self):
        sg.theme('DarkAmber')
        layout = [[sg.Text('Main Menu')],
                  [sg.Text('Available Options:')],
                  [sg.Button('Testing')]]
        self.window = sg.Window(f'{self.title} - Main Menu', layout)

    def run(self):
        # Event Loop to process "events"
        try:
            while True:
                event, values = self.window.read()
                print(f'{event}, {values}')
                if event in (sg.WIN_CLOSED, 'Cancel'):
                    break
        except Exception:
            pass
        finally:
            self.window.close()


if __name__ == '__main__':
    my_editor = Editor()
    my_editor.run()
