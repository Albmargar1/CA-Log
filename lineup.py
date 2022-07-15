import PySimpleGUI as sg
import functions
import definitions


def teams(key, color):
    return sg.Text(key=key,
                   size=(10, 1),
                   justification='center',
                   text='',
                   expand_x=True,
                   background_color=color,
                   text_color = '#000000')


def draft_player_number(team, n):
    return sg.Text(size=(2, 1),
                   enable_events=True,
                   key=f'-n{team}{n}-',
                   text= n,
                   #background_color = '#6fe88c' if n <= 11 else sg.DEFAULT_INPUT_ELEMENTS_COLOR,
                   text_color = '#6fe88c' if n <= 11 else '#000000',
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


def create_lineup_layout(colors):
    teams_lineup = [teams('-LA-', colors[0]),
                    teams('-LB-', colors[1])]

    row_players_title = [sg.Text('Nº', justification='center', text_color = '#000000'),
                         sg.Text('Players', justification='center', text_color = '#000000', expand_x=True),
                         sg.Text('Nº', justification='center', text_color = '#000000'),
                         sg.Text('Players', justification='center', text_color = '#000000', expand_x=True)]

    lineup_layout = [[sg.Text('Lineup', justification='center', text_color = '#000000', expand_x=True)],
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
