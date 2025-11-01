from player_reader import PlayerReader
from enum import Enum

class SortBy(Enum):
    POINTS = 1
    GOALS = 2
    ASSISTS = 3

class StatisticsService():
    def __init__(self, PR):
        reader = PR

        self._players = reader.get_players()

    def search(self, name):
        for player in self._players:
            if name in player.name:
                return player

        return None

    def team(self, team_name):
        players_of_team = filter(
            lambda player: player.team == team_name,
            self._players
        )

        return list(players_of_team)

    def top(self, how_many, sort_by=SortBy.POINTS):
        def POINTS(player): 
            return player.points
        
        def GOALS(player): 
            return player.goals
        
        def ASSISTS(player): 
            return player.assists
            
        key_funcs = {
            SortBy.POINTS: POINTS,
            SortBy.GOALS: GOALS,
            SortBy.ASSISTS: ASSISTS,
        }
        
        key_func = key_funcs.get(sort_by, lambda player: player.points)
        
        sorted_players = sorted(
            self._players,
            reverse=True,
            key = key_func

        )
        

        result = []
        i = 0
        while i <= how_many:
            result.append(sorted_players[i])
            i += 1

        return result
