class PlayerStats():
    def __init__(self, player_reader):
        reader = player_reader
        self.players = reader.get_players()
        #self.players.sort(key=lambda p: p.goals + p.assists, reverse=True)
        #for player in self.players:

    def top_scorers_by_nationality(self, nationality):
        results = []
        self.players.sort(key=lambda p: p.goals + p.assists, reverse=True)
        for player in self.players:
            if player.nationality == nationality:
                results.append(player)
        return results

    def get_stats(self):
        results = []
        self.players.sort(key=lambda p: p.goals + p.assists, reverse=True)
        for player in self.players:
            results.append(player)
        return results

    def __str__(self):
        return f"{self.get_stats()}"
