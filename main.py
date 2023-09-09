# Temporary file to test the game, will be replaced by the player actor

from tkinter import *
from interface.game import GameInterface
from interface.settings import *


class Game(Tk):
    def __init__(self):
        super().__init__()
        self.game_interface = GameInterface(self)
        self.board = self.game_interface.board_interface
        self.image_black_path = "images/Pawn-Black.png"
        self.image_black = self.board._load_image(self.image_black_path)
        self.image_red_path = "images/Pawn-Red.png"
        self.image_red = self.board._load_image(self.image_red_path)
        self.board_state = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.run()

    def place_pieces(self):
        for i, row in enumerate(self.board_state):
            for j, cell in enumerate(row):
                if cell == 1:
                    self.image = self.image_black if i < 5 else self.image_red
                    piece = self.board._place_piece(self.image, j + 1, i + 1)
                    self.board_state[i][j] = piece

    def show_moves(self, event: Event):
        self.board._delete_dots()
        piece = self.board._get_current_piece()
        column, row = self.board._get_grid_position_from_event(event)
        dots = self.place_dots_on_board(column, row)
        for dot in dots:
            self.board._make_clickable(dot, lambda event: self.move_piece(event, piece))

    def place_dots_on_board(self, column: int, row: int):
        dots_in_column = [
            self.board._place_dot(column, i)
            for i in range(1, NUMBER_OF_ROWS)
            if i != row
        ]
        dots_in_row = [
            self.board._place_dot(j, row)
            for j in range(1, NUMBER_OF_COLUMNS)
            if j != column
        ]
        return dots_in_column + dots_in_row

    def move_piece(self, event: Event, piece):
        column, row = self.board._get_grid_position_from_event(event)
        piece_on_square = self.board._get_piece_on_square(column, row)
        if piece_on_square and piece_on_square != piece:
            self.board._delete_piece(piece_on_square)
        self.board._move_piece(piece, column, row)
        self.board._delete_dots()

    def add_click_handlers(self):
        for i, row in enumerate(self.board_state):
            for j, cell in enumerate(row):
                if cell != 0:
                    piece = cell
                    self.board._make_clickable(piece, self.show_moves)

    def run(self):
        self.place_pieces()
        self.add_click_handlers()
        self.game_interface.run()


if __name__ == "__main__":
    game = Game()
    game.mainloop()
