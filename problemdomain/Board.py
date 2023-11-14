from problemdomain.Player import Player
from problemdomain.pieces import *
from problemdomain.Position import Position
from problemdomain.Color import Color

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player_interface import PlayerInterface

class Board:
    _local_player: Player
    _remote_player: Player
    _positions: list[list[Position]]
    _match_in_progress: bool
    _winner: Player
    _player_interface: "PlayerInterface"

    def __init__(self, player_interface: "PlayerInterface"):
        self._local_player = None
        self._remote_player = None
        self._positions = None
        self._match_in_progress = False
        self._winner = None
        self._player_interface = player_interface

    # Métodos relacionados ao jogo
    def initialize_position_matrix(self) -> list[list[Position]]:
        red_player = self._local_player if self._local_player.getColor() == Color.RED else self._remote_player
        black_player = self._local_player if red_player == self._remote_player else self._remote_player

        return [
            [Rook(black_player), Horse(black_player), Bishop(black_player), Guard(black_player), King(black_player), Guard(black_player), Bishop(black_player), Horse(black_player), Rook(black_player)],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, Cannon(black_player), 0, 0, 0, 0, 0, Cannon(black_player), 0],
            [Pawn(black_player), 0, Pawn(black_player), 0, Pawn(black_player), 0, Pawn(black_player), 0, Pawn(black_player)],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [Pawn(red_player), 0, Pawn(red_player), 0, Pawn(red_player), 0, Pawn(red_player), 0, Pawn(red_player)],
            [0, Cannon(red_player), 0, 0, 0, 0, 0, Cannon(red_player), 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [Rook(red_player), Horse(red_player), Bishop(red_player), Guard(red_player), King(red_player), Guard(red_player), Bishop(red_player), Horse(red_player), Rook(red_player)],
        ]

    def finishMatch(self):
        pass

    def startMatch(self, local_player: str, remote_player: str, local_color: str):
        local_color = Color[local_color]
        local_turn = local_color == Color.RED

        remote_color = Color.RED if local_color == Color.BLACK else Color.BLACK

        self._local_player = Player(local_player, local_turn, local_color)
        self._remote_player = Player(remote_player, not local_turn, remote_color)

        self._positions = self.initialize_position_matrix()
        

    def setWinner(self, player: Player):
        pass

    def evaluateMatchFinish(self) -> bool:
        pass

    def changeTurn(self):
        pass

    def selectPosition(self, line: int, column: int):
        pass

    def makeMove(self, move: dict):
        pass

    def receiveMove(self, move: dict):
        pass

    def getMatchInProgress(self) -> bool:
        pass

    # Métodos relacionados às peças e posições
    def calculatePossiblePositions(self, piece: Piece, verify_check: bool, verify_protected: bool) -> list[Position]:
        pass

    def __movePiece(self, piece: Piece, destiny: Position):
        pass

    def __selectPiece(self, piece: Piece):
        pass

    def __placePiece(self, origin: tuple, destiny: tuple):
        pass

    def __getPosition(self, line: int, column: int) -> Position:
        pass

    def getAllPieces(self) -> list[Piece]:
        pass

    def getPlayerPieces(self, player: Player) -> list[Piece]:
        pass

    def getAttackedPieces(self, coordinates: tuple) -> list[Piece]:
        pass

    def getPiecePosition(self, piece: Piece) -> Position:
        pass

    # Métodos de verificação
    def verifyCheck(self, player: Player) -> bool:
        pass

    def verifyDraw(self) -> bool:
        pass

    def verifyWinner(self) -> bool:
        pass

    def verifyPositionOccupiedByPlayer(self, destiny: Position, player: Player) -> bool:
        pass

    def verifyConsecutiveChecks(self, destiny: Position, piece: Piece) -> bool:
        pass

    def verifyPieceThreat(self, destiny: Position, piece: Piece) -> bool:
        pass

    def verifyIfPositionIsProtected(self, pos: Position, player: Player) -> bool:
        pass

    def verifyVisibleKings(self) -> bool:
        pass
