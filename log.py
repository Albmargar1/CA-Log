import PySimpleGUI as sg
import definitions
import random
import functions
import time

def log():
    colors = definitions.get_colors()

    lineup_layout = functions.create_lineup_layout(colors)
    log_layout = functions.create_log_layout()

    timer_layout = [[sg.Text('Timer', size=(8, 1), font='Arial 20', justification='center')],
                    [sg.Text('00:00', size=(8, 1), font=('Helvetica', 20), justification='center', key='timer_text')],
                    [sg.Button('Pause', button_color=('white', '#001480'), key='timer_button'),
                     sg.Button('Next half', button_color=('white', '#007339'))]]

    layout = [[sg.Column(lineup_layout),
               sg.Column(log_layout),
               sg.Column(timer_layout, vertical_alignment='top', pad=(25,25))],
              [sg.Button('Load lineup'), sg.Button('Exit')]]

    window = sg.Window('Log', layout, return_keyboard_events=True)

    current_time = 0
    paused_time = 0
    paused = False
    start_time = int(round(time.time()*100))
    extra_actions = 0
    current_half = 0
    minute_starting_half = [0, 45, 90, 105, 120]

    while True:
        if not paused:
            event, values = window.read(timeout=1000) # change it to 100
            current_time = int(round(time.time() * 100)) - start_time
        else:
            event, values = window.read()

        print(event, values)

        if event in (sg.WIN_CLOSED, 'Exit'):  # always check for closed window
            break

        # TIMER
        if event == 'timer_button':
            event = window[event].GetText()
        if event == 'Next half':
            start_time = int(round(time.time() * 100))
            current_half = current_half + 1 if minute_starting_half[current_half] < 120 else 0
            current_time = 0
            paused_time = start_time
        elif event == 'Pause':
            paused = True
            paused_time = int(round(time.time() * 100))
            window['timer_button'].update(text='Run')
        elif event == 'Run':
            paused = False
            start_time = start_time + int(round(time.time() * 100)) - paused_time
            window['timer_button'].update(text='Pause')

        if current_half < 4:
            if minute_starting_half[current_half + 1] < (current_time // 100) // 60:
                current_time = minute_starting_half[current_half + 1]
        window['timer_text'].update('{:02d}:{:02d}'.format((current_time // 100) // 60  + minute_starting_half[current_half],
                                                           (current_time // 100) % 60))

        if event == 'Load lineup':
            functions.load_lineup_json('lineup.json', window)

        if '-C' in event:
            functions.update_action_buttons_color(window, event)
            
            text = window[event].get_text() + '\n'
            window['-LOG-'].update(value=text, append=True)

    window.close()