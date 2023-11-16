from problemdomain.Color import Color
from problemdomain.pieces.Piece import Piece

from typing import Optional
class Position:
    _color: Color
    _piece: Piece
    _coordenates: tuple[int, int]

    def __init__(self, color: Color, piece: Piece, coordenates: tuple[int, int]):
        self._color = color
        self._piece = piece
        self._coordenates = coordenates

    def getPiece(self) -> Optional[Piece]:
        return self._piece

    def setPiece(self, piece: Piece):
        self._piece = piece

    def getCoordenates(self) -> tuple:
        return self._coordenates
