from problemdomain.Position import Position
from problemdomain.pieces.Piece import Piece


class Move:
    _origin: Position
    _destiny: Position
    _check: bool
    _attacked_pieces: list[Piece]

    def __init__(
        self,
        origin: Position,
        destiny: Position,
        check: bool,
        attacked_pieces: list[Piece],
    ):
        self._origin = origin
        self._destiny = destiny
        self._check = check
        self._attacked_pieces = attacked_pieces

    def getAttackedPiecies(self) -> list[Piece]:
        return self._attacked_pieces

    def getOrigin(self) -> Position:
        return self._origin
    
    def getCheck(self) -> bool:
        return self._check
