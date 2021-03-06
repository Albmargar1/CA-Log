import PySimpleGUI as sg
import definitions
import random
import functions


def draft():
    colors = definitions.get_colors()
    names = definitions.get_players()
    draft_tab = definitions.get_draft_key_tab()
    A_tab = definitions.get_lineup_key_tab('A')
    B_tab = definitions.get_lineup_key_tab('B')

    draft_layout = functions.create_draft_layout(names, colors)
    lineup_layout = functions.create_lineup_layout(colors, erase_player=True)
    layout = [[sg.Column(draft_layout), sg.Column(lineup_layout)]]

    window = sg.Window('Draft', layout, return_keyboard_events=True, no_titlebar=True)

    prev_draft_focused_key = '-P0-'
    prev_lineup_focused_key = '-nA0-'
    team_first_pick = 'A'

    pressed_buttons = []
    team_A_draft_keys, team_B_draft_keys = functions.set_teams(team_first_pick)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):  # always check for closed window
            functions.save_draft(window)
            break

        #############
        ### DRAFT ###
        #############

        # Set team name in lineup
        window['-LA-'].update(value=window['A'].get())
        window['-LB-'].update(value=window['B'].get())

        # SWAP First team drafting
        if event == '-SWAP-':
            team_first_pick = 'B' if team_first_pick == 'A' else 'A'
            colors = functions.swap_colors(colors)
            window['-SWAP-'].update(button_color=colors[0])
            for i in range(32):
                draft_number = i//4
                if draft_number > 0:
                    player_order = i % 4
                    player_color = functions.set_draft_background_color(draft_number, player_order, colors)
                    window[f'-P{i}-'].update(background_color=player_color)

            team_A_draft_keys, team_B_draft_keys = functions.set_teams(team_first_pick)
            functions.swap_lineup(window) # Swap already drafted players

        # Set focus to current element if a player is about to be chosen.
        if '-P' in window.find_element_with_focus().key:
            prev_draft_focused_key = window.find_element_with_focus().key

        # Search on listbox
        if '-P' in prev_draft_focused_key:  # if a keystroke entered in search field
            search = values[prev_draft_focused_key].lower()
            new_values = [x for x in names if search in x.lower()]  # do the filtering
            window['-LIST-'].update(new_values)  # display in the listbox

        else:
            # display original unfiltered list
            window['-LIST-'].update(names)

        # if a player has been added from the list
        if event == '-LIST-' and len(values['-LIST-']):
            window[prev_draft_focused_key].update(values['-LIST-'])
            window['-LIST-'].update(names)
            functions.focus_next_element(window, draft_tab)

        if event == 'Random team':
            for i in range(len(draft_tab)):
                if i > 1 and window[draft_tab[i]].get() == '':
                    window[draft_tab[i]].update(random.choice(names))

                    focus_element = window[draft_tab[i]]
                    value = focus_element.get()

                    if functions.check_element_in_list(focus_element.key, team_A_draft_keys):
                        functions.add_player_first_empty_string(value, A_tab, window)
                    else:
                        functions.add_player_first_empty_string(value, B_tab, window)

        ##############
        ### LINEUP ###
        ##############

        # Swap 2 players in lineup
        if '-A' in event or '-B' in event or '-ERASE-' in event:
            pressed_buttons.append(event)
            if len(pressed_buttons) == 1:
                window[event].update(button_color=functions.swap_colors(definitions.get_colors_button()))
            if len(pressed_buttons) == 2:
                if ('-A' in pressed_buttons[0] and '-A' in pressed_buttons[1]) or (
                   '-B' in pressed_buttons[0] and '-B' in pressed_buttons[1]):
                    functions.swap_players_button(pressed_buttons, window)
                elif '-ERASE-' in pressed_buttons[0]:
                    window[pressed_buttons[1]].update(text='')
                elif '-ERASE-' in pressed_buttons[1]:
                    window[pressed_buttons[0]].update(text='')

                window[pressed_buttons[0]].update(button_color=definitions.get_colors_button())
                pressed_buttons = []

        ################
        ### Navigate ###
        ################

        if event.split(':')[0] in ['Right', 'Left', 'Up', 'Down', '\r']:
            pressed_key = event.split(':')[0]

            # Confirm player if it's the only one on the listbox
            if '-P' in prev_draft_focused_key and len(window['-LIST-'].get_list_values()) == 1:
                focus_element = window.find_element_with_focus()
                value = window['-LIST-'].get_list_values()[-1]

                if functions.check_element_in_list(focus_element.key, team_A_draft_keys):
                    functions.add_player_first_empty_string(value, A_tab, window)
                else:
                    functions.add_player_first_empty_string(value, B_tab, window)

                focus_element.update(value)
                window['-LIST-'].update(names)

            # Focus next field
            if pressed_key in ['Right', 'Down', '\r']:
                functions.focus_next_element(window, draft_tab, 1)
            elif pressed_key in ['Left', 'Up']:
                functions.focus_next_element(window, draft_tab, -1)

    window.close()

    return values