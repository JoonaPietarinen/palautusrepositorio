from statistics import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, All, Not, HasFewerThan, Or

class Build:
	def __init__(self):
		self.matcher = All()
	def build(self):
		return self.matcher

class PlaysInBuild(Build):
	def __init__(self, build, team):
		self.build_olio = build
		self.team = team
	def build(self):
		return And(self.build_olio.build(), PlaysIn(self.team))

class HasAtLeastBuild(Build):
	def __init__(self, build, value, attr):
		self.build_olio = build
		self.value = value
		self.attr = attr
	def build(self):
		return And(self.build_olio.build(), HasAtLeast(self.value, self.attr))

class HasFewerThanBuild(Build):
	def __init__(self, build, value, attr):
		self.build_olio = build
		self.value = value
		self.attr = attr
	def build(self):
		return And(self.build_olio.build(), HasFewerThan(self.value, self.attr))

class OrBuild(Build):
	def __init__(self, *matchers):
		self.matchers = matchers
	def build(self):
		resolved = []
		for m in self.matchers:
			if hasattr(m, "build") and callable(m.build):
				resolved.append(m.build())
			else:
				resolved.append(m)
		return Or(*resolved)

class NotBuild(Build):
	def __init__(self, matcher):
		self.matcher = matcher
	def build(self):
		return Not(self.matcher)

class AndBuild(Build):
	def __init__(self, *matchers):
		self.matchers = matchers
	def build(self):
		return And(*self.matchers)




class QueryBuilder:
	def __init__(self, build = Build()):
		self.build_olio = build

	def plays_in(self, team):
		return QueryBuilder(PlaysInBuild(self.build_olio, team))

	def has_at_least(self, value, attr):
		return QueryBuilder(HasAtLeastBuild(self.build_olio, value, attr))

	def has_fewer_than(self, value, attr):
		return QueryBuilder(HasFewerThanBuild(self.build_olio, value, attr))

	def one_of(self, *matchers):
		return QueryBuilder(OrBuild(*matchers))

	def not_(self, matcher):
		return QueryBuilder(NotBuild(matcher))

	def and_(self, *matchers):
		return QueryBuilder(AndBuild(*matchers))

	def build(self):
		return self.build_olio.build()