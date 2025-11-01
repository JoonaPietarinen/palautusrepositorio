import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_print(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        
    def test_search(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        
        self.player = StatisticsService.search(
            self.stats, "Semenko"
        )
        
    def test_false_search(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.player = StatisticsService.search(
            self.stats, "Jaakko"
        )
       
    def test_team(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.team = StatisticsService.team(
            self.stats, "EDM"
        )
        
    def test_top(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.top = StatisticsService.top(
            self.stats, 3
        )
        
    def test_top_sort_goals(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.top = StatisticsService.top(
            self.stats, 3, SortBy.GOALS
        )
        
    def test_top_sort_assists(self):
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
        self.top = StatisticsService.top(
            self.stats, 4, SortBy.ASSISTS
        )