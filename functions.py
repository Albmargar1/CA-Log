import PySimpleGUI as sg
import json
import re
import definitions


def swap_colors(colors):
    return (colors[1], colors[0])


def save_json(path, dic):
    json_string = json.dumps(dic)
    with open(path, 'w') as outfile:
        outfile.write(json_string)


def load_json(path):
    data = 0
    with open(path, 'r') as f:
        data = json.load(f)

    return data


def read_json(path):
    with open(path, 'r') as infile:
        data = json.load(infile)
    return data


def set_teams(first_pick):
    teams = {'A': ['-P0-', '-P1-'], 'B': ['-P2-', '-P3-']}

    turn = ['A', 'B'] if first_pick == 'A' else ['B', 'A']
    for i in range(1, 8):
        teams[turn[0]].append(f'-P{4 * i + 0}-')
        teams[turn[1]].append(f'-P{4 * i + 1}-')
        teams[turn[1]].append(f'-P{4 * i + 2}-')
        teams[turn[0]].append(f'-P{4 * i + 3}-')

        turn[0], turn[1] = turn[1], turn[0]

    return teams['A'], teams['B']


def check_element_in_list(e, e_list):
    return True if e in e_list else False


def add_player_first_empty_string(player, tab, window):
    for i in tab:
        if window[i].get_text() == '':
            window[i].update(text=player)
            break


def draft_values_to_lineup(draft_values, window):
    window['A'].update(value=draft_values['A'])
    window['B'].update(value=draft_values['B'])

    A, B = set_teams(draft_values)

    for i in range(16):
        window[f'-A{i + 1}-'].update(text=A[i])
        window[f'-B{i + 1}-'].update(text=B[i])


def extract_single_number(string):
    return re.findall(r'\d+', string)[0]


def swap_players(team, window):
    element = window.find_element_with_focus()

    actual_pos = extract_single_number(element.key)
    new_pos = element.get()

    actual_player = window[f'-{team}{actual_pos}-'].get_text()
    new_player = window[f'-{team}{new_pos}-'].get_text()

    window[f'-{team}{new_pos}-'].update(text=actual_player)
    window[f'-{team}{actual_pos}-'].update(text=new_player)

    element.update(actual_pos)


def swap_lineup(window):
    for i in range(1, 17):
        A_key = f'-A{i}-'
        A_value = window[A_key].get_text()
        B_key = f'-B{i}-'
        B_value = window[B_key].get_text()

        window[A_key].update(text=B_value)
        window[B_key].update(text=A_value)


def focus_next_element(window, elements_tab, direction=1):
    current_element_key = window.find_element_with_focus().key
    if current_element_key in elements_tab:
        next_focus = elements_tab.index(current_element_key) + direction
        if (direction > 0 and next_focus < len(elements_tab)) or (direction < 0 and next_focus > 0):
            window[elements_tab[next_focus]].set_focus(True)


def swap_players_button(pressed_buttons, window):
    actual_button = window[pressed_buttons[0]].get_text()
    new_button = window[pressed_buttons[1]].get_text()

    window[pressed_buttons[1]].update(text=actual_button)
    window[pressed_buttons[0]].update(text=new_button)


def input_team(key, color):
    return sg.Input(key=key,
                    size=(10, 1),
                    justification='center',
                    default_text='',
                    expand_x=True,
                    background_color=color,
                    text_color='#000000')


def set_draft_background_color(draft_number, player_order, colors):
    if draft_number == 0:
        return colors[0] if player_order in (0, 1) else colors[1]
    else:
        return colors[0] if ((draft_number % 2 == 0 and player_order in (1, 2)) or
                             (draft_number % 2 == 1 and player_order in (0, 3))) else colors[1]


def input_player(draft_number, player_order, colors):
    return sg.Input(size=(16, 1),
                    enable_events=True,
                    key=f'-P{4 * draft_number + player_order}-',
                    background_color=set_draft_background_color(draft_number, player_order, colors),
                    text_color='#000000',
                    expand_x=True)


def row_draft(i, colors):
    return [sg.Text(f'Draft {i + 1}', text_color='#000000'),
            input_player(i, 0, colors),
            input_player(i, 1, colors),
            input_player(i, 2, colors),
            input_player(i, 3, colors)]


