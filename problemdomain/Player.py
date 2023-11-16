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
        curr_destiny = desnity
        check_on_last_three_moves = True

        for move in self._last_three_moves[::-1]:
            prev_check = move.getCheck()
            prev_origin = move.getOrigin()

            if prev_origin == curr_destiny and prev_check:
                curr_destiny = prev_origin
            else:
                check_on_last_three_moves = False
                break
        
        return check_on_last_three_moves

    def getPiece(self) -> Piece:
        return self._select_piece

    def getColor(self) -> Color:
        return self._color

    def getTurn(self) -> bool:
        return self._turn

    def setTurn(self, turn: bool):
        self._turn = turn

    def getMoves(self) -> list[Move]:
        return self._last_three_moves

    def setPiece(self, piece: Piece):
        self._select_piece = piece

    def setMove(self, move: Move):
        if len(self._last_three_moves) >= 3:
            self._last_three_moves.pop(0)
        self._last_three_moves.append(move)
