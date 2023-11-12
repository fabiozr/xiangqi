from interface.game import GameInterface
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
from uuid import uuid4

class PlayerInterface(DogPlayerInterface):
    game_interface: GameInterface
    dog_sever_interface: DogActor
    player_name: str


    def __init__(self):
        self.game_interface = GameInterface(self)

        # Estabelecer conexão
        self.dog_sever_interface = DogActor()
        player_name = self.generatePlayerName()
        message = self.dog_sever_interface.initialize(player_name, self)
        self.game_interface.showMessage(message)
        
        if message == "Conectado a Dog Server":
            self.game_interface.run()
        

    def generatePlayerName(self) -> str:
        return str(uuid4())

    def start_match(self):
        start_status = self.dog_sever_interface.start_match(2)
        message = start_status.get_message()
        
        self.game_interface.showMessage(message)
        if message == "Partida iniciada":
            self.game_interface.new_game()

    def receive_start(self, start_status: StartStatus):
        print(start_status.get_players(), start_status.get_code(), start_status.get_local_id())
        message = start_status.get_message()
        self.game_interface.showMessage(message)        
        self.game_interface.new_game()
