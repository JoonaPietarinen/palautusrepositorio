import requests
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    #print("JSON-muotoinen vastaus:")
    #print(response)

    players = []

    for player_dict in response:
        player = Player(player_dict)
        if player.nationality == 'FIN':
                players.append(player)

    players.sort(key=lambda p: p.goals + p.assists, reverse=True)

    print("Oliot:")

    for player in players:
        print(f"{player.name:20}", f"{player.team:20}", player.goals, "+", player.assists, "=", player.goals + player.assists)

if __name__ == "__main__":
    main()
