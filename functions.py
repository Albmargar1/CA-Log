import PySimpleGUI as sg
import json
import re

def swap_colors(colors):
    return [colors[1], colors[0]]


def set_background_color(draft_number, player_order, colors):
    if draft_number == 0:
        return colors[0] if player_order in (0, 1) else colors[1]
    else:
        return colors[0] if ((draft_number % 2 == 0 and player_order in (1, 2)) or
                             (draft_number % 2 == 1 and player_order in (0, 3))) else colors[1]


def input_player(draft_number, player_order, colors):
    return sg.Input(size=(16, 1),
                    enable_events=True,
                    key=f'-P{4 * draft_number + player_order}-',
                    background_color=set_background_color(draft_number, player_order, colors),
                    expand_x=True)


def input_team(key, color):
    return sg.Input(key=key,
                    size=(10, 1),
                    justification='center',
                    default_text='',
                    expand_x=True,
                    background_color=color)


def draft_team(key, color):
    return sg.Text(key=key,
                   size=(10, 1),
                   justification='center',
                   text='',
                   expand_x=True,
                   background_color=color)


def draft_player_number(team, n):
    return sg.Input(size=(2, 1),
                    enable_events=True,
                    key=f'-n{team}{n}-',
                    default_text= n,
                    background_color= '#6fe88c' if n <= 11 else sg.DEFAULT_INPUT_ELEMENTS_COLOR,
                    expand_x=True)


def draft_player_name(name, team, n):
    return sg.Button(button_text=name,
                     size=(16, 1),
                     key=f'-{team}{n}-',
                     expand_x=True,
                     button_color=('#000000', '#FFFFFF'))


def save_json(path, dic):
    json_string = json.dumps(dic)
    with open(path, 'w') as outfile:
        outfile.write(json_string)


def read_json(path):
    with open(path, 'r') as infile:
        data = json.load(infile)
    return data

def set_teams(draft_values):
    teams = {}
    teams['A'] = [draft_values['-P0-'], draft_values['-P1-']]
    teams['B'] = [draft_values['-P2-'], draft_values['-P3-']]

    turn = ['A', 'B'] if draft_values['First pick'] == 'A' else ['B', 'A']
    for i in range(1, 8):
        teams[turn[0]].append(draft_values[f'-P{4 * i + 0}-'])
        teams[turn[1]].append(draft_values[f'-P{4 * i + 1}-'])
        teams[turn[1]].append(draft_values[f'-P{4 * i + 2}-'])
        teams[turn[0]].append(draft_values[f'-P{4 * i + 3}-'])

        turn[0], turn[1] = turn[1], turn[0]

    return teams['A'], teams['B']



def draft_values_to_lineup(draft_values, window):
    window['A'].update(value = draft_values['A'])
    window['B'].update(value = draft_values['B'])

    A, B = set_teams(draft_values)

    for i in range(16):
        window[f'-A{i+1}-'].update(text=A[i])
        window[f'-B{i+1}-'].update(text=B[i])


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


def focus_next_element(window, elements_tab, direction=1):
    current_element_key = window.find_element_with_focus().key
    if current_element_key in elements_tab:
        next_focus = elements_tab.index(current_element_key) + direction
        if (direction > 0 and next_focus < len(elements_tab)) or (direction < 0 and next_focus > 0):
            window[elements_tab[next_focus]].set_focus(True)


def swap_players_button(pressed_buttons, window):
    actual_button = window[pressed_buttons[0]].get_text()
    new_button = window[pressed_buttons[1]].get_text()

    window[pressed_buttons[1]].update(text = actual_button)
    window[pressed_buttons[0]].update(text = new_button)