def create_draft_layout(names, colors):
    teams = [sg.Text('Teams', text_color='#000000'),
             input_team('A', colors[0]),
             input_team('B', colors[1]),
             sg.Button(key='-SWAP-', button_text='First drafting team', button_color=colors[0])]

    draft_layout = [[sg.Text('Draft', justification='center', text_color='#000000', expand_x=True)],
                    teams,
                    row_draft(0, colors),
                    row_draft(1, colors),
                    row_draft(2, colors),
                    row_draft(3, colors),
                    row_draft(4, colors),
                    row_draft(5, colors),
                    row_draft(6, colors),
                    row_draft(7, colors),
                    [sg.Listbox(names, size=(20, 6), enable_events=True, key='-LIST-', font='18')],
                    [sg.Button('Random team'), sg.Button('Exit')]]

    return draft_layout


def teams(key, color):
    return sg.Text(key=key,
                   size=(10, 1),
                   justification='center',
                   text='',
                   expand_x=True,
                   background_color=color,
                   text_color='#000000')


def draft_player_number(team, n):
    return sg.Text(size=(2, 1),
                   enable_events=True,
                   key=f'-n{team}{n}-',
                   text=n,
                   # background_color = '#6fe88c' if n <= 11 else sg.DEFAULT_INPUT_ELEMENTS_COLOR,
                   text_color='#6fe88c' if n <= 11 else '#000000',
                   expand_x=True)


def draft_player_name(name, team, n):
    return sg.Button(button_text='',
                     size=(16, 1),
                     key=f'-{team}{n}-',
                     expand_x=True,
                     button_color=definitions.get_colors_button())


def row_players(i):
    return [draft_player_number('A', i),
            draft_player_name(i, 'A', i),
            draft_player_number('B', i),
            draft_player_name(i, 'B', i)]


def create_lineup_layout(colors, erase_player=False):
    teams_lineup = [teams('-LA-', colors[0]),
                    teams('-LB-', colors[1])]

    row_players_title = [sg.Text('Nº', justification='center', text_color='#000000'),
                         sg.Text('Players', justification='center', text_color='#000000', expand_x=True),
                         sg.Text('Nº', justification='center', text_color='#000000'),
                         sg.Text('Players', justification='center', text_color='#000000', expand_x=True)]

    top = [sg.Text('Lineup', justification='center', text_color='#000000', expand_x=True)]
    if erase_player:
        top += [sg.Button(key='-ERASE-', button_text='Erase a player')]

    lineup_layout = [top,
                     teams_lineup,
                     row_players_title,
                     row_players(1),
                     row_players(2),
                     row_players(3),
                     row_players(4),
                     row_players(5),
                     row_players(6),
                     row_players(7),
                     row_players(8),
                     row_players(9),
                     row_players(10),
                     row_players(11),
                     row_players(12),
                     row_players(13),
                     row_players(14),
                     row_players(15),
                     row_players(16)]

    return lineup_layout


def save_draft(window):
    saved_values = {'-A-': window['A'].get(), '-B-': window['B'].get()}

    for i in range(1, 17):
        saved_values[f'-A{i}-'] = window[f'-A{i}-'].get_text()
        saved_values[f'-B{i}-'] = window[f'-B{i}-'].get_text()

    save_json('lineup.json', saved_values)
    print('Saved')


def load_lineup_json(filename, window):
    lineup = load_json(filename)
    window['-LA-'].update(value=lineup['-A-'])
    window['-LB-'].update(value=lineup['-B-'])

    for i in range(1, 17):
        window[f'-A{i}-'].update(text=lineup[f'-A{i}-'])
        window[f'-B{i}-'].update(text=lineup[f'-B{i}-'])


def action_buttons(text, key):
    return sg.Button(button_text=text,
                     auto_size_button=True,
                     size=(16, 1),
                     font='Arial 12',
                     key=key)


def action_text(text):
    return sg.Text(text=text, font='Arial 16', size=(9, 1), pad=(0, 10))


def option_button(text, key, pad):
    return sg.Button(button_text=text,
                     size=(12, 1),
                     font='Arial 12',
                     pad=((0, pad), (0, 0)),
                     key=key)


def option_text(text):
    return sg.Text(text=text, font='Arial 16', auto_size_text=True, pad=((0, 10), (0, 0)))


