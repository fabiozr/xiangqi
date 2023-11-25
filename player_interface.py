from interface.game import GameInterface
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
from uuid import uuid4
from random import choice
from threading import Thread

from queue import Queue
from time import sleep, time
from problemdomain.Board import Board

class PlayerInterface(DogPlayerInterface):
    _game_interface: GameInterface
    _dog_server_interface: DogActor
    _board: Board
    __queue: Queue
    __batch_moves: list[dict[str, any]]


    def __init__(self):
        self._game_interface = GameInterface(self)
        self.__queue = Queue()

        # Estabelecer conexão
        self._dog_server_interface = DogActor()
        player_name = self.generatePlayerName()
        message = self._dog_server_interface.initialize(player_name, self)
        self._game_interface.showMessage(message)
        self.__batch_moves = []

        self._board = Board(self)
        
        if message == "Conectado a Dog Server":
            self._game_interface.run()
        

    def generatePlayerName(self) -> str:
        return str(uuid4())

    def start_match(self):
        if self._board.getMatchInProgress():
            self._game_interface.showMessage("PARTIDA EM ANDAMENTO")
            return

        begin = time()
        code = None
        message = None
        while time() - begin < 5:
            start_status = self._dog_server_interface.start_match(2)
            code = start_status.get_code()
            message = start_status.get_message()

            if code not in ('0', '1'):
                break
        
        if code in ('0', '1'):
            self._game_interface.showMessage(message)
        else:
            color = choice(["RED", "BLACK"])
            other_color = "RED" if color == "BLACK" else "BLACK"
            self._dog_server_interface.send_move({"type": "start", "value": other_color, "match_status": "next"})
            self.initializeMatch(start_status, color)



    def receive_start(self, start_status: StartStatus):
        begin = time()
        color = None
        while time() - begin < 60:
            self._dog_server_interface.proxy.match_status()

            try:
                color = self.__queue.get_nowait()
                break
            except:
                sleep(0.2)
                continue

        if color is None:
            self._game_interface.showMessage("Timeout!")
            return

        self.initializeMatch(start_status, color)


    def initializeMatch(self, start_status: StartStatus, color: str):
        local_player, remote_player = start_status.get_players()
        self._board.startMatch(local_player, remote_player, color)
        self._game_interface.initializeBoard()
        self._game_interface.setLocalColor(color)
        self._game_interface.placeBoardPieces()

    def receive_move(self, a_move: dict[str, str]):
        if a_move["type"] == "start":
            self.__queue.put(a_move["value"])
            return
        elif a_move["type"] == "move":
            print(a_move)
            self._board.makeMove({'origin': self.convertCoordinates(a_move['origin']),
                                 'destiny': self.convertCoordinates(a_move['destiny'])})
        elif a_move["type"] == "batch":
            for move in a_move["moves"]:
                self.receive_move(move)


    def convertCoordinates(self, coord: tuple[int, int]):
        x, y = coord
        return 9 - x, 8 - y

    
    def __send_batch(self):
        status = "next" if self._board.getMatchInProgress() else "finished"
        self._dog_server_interface.send_move(
            {"type": "batch", 
             "moves": self.__batch_moves, 
             "match_status": status
        })
        self.__batch_moves.clear()
    
    def sendBatch(self):
        # Usa uma thread pra evitar que a interface fique congelada enquanto um movimento é enviado.
        Thread(
            target=self.__send_batch,
        ).start()
    
    def addToBatch(self, move: dict[str, any]):
        self.__batch_moves.append(move)

    def selectPosition(self, line: int, column: int):
        self._board.selectPosition(line, column)

    def showValidPositions(self, positions: list[tuple[int, int]]):
        self._game_interface.showValidPosition(positions)

    def updateInterfaceMove(self, origin: tuple[int, int], destiny: tuple[int, int]):
        self._game_interface.updateInterfaceMove(origin, destiny)

    def showMessage(self, message: str):
        self._game_interface.showMessage(message)
    
    def receive_withdrawal_notification(self):
        self._board.finishMatch()
        self._game_interface.showMessage("O jogador adversário desistiu!!")


    

