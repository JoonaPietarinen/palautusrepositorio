class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def build(self, player):
        for matcher in self._matchers:
            if not matcher.build(player):
                return False

        return True


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def build(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def build(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value

class All:
    def build(self, player):
        return player == player
        
class Not:
    def __init__(self, matcher):
        self._matcher = matcher

    def build(self, player):
        return not self._matcher.build(player)

        
class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def build(self, player):
        player_value = getattr(player, self._attr)

        return player_value < self._value

class Or:
    def __init__(self, *matchers):
        self._matchers = matchers

    def build(self, player):
        for matcher in self._matchers:
            if matcher.build(player):
                return True
        return False

