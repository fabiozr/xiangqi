from tkinter import *
from interface.game import GameInterface
from interface.settings import *

# O CÓDIGO ABAIXO É APENAS UM EXEMPLO DE COMO USAR A INTERFACE. SUBSTITER PELA ATOR JOGADOR/CLASSES DO DOMINIO DO POBLEMA

# Initialize the game board
game_interface = GameInterface()
board = game_interface.board_interface

# Load the image for the game piece
image_path = "images/Pawn-Black.png"
image = board._load_image(image_path)

# Define the initial state of the game pieces on the board
board_state = [
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

# Place the pieces on the board according to the initial state
for i, row in enumerate(board_state):
    for j, cell in enumerate(row):
        if cell == 1:
            piece = board._place_piece(image, j + 1, i + 1)
            board_state[i][j] = piece


# Define the function to show possible moves
def show_moves(event: Event):
    board._delete_dots()
    piece = board._get_current_piece()
    column, row = board._get_grid_position_from_event(event)
    dots = place_dots_on_board(column, row)
    for dot in dots:
        board._make_clickable(dot, lambda event: move_piece(event, piece))


# Define the function to place dots on the board
def place_dots_on_board(column: int, row: int):
    dots_in_column = [
        board._place_dot(column, i) for i in range(1, NUMBER_OF_ROWS) if i != row
    ]
    dots_in_row = [
        board._place_dot(j, row) for j in range(1, NUMBER_OF_COLUMNS) if j != column
    ]
    return dots_in_column + dots_in_row


# Define the function to move a piece
def move_piece(event: Event, piece):
    column, row = board._get_grid_position_from_event(event)
    board._move_piece(piece, column, row)


# Add click event handlers to the pieces
for i, row in enumerate(board_state):
    for j, cell in enumerate(row):
        if cell != 0:
            piece = cell
            board._make_clickable(piece, show_moves)


# board.run()
game_interface.run()
