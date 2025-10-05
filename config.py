# Config.py
# Configuration of settings and other constants for the project
# Inputs: None
# Outputs: None
# Author(s): Michael Buckendahl
# Creation Date: 9/2/2025

# Define the frames per second to limit cpu usage
FPS = 60

# Define the window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Define what font and size we will use across the application
FONT_NAME = "Arial"
FONT_SIZE = 12
OUTCOME_FONT_SIZE = 24
TITLE_FONT_SIZE = 36
DESC_FONT_SIZE = 18


# Define the colors of different elements of the application
COLOR_BACKGROUND = (30, 30, 30)  # Dark gray background
COLOR_CELL_COVERED = (200, 200, 200)  # Light gray for covered cells
COLOR_CELL_UNCOVERED = (255, 255, 255)  # White for uncovered cells
COLOR_CELL_FLAGGED = (255, 20, 147)  # Hot pink for flagged cells
COLOR_CELL_MINE = (255, 0, 0)  # Red for mines
COLOR_GRID_LINES = (100, 100, 100)  # Light gray for grid lines
COLOR_1_NEAR_MINE = (0, 0, 255)  # Blue for cells with 1 adjacent mine
COLOR_2_NEAR_MINE = (0, 255, 0)  # Green for cells with 2 adjacent mines
COLOR_3_NEAR_MINE = (255, 255, 0)  # Yellow for cells with 3 adjacent mines
COLOR_4_NEAR_MINE = (255, 0, 255)  # Magenta for cells with 4 adjacent mines
COLOR_5_NEAR_MINE = (0, 255, 255)  # Cyan for cells with 5 adjacent mines
COLOR_6_NEAR_MINE = (255, 165, 0)  # Orange for cells with 6 adjacent mines
COLOR_7_NEAR_MINE = (128, 0, 128)  # Purple for cells with 7 adjacent mines
COLOR_8_NEAR_MINE = (0, 128, 128)  # Teal for cells with 8 adjacent mines
COLOR_TEXT = (255, 255, 255)  # White for text

# Define constants for the game
MIN_MINES = 10
MAX_MINES = 20
GRID_ROWS = 10
GRID_COLS = 10
CELL_SIZE = 40  # Size of each cell in pixels
HELP_TEXT = "To select a cell, hover over it and left-click. If you want to place a flag hover over a cell and right-click. If you want to restart the game press R."
WON_TEXT = "You won! Press 'R' to restart."
LOST_TEXT = "You lost! Press 'R' to restart."
TITLE = "Minesweeper"
DESC_TEXT = "Clear the board without detonating any mines."
NUM_MINES_TEXT = f"Number of Mines({MIN_MINES}-{MAX_MINES}):"
MINES_ERROR_BAD_INPUT_TEXT = f"Please enter a number of mines between {MIN_MINES} and {MAX_MINES}"
START_BUTTON_LABEL = "Start Game"

# AI configuration
AI_TEXT = "Select AI Difficulty:"
AI_BUTTON_EASY = "Easy"
AI_BUTTON_MEDIUM = "Medium"
AI_BUTTON_HARD = "Hard"
AI_BUTTON_NONE = "No AI"

# Define the positioning of elements in the window in there x and y
GRID_POS_X = 200
GRID_POS_Y = 100
CONTROLS_TEXT_X = 100
CONTROLS_TEXT_Y = 525
FLAGS_REMAINING_X = 650
FLAGS_REMAINING_Y = 75
OUTCOME_X = 350
OUTCOME_Y = 550
TITLE_POS_X = WINDOW_WIDTH // 2
TITLE_POS_Y = 100
DESC_POS_X = WINDOW_WIDTH // 2
DESC_POS_Y = 160
MINES_TEXT_X = WINDOW_WIDTH // 2
MINES_TEXT_Y = 220
START_BUTTON_X = WINDOW_WIDTH // 2
START_BUTTON_Y = 300
AI_TEXT_X = WINDOW_WIDTH // 2
AI_TEXT_Y = 350
AI_BUTTON_Y = 400
AI_EASY_X = WINDOW_WIDTH // 2 - 110
AI_MEDIUM_X = WINDOW_WIDTH // 2
AI_HARD_X = WINDOW_WIDTH // 2 + 110
AI_NONE_X = WINDOW_WIDTH // 2 - 220


def set_difficulty(difficulty: str) -> None: #Changes game settings according to the selected difficulty
	
	global GRID_ROWS, GRID_COLS, MIN_MINES, MAX_MINES, CELL_SIZE, NUM_MINES_TEXT, MINES_ERROR_BAD_INPUT_TEXT, CURRENT_DIFFICULTY

	difficulty = (difficulty or '').lower()
	CURRENT_DIFFICULTY = difficulty

	if difficulty == 'easy':
		GRID_ROWS = 8
		GRID_COLS = 8
		MIN_MINES = 5
		MAX_MINES = 15
		CELL_SIZE = 50
	elif difficulty == 'hard':
		GRID_ROWS = 16
		GRID_COLS = 16
		MIN_MINES = 20
		MAX_MINES = 60
		CELL_SIZE = 30
	else:  # normal / fallback
		GRID_ROWS = 10
		GRID_COLS = 10
		MIN_MINES = 10
		MAX_MINES = 20
		CELL_SIZE = 40

	# Update related text constants so modules that import config after this call
	# will see the updated ranges. Note: modules that imported the previous
	# values with `from config import ...` won't automatically update.
	NUM_MINES_TEXT = f"Number of Mines({MIN_MINES}-{MAX_MINES}):"
	MINES_ERROR_BAD_INPUT_TEXT = f"Please enter a number of mines between {MIN_MINES} and {MAX_MINES}"
