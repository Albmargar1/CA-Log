import PySimpleGUI as sg
import definitions
import random
import functions


def input_team(key, color):
    return sg.Input(key=key,
                    size=(10, 1),
                    justification='center',
                    default_text='',
                    expand_x=True,
                    background_color=color,
                    text_color = '#000000')


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
    return [sg.Text(f'Draft {i+1}', text_color = '#000000'),
            input_player(i, 0, colors),
            input_player(i, 1, colors),
            input_player(i, 2, colors),
            input_player(i, 3, colors)]


def create_draft_layout(names, colors):
    teams = [sg.Text('Teams', text_color = '#000000'),
             input_team('A', colors[0]),
             input_team('B', colors[1]),
             sg.Button(key='-SWAP-', button_text='First drafting team', button_color=colors[0])]

    draft_layout = [[sg.Text('Draft', justification='center', text_color = '#000000', expand_x=True)],
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
                    [sg.Button('Save'), sg.Button('Random team'), sg.Button('Exit')]]

    return draft_layout
