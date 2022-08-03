import PySimpleGUI as sg
import definitions
import random
import functions


def draft():
    colors = definitions.get_colors_teams()
    names = definitions.get_players()
    draft_tab = definitions.get_draft_key_tab()
    A_tab = definitions.get_lineup_key_tab('A')
    B_tab = definitions.get_lineup_key_tab('B')

    text_lineup = '1) Set player number in lineup by clicking\n' \
                  '    on two boxes of the same team. \n' \
                  '    This will swap both players.\n'

    draft_layout = functions.create_draft_layout()
    lineup_layout = functions.create_lineup_layout(text_lineup)
    layout = [[sg.Column(draft_layout, vertical_alignment='top', pad=((0,40),(0,0))),
               sg.Column(lineup_layout, vertical_alignment='top')]]

    window = sg.Window('Draft', layout, return_keyboard_events=True)

    team_first_pick = 'A'
    pressed_buttons = []
    team_A_draft_keys, team_B_draft_keys = functions.set_teams(team_first_pick)

    while True:
        event, values = window.read()
        print(event, values)

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

        # Search on listbox
        if '-P' in window.find_element_with_focus().key:  # if a keystroke entered in search field
            search = values[window.find_element_with_focus().key].lower()
            new_values = [x for x in names if search in x.lower()]  # do the filtering
            window['-LIST-'].update(new_values)  # display in the listbox

        else:
            # display original unfiltered list
            window['-LIST-'].update(names)

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

        ################
        ### Navigate ###
        ################

        if event.split(':')[0] in ['Right', 'Left', 'Up', 'Down', '\r']:
            pressed_key = event.split(':')[0]

            # Confirm player if it's the only one on the listbox
            if '-P' in window.find_element_with_focus().key and len(window['-LIST-'].get_list_values()) == 1:
                focus_element = window.find_element_with_focus()
                value = window['-LIST-'].get_list_values()[-1]

                already_in_list = False
                for key in draft_tab:
                    if value == window[key].get():
                        already_in_list = True
                        break

                if not already_in_list:
                    if functions.check_element_in_list(focus_element.key, team_A_draft_keys):
                        functions.add_player_first_empty_string(value, A_tab, window)
                    else:
                        functions.add_player_first_empty_string(value, B_tab, window)

                focus_element.update(value)
                window['-LIST-'].update(names)

                if pressed_key == '\r':
                    functions.focus_next_element(window, draft_tab, 1)

            # Focus next field
            if pressed_key in ['Right', 'Down']:
                functions.focus_next_element(window, draft_tab, 1)
            elif pressed_key in ['Left', 'Up']:
                functions.focus_next_element(window, draft_tab, -1)

        ##############
        ### LINEUP ###
        ##############

        # Swap 2 players in lineup
        if '-A' in event or '-B' in event or 'Erase a player' in event:
            pressed_buttons.append(event)
            if len(pressed_buttons) == 1:
                if '-A' in event:
                    window[event].update(button_color=functions.swap_colors(definitions.get_colors_button_A()))
                elif '-B' in event:
                    window[event].update(button_color=functions.swap_colors(definitions.get_colors_button_B()))
            if len(pressed_buttons) == 2:
                if ('-A' in pressed_buttons[0] and '-A' in pressed_buttons[1]) or (
                   '-B' in pressed_buttons[0] and '-B' in pressed_buttons[1]):
                    functions.swap_players_button(pressed_buttons, window)
                elif 'Erase a player' in pressed_buttons[0]:
                    for key in draft_tab:
                        if window[key].get() == window[pressed_buttons[1]].get_text():
                            window[key].update(value='')
                    window[pressed_buttons[1]].update(text='')
                elif 'Erase a player' in pressed_buttons[1]:
                    for key in draft_tab:
                        if window[key].get() == window[pressed_buttons[0]].get_text():
                            window[key].update(value='')
                    window[pressed_buttons[0]].update(text='')

                if '-A' in event:
                    window[pressed_buttons[0]].update(button_color=definitions.get_colors_button_A())
                elif '-B' in event:
                    window[pressed_buttons[0]].update(button_color=definitions.get_colors_button_B())
                pressed_buttons = []

    window.close()

    return values