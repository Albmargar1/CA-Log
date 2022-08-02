##########
# KEYS
# Team draft 'A' or 'B'
# Team lineup '-LA-' or '-LB-'
# Player draft '-P0-', ..., '-P31-'
# Player nº lineup '-nA0-', ..., '-nB16-'
# Player team '-A0-', ..., '-B16-'

def get_players():
    names = ['Abraham', 'Aguayo', 'Allou', 'Andersen', 'André Noruega',
             'Attah', 'Aziz', 'Baas', 'Baez', 'Bank', 'Barisic',
             'Bertans', 'Bosic', 'Bratoz', 'Buzek', 'Byrne',
             'Cafferata', 'Chapman', 'Chova', 'Cuzman', 'Delgado',
             'Delpech', 'Denier', 'Diogu', 'Dionte', 'Doxakis',
             'Ekström', 'Eubsinho', 'Ezzine', 'Faye', 'Ferraro',
             'Firrell', 'Foyle', 'Fruin', 'Gaham', 'Gilbert',
             'Goalev', 'Gortz', 'Gowman', 'Hardy', 'Horna', 'Hrstkova',
             'Humphrey', 'Iwu', 'Jansen', 'Jung', 'K. Ozcan', 'Kalla',
             'Kanaras', 'Kerr', 'Kucklick', 'Kuzmic', 'Kuzmina',
             'Langdon', 'Lessa', 'Littlewood', 'Longo', 'López',
             'Manolis', 'Marell', 'Mbenga', 'McNulty', 'Meloni',
             'Mikhailov', 'Mitchell', 'Mooney', 'Moriuchi', 'Muirhead',
             'Murphy', 'Nazef', 'Nilsson', 'Nkosi', 'Noon', 'O\'Connor',
             'Orresta', 'Patras', 'Patterson', 'Pavlovic', 'Petersen',
             'Polyakov', 'Poulsen', 'Ribeiro', 'Robbie', 'Ruiz', 'Rupnik',
             'Rusu', 'Sang', 'Savvakis', 'Sesay', 'Siami', 'Soares',
             'Spearman', 'Stewart', 'Taylor', 'Terto', 'Toothnail',
             'Ulisses', 'Van de Kerkhof', 'Vladoiu', 'Volkova',
             'Vrabec', 'Walker', 'Walton', 'Werdekker', 'Willemns',
             'Wilson', 'Yaneva', 'Yugar', 'Zhao', 'Zimmer']

    return names


def get_draft_key_tab():
    tab_list = ['A', 'B']
    for i in range(32):
        tab_list.append(f'-P{i}-')

    return tab_list


def get_lineup_key_tab(team):
    tab_list = [f'-{team}{i}-' for i in range(1,17)]
    return tab_list


def get_colors():
    return ['#7aa7f0', '#f07a92']


def get_colors_button():
    return ('#000000', '#FFFFFF')


def get_colors_options_buttons():
    return ('#348ceb', '#65f077', '#eb4c34')






