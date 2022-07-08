import PySimpleGUI as sg
import functions
import definitions

def create_lineup():
    colors = ['#7aa7f0', '#f07a92']

    A_tab = definitions.get_lineup_key_tab('A')
    B_tab = definitions.get_lineup_key_tab('B')

    teams = [functions.draft_team('A', colors[0]),
             functions.draft_team('B', colors[1])]

    row_players_title = [sg.Text('Nº', justification='center'),
                         sg.Text('Players', justification='center', expand_x=True),
                         sg.Text('Nº', justification='center'),
                         sg.Text('Players', justification='center', expand_x=True)]

    row_players = [[functions.draft_player_number('A', i),
                    functions.draft_player_name(i, 'A', i),
                    functions.draft_player_number('B', i),
                    functions.draft_player_name(i, 'B', i)]
                   for i in range(1, 17)]

    layout = [[sg.Text('Lineup', justification='center', expand_x=True)],
              teams,
              row_players_title,
              row_players,
              [sg.Button('Load'), sg.Button('Save'), sg.Button('Exit')]]

    window = sg.Window('Lineup', layout, return_keyboard_events=True)
    pressed_buttons = []

    while True:
        event, values = window.read()
        element = window.find_element_with_focus()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Load':
            draft = functions.read_json('draft.json')
            functions.draft_values_to_lineup(draft, window)

        if event == 'Save':
            saved_values = values
            functions.save_json('lineup.json', saved_values)
            print('Saved')

        if '-A' in event or '-B' in event:
            pressed_buttons.append(event)
            if len(pressed_buttons) == 2:
                functions.swap_players_button(pressed_buttons, window)

                pressed_buttons = []

        if event == '\r':
            if '-nA' in element.key:
                functions.swap_players('A', window)
                functions.focus_next_element(window, A_tab)
            elif '-nB' in element.key:
                functions.swap_players('B', window)
                functions.focus_next_element(window, B_tab)

        if 'Prior' in event:
            if '-nA' in element.key:
                functions.focus_next_element(window, A_tab, direction=-1)
            elif '-nB' in element.key:
                functions.focus_next_element(window, B_tab, direction=-1)

    window.close()