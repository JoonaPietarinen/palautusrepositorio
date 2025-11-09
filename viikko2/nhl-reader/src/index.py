from rich.console import Console
from rich.table import Table
from player_reader import PlayerReader
from player_stats import PlayerStats


def main():
    season = input("Season (ex. 2024-25): ")
    nationality = input("Nationality (ex. FIN): ")
    players = PlayerStats(PlayerReader(f"https://studies.cs.helsinki.fi/nhlstats/{season}/players")).top_scorers_by_nationality(nationality)
    ct(season, nationality, players)

def ct(season, nationality, players):
    table = Table(title=f"Season {season} players from {nationality}")
    table.add_column("Name", style="cyan")
    table.add_column("teams", style="magenta")
    table.add_column("goals", style="green", justify="right")
    table.add_column("assists", style="green", justify="right")
    table.add_column("points", style="green", justify="right")
    for player in players:
        points = player.goals + player.assists
        table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(points))
    Console().print(table)

if __name__ == "__main__":
    main()
