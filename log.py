import PySimpleGUI as sg
import definitions
import random
import functions

def log():
    colors = definitions.get_colors()

    lineup_layout = functions.create_lineup_layout(colors)
    log_layout = functions.create_log_layout()

    layout = [[sg.Column(lineup_layout), sg.Column(log_layout)],
              [sg.Button('Load lineup'), sg.Button('Exit')]]

    window = sg.Window('Log', layout, return_keyboard_events=True, no_titlebar=True)

    while True:
        event, values = window.read()
        print(event, values)

        if event in (sg.WIN_CLOSED, 'Exit'):  # always check for closed window
            break

        if event == 'Load lineup':
            functions.load_lineup_json('lineup.json', window)

        if '-C' in event:
            text = window[event].get_text() + '\n'
            window['-LOG-'].update(value=text, append=True)

    window.close()