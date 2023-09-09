from tkinter import *
from .board import BoardFrame
from .control import ControlFrame
from .settings import *


class GameInterface:
    def __init__(self, root: Tk):
        self.root = root
        self._initialize_window()
        self._initialize_menu()
        self.board_interface = BoardFrame(self.root)
        self.control_interface = ControlFrame(self.root)

    def _initialize_window(self):
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)

    def _initialize_menu(self):
        menu = Menu(self.root)
        menu.option_add("*tearOff", False)
        self.root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label=MENU_OPTION_TEXT, menu=file_menu)
        file_menu.add_command(label=MENU_NEW_GAME_TEXT, command=self._new_game)

    def _new_game(self):
        print("Placeholder")

    def run(self):
        self.board_interface.frame.pack(side=LEFT, fill=BOTH)
        self.control_interface.frame.pack(side=RIGHT, fill=BOTH, expand=True)
        # self.root.mainloop()
