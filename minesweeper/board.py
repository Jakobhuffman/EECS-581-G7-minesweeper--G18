# board.py
# Contain the two main classes for the game:
# 1. Board: Represents the game board and handles the logic for intializing the board, revealing cells, placing flags, and checking for wins/losses.
# 2. Cell: Represents a single cell on the board, including its state (covered, uncovered, flagged) and the number of adjacent mines.
# Authors: Michael Buckendahl, C. Cooper
# Creation Date: 9/4/2025

import config
import random


class Cell:
    def __init__(self):
        self.is_revealed = False
        self.is_flag = False
        self.is_mine = False
        self.can_be_mine = True
        self.adjacent_mines = 0

class BoardGame:
    def __init__(self):
        self.board = [[Cell() for _ in range(config.GRID_COLS)] for _ in range(config.GRID_ROWS)]
        self.total_mines = 0
        self.used_flags = 0
        self.phase = 'ready'
        self.flags_remaining = config.MINE_MAX
        self.is_first_click = True

    def init_board(self):

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

    def reveal(self, click_pos_x, click_pos_y):
        return

    def toggle_flag(self, click_pos_x, click_pos_y):
        return

    def check_win(self):
        if self.phase != "playing":
            return
        for row in self.board:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return
        self.phase = "won"

    def reveal_all_mines(self):
        for row in self.board:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True
    
    def handle_first_click(self, cell: Cell):
        """Generates the minesweeper board such that the given cell is not a mine.

        Args:
            cell (Cell): The cell that was clicked on.
        """
        # Prevent this cell from being selected as a mine
        cell.can_be_mine = False

        # Mark that the first click has been handled
        self.is_first_click = False

        # Generate the board
        self.init_board()
