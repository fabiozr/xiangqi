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
        # Quando é jogador local, diminui x em 1. Senão, incrementa x em 1.
        # O lado do jogador local começa de x = 9 para baixo.
        up = -1 if matrix_board[9][0].getColor() == self._player.getColor() else 1
        possible_coords = [(x + dx, y + dy) for dx, dy in [(0, -1), (up, 0), (0, 1)]] if position.getColor() != self.getPlayer().getColor()  else [(x-1, y)]

        for x, y in possible_coords:
            condition = 0 <= x < 10 and 0 <= y < 9

            if condition:
                reachable_positions.append(matrix_board[x][y])

        return reachable_positions
