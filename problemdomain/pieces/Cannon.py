from problemdomain.pieces.Piece import Piece
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from problemdomain.Player import Player
    from problemdomain.Position import Position

class Cannon(Piece):
    def __init__(self, player: "Player"):
        super().__init__(player)

    def getReachablePositions(
        self, position: "Position", matrix_board: list[list["Position"]]
    ) -> list["Position"]:
        reachable_positions = []
        x, y = position.getCoordenates()
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for i in range(len(directions)):
            has_jumped = False

            for j in range(1, 10):
                new_x, new_y = x + j * directions[i][0], y + j * directions[i][1]
                condition = 0 <= new_x < 10 and 0 <= new_y < 9

                if condition:

                    condition = matrix_board[new_x][new_y].getPiece() != None

                    if condition and has_jumped:
                        reachable_positions.append(matrix_board[new_x][new_y])
                        break

                    if condition and not has_jumped:
                        has_jumped = True

                    if not has_jumped:
                        reachable_positions.append(matrix_board[new_x][new_y])

        return reachable_positions
