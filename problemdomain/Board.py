from problemdomain.Player import Player
from problemdomain.pieces import *
from problemdomain.Position import Position
from problemdomain.Color import Color
from problemdomain.Move import Move

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
        self._match_in_progress = False
        self._player_interface.addToBatch({"type": "game_over", "match_status": "finished"})
        

    def startMatch(self, local_player: str, remote_player: str, local_color: str):
        local_color = Color[local_color]
        local_turn = local_color == Color.RED

        remote_color = Color.RED if local_color == Color.BLACK else Color.BLACK

        self._local_player = Player(local_player, local_turn, local_color)
        self._remote_player = Player(remote_player, not local_turn, remote_color)
        self._match_in_progress = True
        self._positions = self.initialize_position_matrix()

    def setWinner(self, player: Player):
        self._winner = player

    def evaluateMatchFinish(self) -> bool:
        draw = self.verifyDraw()

        if draw:
            self.setWinner(None)
            self._player_interface.showMessage('OCORREU EMPATE')
            self.finishMatch()

        else:
            winner = self.verifyWinner()

            if winner:
                winner_player = self._local_player if self._local_player.getTurn() == True else self._remote_player
                self.setWinner(winner_player)
                self._player_interface.showMessage(f'O {winner_player.getColor().name} VENCEU!!')
                self.finishMatch()

        return draw or winner

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

        if self._match_in_progress:
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

        origin: tuple[int, int] = move['origin']
        destiny: tuple[int, int] = move['destiny']
        print(f"Movendo peça de {origin} para {destiny}")

        piece = self._positions[origin[0]][origin[1]].getPiece()
        player = piece.getPlayer()
        other_player = self._local_player if player == self._remote_player else self._remote_player
        attacked = self.getAttackedPieces(origin)
        move = Move(self._positions[origin[0]][origin[1]], self._positions[destiny[0]][destiny[1]], self.verifyCheck(other_player), attacked)
        player.setMove(move)

        self.__placePiece(origin, destiny)
        self._local_player.setPiece(None)
        self._player_interface.updateInterfaceMove(origin, destiny)
        self.evaluateMatchFinish()
        self.changeTurn()
        self._player_interface.sendBatch()

    def receiveMove(self, move: dict):
        pass

    def getMatchInProgress(self) -> bool:
        return self._match_in_progress

    # Métodos relacionados às peças e posições
    def calculatePossiblePositions(self, piece: Piece, verify_check: bool, verify_protected: bool) -> list[Position]:
        origin = self.getPiecePosition(piece)
        posible_reachable_position = piece.getReachablePositions(origin, self._positions)
        player = piece.getPlayer()

        reachable_positions = []

        if verify_check and verify_protected:
            print(f"Peça selecionada: {type(piece)}\nDestinos: \n")
        
        for destiny in posible_reachable_position:
            coord_destiny = destiny.getCoordenates()

            occupied = self.verifyPositionOccupiedByPlayer(destiny, player)
            protected = None
            visible = None
            consecutive_check = None
            check = None

            if not occupied: 
                protected = self.verifyPieceThreat(destiny, piece) if verify_protected else False
                if not verify_protected or not protected:
                    other_piece = destiny.getPiece()
                    origin.setPiece(None)
                    destiny.setPiece(piece)
                    
                    consecutive_check = self.verifyConsecutiveChecks(destiny, piece) if verify_check else False
                    if not verify_check or not consecutive_check:
                        visible = self.verifyVisibleKings()
                        if not visible:
                            check = self.verifyCheck(player) if verify_check else False
                            if not verify_check or not check:
                                reachable_positions.append(destiny)
                            
                    origin.setPiece(piece)
                    destiny.setPiece(other_piece)

            if verify_check and verify_protected:
                print(f"Posição: {coord_destiny}")
                print(f"Occupied: {occupied}\nprotected: {protected}\nconsecutive_check: {consecutive_check}\nvisible: {visible}\ncheck: {check}\n")

        if verify_check and verify_protected:    
            print("="*30 + '\n')
        
        return reachable_positions

    def __movePiece(self, piece: Piece, destiny: Position):
        valid = piece.verifyValidPosition(destiny)

        if valid:
            origin = self.getPiecePosition(piece)

            cord_origin = origin.getCoordenates()
            cord_destiny = destiny.getCoordenates()

            self._player_interface.addToBatch({"type": "move", "origin": cord_origin,
                                             'destiny': cord_destiny, "match_status": "next"})
            self.makeMove({'origin': cord_origin, 'destiny': cord_destiny})

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
        pieces = []
        for line in self._positions:
            for pos in line:
                if pos.getPiece():
                    pieces.append(pos.getPiece())
        return pieces


    def getPlayerPieces(self, player: Player) -> list[Piece]:
        pieces = []
        for line in self._positions:
            for pos in line:
                if pos.getPiece() and pos.getPiece().getPlayer() == player:
                    pieces.append(pos.getPiece())
        return pieces

    def getAttackedPieces(self, coordinates: tuple[int, int]) -> list[Piece]:
        i, j = coordinates
        pos = self._positions[i][j]
        piece = pos.getPiece()

        if not piece:
            return []
        
        attacked = []
        for pos in self.calculatePossiblePositions(piece, True, True):
            if pos.getPiece():
                attacked.append(pos.getPiece())
        return attacked

    def getPiecePosition(self, piece: Piece) -> Position:
        for i in range(10):
            for j in range(9):
                curr_piece = self._positions[i][j].getPiece()
                if curr_piece == piece:
                    return self._positions[i][j]

    # Métodos de verificação
    def verifyCheck(self, player: Player) -> bool:
        king_pos = None
        for line in (0, 1, 2, 7, 8, 9):
            for column in range(3, 6):
                pos = self._positions[line][column]
                piece = pos.getPiece()

                if isinstance(piece, King):
                    piece_player = piece.getPlayer()
                    if piece_player == player:
                        king_pos = pos
                        break
        
        opponent_pieces = None
        if player == self._local_player:
            opponent_pieces = self.getPlayerPieces(self._remote_player)
        else:
            opponent_pieces = self.getPlayerPieces(self._local_player)
        
        for piece in opponent_pieces:
            posible_positions = self.calculatePossiblePositions(piece, False, False)
            for pos in posible_positions:
                if king_pos == pos:
                    print(f"Check!!!\nPiece: {type(piece)}\nPiece pos: {self.getPiecePosition(piece).getCoordenates()}\nKing pos: {king_pos.getCoordenates()}\nReachable positions: {[p.getCoordenates() for p in posible_positions]}")
                    return True
        
        return False


    def verifyDraw(self) -> bool:
        for piece in self.getAllPieces():
            if isinstance(piece, (Cannon, Horse, Rook, Pawn)):
                return False
        return True

    def verifyWinner(self) -> bool:
        player_not_in_turn = self._local_player if not self._local_player.getTurn() else self._remote_player

        if all(len(self.calculatePossiblePositions(piece, True, False)) == 0 for piece in self.getPlayerPieces(player_not_in_turn)):
            return True
        return False

    def verifyPositionOccupiedByPlayer(self, destiny: Position, player: Player) -> bool:
        other_piece = destiny.getPiece()
        other_player = other_piece.getPlayer() if other_piece else None
        return player == other_player


    def verifyConsecutiveChecks(self, destiny: Position, piece: Piece) -> bool:
        player = piece.getPlayer()
        other_player = self._local_player if player != self._local_player else self._remote_player
        other_check = self.verifyCheck(other_player)
        consecutive_checks = player.verifyCheckOnLastThreeMoves(destiny)

        return other_check and consecutive_checks

    def verifyPieceThreat(self, destiny: Position, piece: Piece) -> bool:
        player = piece.getPlayer()
        if not len(player.getMoves()):
            return False
        
        protected = self.verifyIfPositionIsProtected(destiny, player)

        attacked_piece = destiny.getPiece()
        last_move = player.getMoves()[-1]
        
        last_move_attacked_pieces = last_move.getAttackedPiecies()
        last_move_origin = last_move.getOrigin()

        return protected and attacked_piece in last_move_attacked_pieces and destiny.getCoordenates() == last_move_origin.getCoordenates()

    def verifyIfPositionIsProtected(self, pos: Position, player: Player) -> bool:
        other_player = self._local_player if self._local_player != player else self._remote_player
        pieces = self.getPlayerPieces(other_player)

        protected = False
        for piece in pieces:
            reachable_positions = self.calculatePossiblePositions(piece, True, False)

            if pos in reachable_positions:
                protected = True
                break
        
        return protected


    def verifyVisibleKings(self) -> bool:
        for line in range(0, 3):
            for column in range(3, 6):
                pos = self._positions[line][column]
                piece = pos.getPiece()

                if isinstance(piece, King):
                    for line_to_view in range(line+1, 10):
                        pos_to_view = self._positions[line_to_view][column]
                        piece_to_view = pos_to_view.getPiece()

                        if isinstance(piece_to_view, King):
                            return True
                        if piece_to_view and not isinstance(piece_to_view, King):
                            return False
        return False
