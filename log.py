import PySimpleGUI as sg
import definitions
import random
import functions
import time


def log():
    text_lineup = ''

    lineup_layout = functions.create_lineup_layout(text_lineup)
    log_layout = functions.create_log_layout()

    timer_layout = [[sg.Text('Timer', size=(8, 1), font='Arial 20', justification='center', expand_x=True)],
                    [sg.Text('00:00', size=(8, 1), font=('Helvetica', 20), justification='center', key='timer_text',
                             expand_x=True)],
                    [sg.Button('Pause', button_color=('white', '#001480'), key='timer_button', expand_x=True),
                     sg.Button('Next half', button_color=('white', '#007339'), expand_x=True)],
                    [sg.Text('')]]

    layout = [[sg.Column(lineup_layout),
               sg.Column(timer_layout + log_layout)],
              [sg.Button('Load lineup'), sg.Button('Exit')]]

    window = sg.Window('Log', layout, return_keyboard_events=True)

    current_time = 0
    paused_time = 0
    paused = False
    start_time = int(round(time.time() * 100))
    extra_actions = 0
    current_half = 0
    minute_starting_half = [0, 45, 90, 105, 120]

    pressed_buttons = []
    pressed_action = ''
    start = True
    while True:
        if not paused:
            event, values = window.read(timeout=1000)  # change it to 100
            current_time = int(round(time.time() * 100)) - start_time
        else:
            event, values = window.read()

        cur_minute = (current_time // 100) // 60

        if start:
            functions.load_lineup_json('lineup.json', window)
            start = False

        print(event, values)

        if event in (sg.WIN_CLOSED, 'Exit'):  # always check for closed window
            break

        if '-C' in event:
            if pressed_action != '':
                window[pressed_action].update(button_color=functions.swap_colors(window[pressed_action].ButtonColor))
            pressed_action = event
            window[event].update(button_color=functions.swap_colors(window[event].ButtonColor))
            functions.update_action_buttons_color(window, event)

        if 'Submit' in event and pressed_action != '':

            text = str(cur_minute) + ' - '
            if window['Agent'].get_text() != '':
                text += window['Agent'].get_text() + ' performs ' + window[pressed_action].get_text()
            else:
                text += window[pressed_action].get_text()
            if window['Recipient'].get_text() != '':
                text += ' on ' + window['Recipient'].get_text()
            if window['Result'].get_text() != '':
                text += ' resulting in ' + window['Result'].get_text()
            text += '\n'

            window['-LOG-'].update(value=text, append=True)

        if (event == 'Agent' and window['Agent'].get_text() != '') \
                or (event == 'Recipient' and window['Recipient'].get_text() != '') \
                or '-A' in event or '-B' in event:

            pressed_buttons.append(event)
            if len(pressed_buttons) == 1:
                window[pressed_buttons[0]].update(
                    button_color=functions.swap_colors(window[pressed_buttons[0]].ButtonColor))
            if len(pressed_buttons) == 2:
                lineup_button = ''
                action_button = ''
                for button in pressed_buttons:
                    if button == 'Agent' or button == 'Recipient':
                        action_button = button
                    elif '-A' in button or '-B' in button:
                        lineup_button = button

                if lineup_button != '' and action_button != '':
                    window[action_button].update(text=window[lineup_button].get_text())

                window[pressed_buttons[0]].update(
                    button_color=functions.swap_colors(window[pressed_buttons[0]].ButtonColor))
                pressed_buttons = []

        if event == 'Result':
            if window['Result'].get_text() == 'Success':
                window['Result'].update(text='Failure', button_color=definitions.get_colors_options_buttons()[2])
            elif window['Result'].get_text() == 'Failure':
                window['Result'].update(text='Success', button_color=definitions.get_colors_options_buttons()[0])

        if event == 'Agent':
            if window['Agent'].get_text() != '':
                print('hi')

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
        window['timer_text'].update(
            '{:02d}:{:02d}'.format((current_time // 100) // 60 + minute_starting_half[current_half],
                                   (current_time // 100) % 60))

    window.close()
