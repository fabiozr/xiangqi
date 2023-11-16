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
        positions = [[None] * 9 for _ in range(10)]
        red_player = self._local_player if self._local_player.getColor() == Color.RED else self._remote_player
        black_player = self._local_player if red_player == self._remote_player else self._remote_player

        if self._local_player == black_player:
            self.setPieces(positions, Color.RED, Color.BLACK, red_player, black_player)
        else:
            self.setPieces(positions, Color.BLACK, Color.RED, black_player, red_player)

        return positions

    def setPieces(self, positions: list[list], color1: Color, color2: Color, player1: Player, player2: Player):
        for row in range(5):
            for column in range(9):
                positions[row][column] = Position(color1, None, (row, column))

        for row in range(5, 10):
            for column in range(9):
                positions[row][column] = Position(color2, None, (row, column))

        # Preenchendo as posições com peças
        positions[0][0] = Position(color1, Rook(player1), (0, 0))
        positions[0][1] = Position(color1, Horse(player1), (0, 1))
        positions[0][2] = Position(color1, Elephant(player1), (0, 2))
        positions[0][3] = Position(color1, Guard(player1), (0, 3))
        positions[0][4] = Position(color1, King(player1), (0, 4))
        positions[0][5] = Position(color1, Guard(player1), (0, 5))
        positions[0][6] = Position(color1, Elephant(player1), (0, 6))
        positions[0][7] = Position(color1, Horse(player1), (0, 7))
        positions[0][8] = Position(color1, Rook(player1), (0, 8))

        positions[3][0] = Position(color1, Pawn(player1), (3, 0))
        positions[3][2] = Position(color1, Pawn(player1), (3, 2))
        positions[3][4] = Position(color1, Pawn(player1), (3, 4))
        positions[3][6] = Position(color1, Pawn(player1), (3, 6))
        positions[3][8] = Position(color1, Pawn(player1), (3, 8))

        positions[2][1] = Position(color1, Cannon(player1), (2, 1))
        positions[2][7] = Position(color1, Cannon(player1), (2, 7))

        # Preenchendo as posições com peças
        positions[9][0] = Position(color2, Rook(player2), (9, 0))
        positions[9][1] = Position(color2, Horse(player2), (9, 1))
        positions[9][2] = Position(color2, Elephant(player2), (9, 2))
        positions[9][3] = Position(color2, Guard(player2), (9, 3))
        positions[9][4] = Position(color2, King(player2), (9, 4))
        positions[9][5] = Position(color2, Guard(player2), (9, 5))
        positions[9][6] = Position(color2, Elephant(player2), (9, 6))
        positions[9][7] = Position(color2, Horse(player2), (9, 7))
        positions[9][8] = Position(color2, Rook(player2), (9, 8))

        positions[6][0] = Position(color2, Pawn(player2), (6, 0))
        positions[6][2] = Position(color2, Pawn(player2), (6, 2))
        positions[6][4] = Position(color2, Pawn(player2), (6, 4))
        positions[6][6] = Position(color2, Pawn(player2), (6, 6))
        positions[6][8] = Position(color2, Pawn(player2), (6, 8))

        positions[7][1] = Position(color2, Cannon(player2), (7, 1))
        positions[7][7] = Position(color2, Cannon(player2), (7, 7))

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
        if self._local_player.getTurn() == True:
            self._local_player.setTurn(False)
            self._remote_player.setTurn(True)
        else:
            self._local_player.setTurn(True)
            self._remote_player.setTurn(False)

    def selectPosition(self, line: int, column: int):
        position = self.__getPosition(line - 1, column - 1)
        local_turn = self._local_player.getTurn()

        if local_turn:
            piece = position.getPiece()

            if piece != None:
                player = piece.getPlayer()

                if player != self._local_player:
                    piece_selected = self._local_player.getPiece()

                    if piece_selected != None:
                        print('Mover peça')
                        self.__movePiece(piece_selected, position)
                else:
                    print('Selecionar peça')
                    self.__selectPiece(piece)
            else:
                piece_selected = self._local_player.getPiece()

                if piece_selected != None:
                    print('Mover peça')
                    self.__movePiece(piece_selected, position)

    def makeMove(self, move: dict):

        origin = move['origin']
        destiny = move['destiny']

        self.__placePiece(origin, destiny)
        self._local_player.setPiece(None)
        self._player_interface.updateInterfaceMove(origin, destiny)
        self.changeTurn()

    def receiveMove(self, move: dict):
        pass

    def getMatchInProgress(self) -> bool:
        return self._match_in_progress

    # Métodos relacionados às peças e posições
    def calculatePossiblePositions(self, piece: Piece, verify_check: bool, verify_protected: bool) -> list[Position]:
        origin = self.getPiecePosition(piece)
        return piece.getReachablePositions(origin, self._positions)

    def __movePiece(self, piece: Piece, destiny: Position):
        valid = piece.verifyValidPosition(destiny)

        if valid:
            origin = self.getPiecePosition(piece)

            cord_origin = origin.getCoordenates()
            cord_destiny = destiny.getCoordenates()

            self.makeMove({'origin': cord_origin, 'destiny': cord_destiny})
            self._player_interface.sendMove({'origin': cord_origin, 'destiny': cord_destiny})

    def __selectPiece(self, piece: Piece):
        self._local_player.setPiece(piece)
        possible_positions = self.calculatePossiblePositions(piece, True, True)

        piece.setPossiblePosition(possible_positions)

        cords = [pos.getCoordenates() for pos in possible_positions]
        self._player_interface.showValidPositions(cords)

    def __placePiece(self, origin: tuple, destiny: tuple):
        self._positions[destiny[0]][destiny[1]].setPiece(self._positions[origin[0]][origin[1]].getPiece())
        self._positions[origin[0]][origin[1]].setPiece(None)

    def __getPosition(self, line: int, column: int) -> Position:
        return self._positions[line][column]

    def getAllPieces(self) -> list[Piece]:
        pass

    def getPlayerPieces(self, player: Player) -> list[Piece]:
        pass

    def getAttackedPieces(self, coordinates: tuple) -> list[Piece]:
        pass

    def getPiecePosition(self, piece: Piece) -> Position:
        for i in range(10):
            for j in range(9):
                curr_piece = self._positions[i][j].getPiece()
                if curr_piece == piece:
                    return self._positions[i][j]

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
