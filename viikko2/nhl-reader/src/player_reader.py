import requests
from player import Player

class PlayerReader():
    def __init__(self, url):
        self.url = url
    def get_players(self):
        response = requests.get(self.url, timeout=25).json()
        players = []
        for player_dict in response:
            player = Player(player_dict)
            players.append(player)
        return players

    def __str__(self):
        return f"{self.get_players()}"
