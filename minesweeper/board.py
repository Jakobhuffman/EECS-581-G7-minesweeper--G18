# board.py
# Contain the two main classes for the game:
# 1. Board: Represents the game board and handles the logic for intializing the board, revealing cells, placing flags, and checking for wins/losses.
# 2. Cell: Represents a single cell on the board, including its state (covered, uncovered, flagged) and the number of adjacent mines.
# Inputs: None
# Outputs: None
# Authors: Michael Buckendahl, C. Cooper, Cole Charpentier
# Creation Date: 9/4/2025

import config
import random


class Cell:
    """Represents a cell in the minesweeper game
    """

    def __init__(self):
        self.is_revealed = False
        self.is_flag = False
        self.is_mine = False
        self.can_be_mine = True
        self.adjacent_mines = 0 # to be calculated later after board is initialized

class BoardGame:
    """Represents the board in the minesweeper game
    """

    def __init__(self):
        self.board = [[Cell() for _ in range(config.GRID_COLS)] for _ in range(config.GRID_ROWS)]
        self.total_mines = 0 # to be set later when the user gives us a value
        self.used_flags = 0
        self.phase = 'ready'
        self.flags_remaining = 0 # to be calculated as total_mines - used_flags
        self.is_first_click = True

    def init_board(self):
        """Randomly place mines on the board and calculate adjacent mine counts"""

        # This places mine randomly on the board.
        # This loops till all the bombs are placed, it is not a for loop because if a randomly
        # selected cell is already a mine it will not place a new one and try again.
        mines_placed = 0
        while mines_placed < self.total_mines:
            x = random.randint(0, config.GRID_COLS - 1)
            y = random.randint(0, config.GRID_ROWS - 1)
            if self.board[x][y].can_be_mine:
                self.board[x][y].is_mine = True
                self.board[x][y].can_be_mine = False
                self.update_adjacent_mines(x, y)
                mines_placed += 1

    def update_adjacent_mines(self, x, y):
        """Update the adjacent mine counts for all neighboring cells"""

        # Go through each neighbor and increment its adjacent mine count
        if x+1 < config.GRID_ROWS:
            self.board[x+1][y].adjacent_mines += 1
        if x-1 >= 0:
            self.board[x-1][y].adjacent_mines += 1
        if y+1 < config.GRID_COLS:
            self.board[x][y+1].adjacent_mines += 1
        if y-1 >= 0:
            self.board[x][y-1].adjacent_mines += 1
        if x+1 < config.GRID_ROWS and y+1 < config.GRID_COLS:
            self.board[x+1][y+1].adjacent_mines += 1
        if x-1 >= 0 and y-1 >= 0:
            self.board[x-1][y-1].adjacent_mines += 1
        if x+1 < config.GRID_ROWS and y-1 >= 0:
            self.board[x+1][y-1].adjacent_mines += 1
        if x-1 >= 0 and y+1 < config.GRID_COLS:
            self.board[x-1][y+1].adjacent_mines += 1

    def reveal(self, col, row): #reveals a cell
        if self.is_first_click==True: #first click initialize board and handle first click if so
            self.handle_first_click(row, col)

        clicked_cell=self.board[row][col] # gets the cell
        if clicked_cell.is_mine: #if a mine then lose game and reveal all mines
            self.phase="lost"
            self.reveal_all_mines()
            return
        if clicked_cell.adjacent_mines > 0: #is a number reveal it
            clicked_cell.is_revealed=True
        else: #if passes all others, start flood reveal since its an empty spot
            self.flood_reveal(row, col)

        self.check_win()

    def flood_reveal(self, row,col): # reveals the empty spots
        if not (0 <= row < config.GRID_ROWS and 0 <= col < config.GRID_COLS): #make sure the cell is in the grid
            return
        cell = self.board[row][col] # grab cell
        if cell.is_flag or cell.is_revealed: #if flag or reveal you cant reveal
            return

        cell.is_revealed=True# passes so reveal

        if cell.adjacent_mines > 0: #stop if neighbor mine
            return

        for dr in (-1, 0, 1): #otherwise continues revealing
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                self.flood_reveal(row + dr, col + dc)

    def toggle_flag(self, click_pos_x, click_pos_y):
        """Toggle a flag on a covered cell given x and y coordinates"""

        # Only handle flags while the game is active
        if self.phase != "playing":
            return

        # Ensure click maps inside the grid
        if not (0 <= click_pos_y < config.GRID_ROWS and 0 <= click_pos_x < config.GRID_COLS):
            return

        # Access target cell
        cell = self.board[click_pos_y][click_pos_x]

        # Ignore revealed cells
        if cell.is_revealed:
            return

        # Toggle flag status
        if cell.is_flag:
            # If flagged remove the flag and decrement counter
            cell.is_flag = False
            self.used_flags = max(0, self.used_flags - 1)
        else:
            if self.used_flags < self.total_mines:
                cell.is_flag = True
                self.used_flags += 1

    def check_win(self):
        """Check if the player has won (revealed all non-mine cells)"""

        # Only check for a win if the game is being played
        if self.phase != "playing":
            return

        # Iterate through each cell
        for row in self.board:
            for cell in row:
                # If a cell is not a mine and has not been revealed the player has not won so return early
                if not cell.is_mine and not cell.is_revealed:
                    return
        # If this line is reached all non-mine cells have been revealed so player wins
        self.phase = "won"
 
    def reveal_all_mines(self):
        """Used to reveal every mine (called when player loses)"""

        # Iterate through every cell
        for row in self.board:
            for cell in row:
                if cell.is_mine:
                    # If cell is a mine reveal it
                    cell.is_revealed = True
    
    def handle_first_click(self, row: int, column: int):
        """Generates the minesweeper board such that the given cell is not a mine.
           This ensures that the first click is always safe.

        Args:
            cell (Cell): The cell that was clicked on.
        """

        # Prevent this and adjacent cells from being selected as a mine
        self.board[row][column].can_be_mine = False

        if row+1 < config.GRID_ROWS:
            self.board[row+1][column].can_be_mine = False
        if row-1 >= 0:
            self.board[row-1][column].can_be_mine = False
        if column+1 < config.GRID_COLS:
            self.board[row][column+1].can_be_mine = False
        if column-1 >= 0:
            self.board[row][column-1].can_be_mine = False
        if row+1 < config.GRID_ROWS and column+1 < config.GRID_COLS:
            self.board[row+1][column+1].can_be_mine = False
        if row-1 >= 0 and column-1 >= 0:
            self.board[row-1][column-1].can_be_mine = False
        if row+1 < config.GRID_ROWS and column-1 >= 0:
            self.board[row+1][column-1].can_be_mine = False
        if row-1 >= 0 and column+1 < config.GRID_COLS:
            self.board[row-1][column+1].can_be_mine = False


        # Mark that the first click has been handled
        self.is_first_click = False

        # Generate the board
        self.init_board()
