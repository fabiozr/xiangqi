from problemdomain.pieces.Piece import Piece
from problemdomain.Color import Color
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from problemdomain.Player import Player
    from problemdomain.Position import Position

class Elephant(Piece):
    def __init__(self, player: "Player"):
        super().__init__(player)

    def getReachablePositions(
        self, position: "Position", matrix_board: list[list["Position"]]
    ) -> list["Position"]:
        reachable_positions = []
        x, y = position.getCoordenates()
        color = self._player.getColor()
        orthogonal_coords = [(x + ox, y + oy) for ox, oy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]]
        possible_coords = [(x+dx, y+dy) for dx, dy in [(2, 2), (2, -2), (-2, 2), (-2, -2)]]

        for i in range(len(possible_coords)):
            x, y = possible_coords[i]
            ox, oy = orthogonal_coords[i]

            condition = 0 <= x < 10 and 0 <= y < 9 and color == matrix_board[x][y].getColor() \
                        and matrix_board[ox][oy].getPiece() == None

            if condition:
                reachable_positions.append(matrix_board[x][y])

        return reachable_positions

