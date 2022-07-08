import PySimpleGUI as sg
import definitions
import random
import functions


def create_draft():
    colors = ['#7aa7f0', '#f07a92']

    draft_tab = definitions.get_draft_key_tab()

    names = definitions.get_players()

    teams = [sg.Text('Teams'),
             functions.input_team('A', colors[0]),
             functions.input_team('B', colors[1]),
             sg.Button(key='-SWAP-', button_text='First drafting team', button_color=colors[0])]

    row_draft = [[sg.Text(f'Draft {i+1}'),
                  functions.input_player(i, 0, colors),
                  functions.input_player(i, 1, colors),
                  functions.input_player(i, 2, colors),
                  functions.input_player(i, 3, colors)]
                 for i in range(0,8)]

    layout = [[sg.Text('Draft', justification='center', expand_x=True)],
              teams,
              row_draft,
              [sg.Listbox(names, size=(20, 6), enable_events=True, key='-LIST-', font='18')],
              [sg.Button('Save'), sg.Button('Random team'), sg.Button('Exit')]]

    window = sg.Window('Draft', layout, return_keyboard_events=True)

    element_key = '-P0-'
    team_first_pick = 'A'

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):  # always check for closed window
            saved_values = values
            break

        # SWAP First team drafting
        if event == '-SWAP-':
            team_first_pick = 'B' if team_first_pick == 'A' else 'A'
            colors = functions.swap_colors(colors)
            window['-SWAP-'].update(button_color=colors[0])
            for i in range(32):
                draft_number = i//4
                if draft_number > 0:
                    player_order = i%4
                    player_color = functions.set_background_color(draft_number, player_order, colors)
                    window[f'-P{i}-'].update(background_color=player_color)

        # Finish draft and create teams and players
        if event == 'Save':
            saved_values = values
            saved_values['First pick'] = team_first_pick
            functions.save_json('draft.json', saved_values)
            print('Saved')

        # Set focus to current element if a player is about to be chosen.
        if '-P' in window.find_element_with_focus().key:
            element_key = window.find_element_with_focus().key

        # Listbox
        if '-P' in element_key:  # if a keystroke entered in search field
            search = values[element_key].lower()
            new_values = [x for x in names if search in x.lower()]  # do the filtering
            window['-LIST-'].update(new_values)  # display in the listbox
        else:
            # display original unfiltered list
            window['-LIST-'].update(names)

        if event == '\r':
            # Confirm player if it's the only one on the listbox
            if '-P' in element_key and len(window['-LIST-'].get_list_values()) == 1:
                window.find_element_with_focus().update(window['-LIST-'].get_list_values()[-1])
                window['-LIST-'].update(names)
                # Focus next field
                functions.focus_next_element(window, draft_tab)

        # if a player has been added from the list
        if event == '-LIST-' and len(values['-LIST-']):
            window[element_key].update(values['-LIST-'])
            window['-LIST-'].update(names)
            functions.focus_next_element(window, draft_tab)

        if event == 'Random team':
            for i in range(len(draft_tab)):
                if i > 1:
                    window[draft_tab[i]].update(random.choice(names))

    window.close()
