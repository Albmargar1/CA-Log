import PySimpleGUI as sg
import json
import re


def swap_colors(colors):
    return [colors[1], colors[0]]


def save_json(path, dic):
    json_string = json.dumps(dic)
    with open(path, 'w') as outfile:
        outfile.write(json_string)


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
            window[i].update(text = player)
            break



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


def swap_lineup(window):
    for i in range(1,17):
        A_key = f'-A{i}-'
        A_value = window[A_key].get_text()
        B_key = f'-B{i}-'
        B_value = window[B_key].get_text() 

        window[A_key].update(text = B_value)
        window[B_key].update(text = A_value)


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



