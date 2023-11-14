from problemdomain.pieces.Piece import Piece
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from problemdomain.Player import Player
    from problemdomain.Position import Position

class King(Piece):
    def __init__(self, player: "Player"):
        super().__init__(player)

    def getReachablePositions(
        self, position: "Position", matrix_board: list[list["Position"]]
    ) -> list["Position"]:
        pass
