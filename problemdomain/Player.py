from problemdomain.Color import Color
from problemdomain.pieces.Piece import Piece
from problemdomain.Move import Move
from problemdomain.Position import Position


class Player:
    _id: int
    _turn: bool
    _color: Color
    _last_three_moves: list[Move]
    _select_piece: Piece

    def __init__(self, id: int, turn: bool, color: Color):
        self._id = id
        self._turn = turn
        self._color = color
        self._last_three_moves = []
        self._select_piece = None

    def verifyCheckOnLastThreeMoves(self, desnity: Position) -> bool:
        pass

    def getPiece(self) -> Piece:
        return self._select_piece

    def getColor(self) -> Color:
        return self._color

    def getTurn(self) -> bool:
        return self._turn

    def getMoves(self) -> list[Move]:
        return self._last_three_moves

    def setPiece(self, piece: Piece):
        self._select_piece = piece

    def setMove(self, move: Move):
        if len(self._last_three_moves) >= 3:
            self._last_three_moves.pop(0)
        self._last_three_moves.append(move)
