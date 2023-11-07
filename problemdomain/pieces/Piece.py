from problemdomain.Player import Player
from problemdomain.Position import Position


class Piece():
	def __init__(self, player: Player):
		self._player = player
		self._possible_moves = None

	def verifyValidPosition(self, position: Position) -> bool:
		return position in self._possible_moves

	def getPlayer(self) -> Player:
		return self._player

	def getReachablePositions(self, position: Position, matrix_board: list[list]) -> list[list]:
		pass

	def setPossiblePosition(self, positions:  list[list]):
		self._possible_moves = positions



