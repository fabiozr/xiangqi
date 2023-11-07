from problemdomain.Player import Player
from player_interface import PlayerInterface
from problemdomain.pieces.Piece import Piece
from problemdomain.Position import Position

class Board:
	def __init__(self, local_player: Player, remote_player: Player, player_interface: PlayerInterface):
		self._local_player = local_player
		self._remote_player = remote_player
		self._positions = [[]]
		self._match_in_progress = False
		self._winner = None
		self._player_interface = player_interface

	# Métodos relacionados ao jogo
	def initialize_position_matrix(self) -> list[list]:
		pass

	def finishMatch(self):
		pass

	def startMatch(self, local_player: str, remote_player: str):
		pass

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
