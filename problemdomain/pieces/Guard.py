from problemdomain.pieces.Piece import Piece
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from problemdomain.Player import Player
    from problemdomain.Position import Position

class Guard(Piece):
    def __init__(self, player: "Player"):
        super().__init__(player)

    def getReachablePositions(
        self, position: "Position", matrix_board: list[list["Position"]]
    ) -> list["Position"]:
        reacheble_positions = []
        x, y = position.getCoordenates()
        possible_cords = [(x + dx, y + dy) for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]]

        for x, y in possible_cords:
            condition = 3 <= y <= 5 and (0 <= x <= 2 or 7 <= x <= 9)

            if condition:
                reacheble_positions.append(matrix_board[x][y])

        return reacheble_positions
