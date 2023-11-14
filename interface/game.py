from typing import Callable
from threading import Thread
from time import sleep
from enum import Enum, auto

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from .settings import *

from dog.dog_interface import DogPlayerInterface

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player_interface import PlayerInterface


class GameInterface(Tk):
    player_interface: "PlayerInterface"
    frame: Frame
    canvas: Canvas
    images: dict[str, PhotoImage]
    local_color: str

    def __init__(self, player_interface: "PlayerInterface"):
        super().__init__()

        self._initialize_window()
        self._initialize_menu()
        self.frame = Frame(
            self,
            bg=BACKGROUND_COLOR,
            padx=CELL_SIZE / 2,
            pady=CELL_SIZE / 2,
        )
        self.canvas = Canvas(
            self.frame,
            width=NUMBER_OF_COLUMNS * CELL_SIZE,
            height=NUMBER_OF_ROWS * CELL_SIZE,
            borderwidth=0,
            highlightthickness=0,
            bg=BOARD_COLOR,
        )
        self._draw_grid()
        self.canvas.pack()
        self.player_interface = player_interface

        self.images = {
            "p_b": self._load_image("images/Pawn-Black.png"),
            "p_r": self._load_image("images/Pawn-Red.png"),
            "a_b": self._load_image("images/Advisor-Black.png"),
            "a_r": self._load_image("images/Advisor-Red.png"),
            "c_b": self._load_image("images/Cannon-Black.png"),
            "c_r": self._load_image("images/Cannon-Red.png"),
            "e_b": self._load_image("images/Elephant-Black.png"),
            "e_r": self._load_image("images/Elephant-Red.png"),
            "k_b": self._load_image("images/King-Black.png"),
            "k_r": self._load_image("images/King-Red.png"),
            "h_b": self._load_image("images/Horse-Black.png"),
            "h_r": self._load_image("images/Horse-Red.png"),
            "r_r": self._load_image("images/Rook-Red.png"),
            "r_b": self._load_image("images/Rook-Black.png"),
        }

        self.board_state = [
            ["r_b", "h_b", "e_b", "a_b", "k_b", "a_b", "e_b", "h_b", "r_b"],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, "c_b", 0, 0, 0, 0, 0, "c_b", 0],
            ["p_b", 0, "p_b", 0, "p_b", 0, "p_b", 0, "p_b"],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ["p_r", 0, "p_r", 0, "p_r", 0, "p_r", 0, "p_r"],
            [0, "c_r", 0, 0, 0, 0, 0, "c_r", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ["r_r", "h_r", "e_r", "a_r", "k_r", "a_r", "e_r", "h_r", "r_r"],
        ]

    def _initialize_window(self):
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

    def _initialize_menu(self):
        menu = Menu(self)
        menu.option_add("*tearOff", False)
        self.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label=MENU_OPTION_TEXT, menu=file_menu)
        file_menu.add_command(
            label=MENU_NEW_GAME_TEXT,
            command=lambda: self.player_interface.start_match(),
        )

    def showMessage(self, message: str):
        messagebox.showinfo("information", message)

    
    def setLocalColor(self, color: str):
        self.local_color = color

    def placeBoardPieces(self):
        if self.local_color != "RED":
            l = 0
            r = len(self.board_state) - 1

            while l < r:
                self.board_state[l], self.board_state[r] = self.board_state[r], self.board_state[l]
                l += 1
                r -= 1

        for i, row in enumerate(self.board_state):
            for j, cell in enumerate(row):
                if cell:
                    image = self.images[cell]
                    piece = self._place_piece(image, j + 1, i + 1)
                    self.board_state[i][j] = piece
        self.add_click_handlers()

    def clickPosition(self, event: Event):
        self._delete_dots()
        column, row = self._get_grid_position_from_event(event)
        self.player_interface.selectPosition(row, column)

    def updateInterfaceMove(self, origin: tuple[int, int], destiny: tuple[int, int]):
        piece_origin = self._get_piece_on_square(origin[1]+1, origin[0]+1)
        piece_destiny = self._get_piece_on_square(destiny[1]+1, destiny[0]+1)

        self.board_state[destiny[0]][destiny[1]] = self.board_state[origin[0]][origin[1]]
        self.board_state[origin[0]][origin[1]] = 0

        if piece_destiny and piece_origin != piece_destiny:
            self._delete_piece(piece_destiny)

        self._move_piece(piece_origin, destiny[1]+1, destiny[0]+1)
        self._delete_dots()


    def showValidPosition(self, positions: list[tuple[int, int]]):
        for row, column in positions:
            dot = self._place_dot(column + 1, row + 1)
            self._make_clickable(dot, self.clickPosition)

    def place_dots_on_board(self, column: int, row: int):
        dots_in_column = [
            self._place_dot(column, i) for i in range(1, NUMBER_OF_ROWS) if i != row
        ]
        dots_in_row = [
            self._place_dot(j, row) for j in range(1, NUMBER_OF_COLUMNS) if j != column
        ]
        return dots_in_column + dots_in_row

    def move_piece(self, event: Event, piece):
        """
        TODO: As posições no tabuleiro local são diferentes. 
              Por exemplo, a linha 0 no tabuleiro do RED corresponde à linha 9.
                
              Para compensar isso, temos que aplicar a função self._transform nas coordenadas!!

        """
        column, row = self._get_grid_position_from_event(event)
        piece_on_square = self._get_piece_on_square(column, row)
        if piece_on_square and piece_on_square != piece:
            self._delete_piece(piece_on_square)
        self._move_piece(piece, column, row)
        self._delete_dots()

    def _transform(self, coords: tuple[int, int]) -> tuple[int, int]:
        if self.local_color == "RED":
            return coords
        return 9 - coords[0], coords[1] # Aaaacho que ta certo. Mas nao testei

    def add_click_handlers(self):
        for i, row in enumerate(self.board_state):
            for j, cell in enumerate(row):
                if cell != 0:
                    piece = cell
                    self._make_clickable(piece, self.clickPosition)

    def run(self):
        self.frame.pack(side=LEFT, fill=BOTH)
        self.frame.pack(side=RIGHT, fill=BOTH, expand=True)
        # self.placeBoardPieces()
        # self.add_click_handlers()
        self.mainloop()

    def _draw_grid(self):
        self._draw_board()
        self._draw_river()
        self._draw_palace(1)
        self._draw_palace(8)

    def _draw_board(self):
        for column in range(NUMBER_OF_COLUMNS):
            for row in range(NUMBER_OF_ROWS):
                if column in [0, 9] or row in [0, 10]:
                    continue
                self.canvas.create_rectangle(
                    column * CELL_SIZE,
                    row * CELL_SIZE,
                    (column + 1) * CELL_SIZE - 1,
                    (row + 1) * CELL_SIZE - 1,
                    width=CELL_WIDTH,
                    outline=GRID_COLOR,
                )

    def _draw_river(self):
        self.canvas.create_rectangle(
            1 * CELL_SIZE,
            5 * CELL_SIZE,
            9 * CELL_SIZE - 1,
            6 * CELL_SIZE - 1,
            fill=BOARD_COLOR,
            outline=GRID_COLOR,
            width=CELL_WIDTH,
        )

    def _draw_palace(self, start_row: int):
        self.canvas.create_line(
            4 * CELL_SIZE,
            start_row * CELL_SIZE,
            6 * CELL_SIZE,
            (start_row + 2) * CELL_SIZE,
            fill=GRID_COLOR,
            width=CELL_WIDTH,
        )
        self.canvas.create_line(
            6 * CELL_SIZE,
            start_row * CELL_SIZE,
            4 * CELL_SIZE,
            (start_row + 2) * CELL_SIZE,
            fill=GRID_COLOR,
            width=CELL_WIDTH,
        )

    def _load_image(self, image_path: str):
        image = Image.open(image_path)
        image = image.resize((int(CELL_SIZE - 5), int(CELL_SIZE - 5)))
        return ImageTk.PhotoImage(image)

    def _get_grid_position_from_event(self, event: Event):
        x, y = event.x, event.y

        column = x / CELL_SIZE
        row = y / CELL_SIZE
        return round(column), round(row)

    def _get_absolute_position(self, column: int, row: int):
        x = column * CELL_SIZE
        y = row * CELL_SIZE
        return x, y

    def _place_piece(self, image: ImageTk.PhotoImage, column: int, row: int):
        x, y = self._get_absolute_position(column, row)
        return self.canvas.create_image(x, y, image=image, tags=PIECES_TAG)

    def _move_piece(self, piece_id: str, column: int, row: int):
        x, y = self._get_absolute_position(column, row)
        self.canvas.coords(piece_id, x, y)

    def _get_current_piece(self):
        return self.canvas.find_withtag(CURRENT_TAG)[0]

    def _delete_piece(self, piece_id: str | int):
        self.canvas.delete(piece_id)

    def _get_piece_on_square(self, column: int, row: int):
        x, y = self._get_absolute_position(column, row)
        items = self.canvas.find_overlapping(x, y, x, y)

        pieces = self.canvas.find_withtag(PIECES_TAG)

        for item_id in items:
            if item_id in pieces:
                return item_id

    def _place_dot(self, column: int, row: int):
        x, y = self._get_absolute_position(column, row)
        return self.canvas.create_oval(
            x - DOT_WIDTH - 2,
            y - DOT_WIDTH,
            x + DOT_WIDTH,
            y + DOT_WIDTH + 2,
            fill=DOT_COLOR,
            tags=DOTS_TAG,
        )

    def _delete_dots(self):
        self.canvas.delete(DOTS_TAG)

    def _make_clickable(self, id: int, callback: Callable):
        self.canvas.tag_bind(id, "<Button-1>", callback)
        self.canvas.tag_bind(id, "<Enter>", lambda _: self._make_cursor_clickable())
        self.canvas.tag_bind(id, "<Leave>", lambda _: self._reset_cursor())

    def _make_cursor_clickable(self):
        self.canvas.config(cursor="hand2")

    def _reset_cursor(self):
        self.canvas.config(cursor="")
