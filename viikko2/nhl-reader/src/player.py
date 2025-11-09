class Player:
    def __init__(self, _dict):
        self.name = _dict['name']
        self.nationality = _dict['nationality']
        self.team = _dict['team']
        self.goals = _dict['goals']
        self.assists = _dict['assists']

    def get_player(self):
        return f"{self.name, self.nationality, self.team, self.goals, self.assists}"

    def __str__(self):
        return self.get_player()
