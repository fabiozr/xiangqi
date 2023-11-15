from problemdomain.pieces.Piece import Piece
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from problemdomain.Player import Player
    from problemdomain.Position import Position

class Pawn(Piece):
    def __init__(self, player: "Player"):
        super().__init__(player)

    def getReachablePositions(
        self, position: "Position", matrix_board: list[list["Position"]]
    ) -> list["Position"]:
        reachable_positions = []
        x, y = position.getCoordenates()
        possible_coords = [(x + dx, y + dy) for dx, dy in [(0, -1), (-1, 0), (0, 1)]] if x <= 4 else [(x-1, y)]


        for x, y in possible_coords:
            condition = 0 <= x < 10 and 0 <= y < 9

            if condition:
                reachable_positions.append(matrix_board[x][y])

        return reachable_positions
