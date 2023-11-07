from problemdomain.Position import Position
from problemdomain.pieces.Piece import Piece
from problemdomain.Player import Player


class Bishop(Piece):
	def __init__(self, player: Player):
		super().__init__(player)

	def getReachablePositions(self, position: Position, matrix_board: list[list[Position]]) -> list[Position]:
		pass



