from tkinter import *
from PIL import Image, ImageTk
from typing import Callable
from .settings import *


class BoardFrame:
    def __init__(self, root: Tk):
        self.frame = Frame(
            root,
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
        x, y = event.x_root, event.y_root + 5
        column = x // CELL_SIZE
        row = y // CELL_SIZE
        return int(column), int(row - 1)

    def _get_absolute_position(self, column: int, row: int):
        x = column * CELL_SIZE
        y = row * CELL_SIZE
        return x, y

    def _place_piece(self, image: ImageTk.PhotoImage, column: int, row: int):
        x, y = self._get_absolute_position(column, row)
        return self.canvas.create_image(x, y, image=image)

    def _move_piece(self, piece_id: str, column: int, row: int):
        x, y = self._get_absolute_position(column, row)
        self.canvas.coords(piece_id, x, y)

    def _get_current_piece(self):
        return self.canvas.find_withtag(CURRENT_TAG)[0]

    def _delete_piece(self, piece_id: str):
        self.canvas.delete(piece_id)

    def _place_dot(self, column: int, row: int):
        x, y = self._get_absolute_position(column, row)
        return self.canvas.create_oval(
            x - DOT_WIDTH - 2,
            y - DOT_WIDTH,
            x + DOT_WIDTH,
            y + DOT_WIDTH + 2,
            fill=GRID_COLOR,
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
