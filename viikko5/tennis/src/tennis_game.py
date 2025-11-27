class TennisGame:
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3
    ADVANTAGE = 1
    WIN = 2

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_scores = 0
        self.player2_scores = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.player1_scores += 1
        else:
            self.player2_scores += 1

    def get_score(self):
        if self.player1_scores == self.player2_scores:
            return self.get_tied_score(self.player1_scores)
        elif self.player1_scores >= 4 or self.player2_scores >= 4:
            return self.match_point()
        else:
            return self.current_scores()

    def get_tied_score(self, player_score):
            if player_score == self.LOVE:
                return "Love-All"
            elif player_score == self.FIFTEEN:
                return "Fifteen-All"
            elif player_score == self.THIRTY:
                return "Thirty-All"
            else:
                return "Deuce"

    def match_point(self):
        score_difference = self.player1_scores - self.player2_scores
        if -self.ADVANTAGE <= score_difference <= self.ADVANTAGE:
            leading_player = self.player1_name if score_difference > 0 else self.player2_name
            return "Advantage " + leading_player
        leading_player = self.player1_name if score_difference > 0 else self.player2_name
        return "Win for " + leading_player

    def score_name(self, score):
        if score == self.LOVE:
            return "Love"
        if score == self.FIFTEEN:
            return "Fifteen"
        if score == self.THIRTY:
            return "Thirty"
        if score == self.FORTY:
            return "Forty"
        raise ValueError(f"Invalid score value: {score}")
    def current_scores(self):
        return f"{self.score_name(self.player1_scores)}-{self.score_name(self.player2_scores)}"
