class Player:
    def __init__(self, name, key):
        self.name = name
        self.key = key


class Team:
    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.drafted_players = []

    def add_player(self, player):
        self.drafted_players.append(player)

