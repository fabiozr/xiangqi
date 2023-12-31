
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from problemdomain.Player import Player
    from problemdomain.Position import Position

class Piece:
    _player: "Player"
    _possible_moves: list["Position"]

    def __init__(self, player: "Player"):
        self._player = player
        self._possible_moves = None

    def verifyValidPosition(self, position: "Position") -> bool:
        return position in self._possible_moves

    def getPlayer(self) -> "Player":
        return self._player

    def getReachablePositions(
        self, position: "Position", matrix_board: list[list]
    ) -> list["Position"]:
        pass

    def setPossiblePosition(self, positions: list["Position"]):
        self._possible_moves = positions
