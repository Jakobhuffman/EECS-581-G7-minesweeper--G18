# Config.py
# Configuration of settings and other constants for the project
# Input: N/A
# Output: N/A
# Author(s): Michael Buckendahl
# Creation Date: 9/2/2025

# Define the frames per second to limit cpu usage
FPS = 60

# Define the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define what font and size we will use across the application
FONT_NAME = "Arial"
FONT_SIZE = 12

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
MINE_MINES = 10
MINE_MAX = 20
GRID_ROWS = 10
GRID_COLS = 10
CELL_SIZE = 40  # Size of each cell in pixels
HELP_TEXT = "To select a cell, hover over it and left-click. If you want to place a flag hover over a cell and right-click. If you want to restart the game press R."

# Define the positioning of elements in the window in there x and y
GRID_POS_X = 200
GRID_POS_Y = 100
HELP_TEXT_X = 100
HELP_TEXT_Y = 525
FLAGS_REMAINING_X = 650
FLAGS_REMAINING_Y = 75
OUTCOME_X = 350
OUTCOME_Y = 550