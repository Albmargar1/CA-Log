class ObjectWithStats:
    def __init__(self, name):
        self.name = name
        self.stats = {'Short passes': 0,
                      'Long passes': 0,
                      'Heads': 0,
                      'Shots': 0,
                      'Dribbles': 0,
                      'Tackles': 0,
                      'Interceptions': 0,
                      'Savings': 0,
                      'Fouls': 0,
                      'Yellow cards': 0,
                      'Red cards': 0,
                      }


class Player(ObjectWithStats):
    def __init__(self, name):
        super().__init__(name)


class Team(ObjectWithStats):
    def __init__(self, name):
        super().__init__(name)
        self.stats['Corners'] = 0
        self.stats['Throws-in'] = 0
        self.stats['Free kicks'] = 0
        self.stats['Penalties'] = 0
        self.stats['Possession'] = 0