def create_log_layout():
    pass_actions = [action_text('Pass'),
                    action_buttons('Standard pass', '-CSP-'),
                    action_buttons('High pass', '-CHP-'),
                    action_buttons('Long pass', '-CLP-'),
                    action_buttons('First-time pass', '-CFP-'),
                    action_buttons('Head pass', '-CHE-')]

    shot_actions = [action_text('Shot'),
                    action_buttons('Shot', '-CSH-'),
                    action_buttons('Snapshot', '-CSN-'),
                    action_buttons('Head shot', '-CHS-')]

    attacking_actions = [action_text('Attacker'),
                         action_buttons('Movement phase', '-CMP-'),
                         action_buttons('Dribble', '-CDR-'),
                         action_buttons('Nutmeg', '-CNU-'),
                         action_buttons('Control high pass', '-CCP-')]

    defending_actions = [action_text('Defender'),
                         action_buttons('Tackle', '-CTA-'),
                         action_buttons('Steal', '-CST-'),
                         action_buttons('Tackle from behind', '-CTB-'),
                         action_buttons('Reckless tackle', '-CRT-'),
                         action_buttons('Intercept pass', '-CIP-'),
                         action_buttons('Deflect shot', '-CDS-')]

    goalkeeper_actions = [action_text('Goalkeeper'),
                          action_buttons('Save ball', '-CSB-'),
                          action_buttons('Hold ball', '-CHB-'),
                          action_buttons('Dive at the feet', '-CDF-'),
                          action_buttons('Kick ball', '-CKB-'),
                          action_buttons('Drop ball', '-CDB-')]

    set_pieces = [action_text('Set pieces'),
                  action_buttons('Corner kick', '-CCK-'),
                  action_buttons('Throw-in', '-CTI-'),
                  action_buttons('Free kick', '-CFK-'),
                  action_buttons('Penalty', '-CPE-')]

    other_actions = [action_text('Other'),
                     action_buttons('Loose ball', '-CLB-'),
                     action_buttons('Pick up ball', '-CPB-'),
                     action_buttons('Heading challenge', '-CHC-')]

    options = [option_text('Agent'), option_button('Pick a player', 'Agent', 30),
               option_text('Recipient'), option_button('Pick a player', 'Recipient', 30),
               option_text('Result'), option_button('Success', 'Result', 70),
               option_button('Submit', 'Submit', 0)]

    multiline = [sg.Multiline(key='-LOG-',
                              size=(120, 10),
                              disabled=True,
                              autoscroll=True,
                              write_only=True)]

    layout = [attacking_actions,
              defending_actions,
              pass_actions,
              shot_actions,
              goalkeeper_actions,
              set_pieces,
              other_actions,
              [sg.Text('', pad=((0, 0), (10, 0)))],
              options,
              [sg.Text('', pad=((0, 0), (10, 0)))],
              multiline]

    return layout


def set_action_buttons_color(window, color_agent, color_recipient, color_result):
    window['Agent'].update(button_color=color_agent)
    window['Recipient'].update(button_color=color_recipient)
    window['Result'].update(button_color=color_result)


def update_button_text(button, text):
    button.update(text=text)


def update_action_buttons_color(window, event):
    colors = definitions.get_colors_options_buttons()

    if (event == '-CLP-') or (event == '-CSH-') or (event == '-CSN-') or (event == '-CCP-') or (
            event == '-CIP-') or (event == '-CDS-') or (event == '-CSB-') or (event == '-CKB-') or (
            event == '-CHB-'):
        set_action_buttons_color(window, colors[0], colors[2], colors[0])
        update_button_text(window['Result'], 'Success')

    elif (event == '-CHS-') or (event == '-CDB-') or (event == '-CPB-') or (
            event == '-CSP-') or (event == '-CFP-') or (event == '-CHE-'):
        set_action_buttons_color(window, colors[0], colors[2], colors[1])
        update_button_text(window['Result'], '')

    elif (event == '-CMP-') or (event == '-CLB-') or (event == '-CHC-') or (event == '-CCK-') or (
            event == '-CTI-') or (event == '-CFK-') or (event == '-CPE-'):
        set_action_buttons_color(window, colors[2], colors[2], colors[1])
        update_button_text(window['Result'], '')

    else:
        set_action_buttons_color(window, colors[0], colors[0], colors[0])
        update_button_text(window['Result'], 'Success')
