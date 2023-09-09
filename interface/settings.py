# Main window settings
WINDOW_TITLE = "Xiangqi"
WINDOW_HEIGHT = 720
WINDOW_WIDTH = int(WINDOW_HEIGHT * 1.33333)  # 4:3 aspect ratio
BACKGROUND_COLOR = "#5b3223"

# Menu settings
MENU_OPTION_TEXT = "Opções"
MENU_NEW_GAME_TEXT = "Novo jogo"

# Timer settings
TIMER_COLOR = "#382d2c"
TEXT_COLOR = "#eeede9"
TIMER_FONT = ("Helvetica", 50)

# Give up button settings
GIVE_UP_TEXT = "Desistir"
GIVE_UP_COLOR = "#c0a866"
GIVE_UP_COLOR_ACTIVE = "#b59a4e"
GIVE_UP_FONT = ("Helvetica", 30)

# Board settings
BOARD_SIZE = WINDOW_HEIGHT * 0.83333
BOARD_COLOR = "#c05832"

# Board grid settings
NUMBER_OF_COLUMNS = 10  # 9 columns + 1 for the frame
NUMBER_OF_ROWS = 11  # 10 rows + 1 for the frame
GRID_COLOR = "#190c06"
DOT_COLOR = "#692947"

# Board cell settings
CELL_SIZE = BOARD_SIZE / NUMBER_OF_COLUMNS
CELL_WIDTH = CELL_SIZE / 20
DOT_WIDTH = CELL_SIZE / 9

# Board canvas tags
DOTS_TAG = "dots"
PIECES_TAG = "pieces"
CURRENT_TAG = "current"
