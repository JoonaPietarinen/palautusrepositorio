from player_reader import PlayerReader

class PlayerStats():
    def __init__(self, PR):
        reader = PR
        self.players = reader.get_players()
        #self.players.sort(key=lambda p: p.goals + p.assists, reverse=True)


        #for player in self.players:
            #player_stats = (f"{player.name:20}", f"{player.team:20}", player.goals, "+", player.assists, "=", player.goals + player.assists)
    
    def top_scorers_by_nationality(self, nationality):
        results = []
        self.players.sort(key=lambda p: p.goals + p.assists, reverse=True)
        for player in self.players:
            if player.nationality == nationality:
                results.append(player)
        return results

