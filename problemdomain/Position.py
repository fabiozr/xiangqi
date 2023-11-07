from problemdomain.Color import Color
from problemdomain.pieces.Piece import Piece


class Position:
	def __init__(self, color: Color, piece: Piece, coordenates: tuple):
		self._color = color
		self._piece = piece
		self._coordenates = coordenates

	def getPiece(self) -> Piece:
		return self._piece

	def getCoordenates(self) -> tuple:
		return self._coordenates



