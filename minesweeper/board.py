# board.py
# Contain the two main classes for the game:
# 1. Board: Represents the game board and handles the logic for intializing the board, revealing cells, placing flags, and checking for wins/losses.
# 2. Cell: Represents a single cell on the board, including its state (covered, uncovered, flagged) and the number of adjacent mines.
# Authors: Michael Buckendahl
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

    def reveal(self, pos,click_pos_x=None, click_pos_y=None):
        if pos != None:# set variables
            click_pos_x = pos[0]
            click_pos_y = pos[1]

        relative_x = click_pos_x - (config.GRID_POS_X)  # calc position in grid
        relative_y = click_pos_y - (config.GRID_POS_Y)
        col = relative_x // config.CELL_SIZE  # which column
        row = relative_y // config.CELL_SIZE  # which row

        if (0 <= relative_x <= config.GRID_COLS * config.CELL_SIZE) and ( 0 <= relative_y <= config.GRID_ROWS * config.CELL_SIZE): #is it on the board
            if self.is_first_click==True: #first click initialize board
                self.init_board()
                self.is_first_click=False
                print('First click:',row,col)
                return

            clicked_cell=self.board[row][col]
            print("Cell clicked:", row,col, "Mine?",clicked_cell.is_mine)
            if clicked_cell.is_mine:
                self.phase="loss"
                self.reveal_all_mines()
                return
            if clicked_cell.adjacent_mines > 0: #is a number
                print("Cell is number",row,col,":", clicked_cell.adjacent_mines)
                clicked_cell.is_revealed=True
            else:
                self.flood_reveal(row, col)
        else:
            print("Not on Board")
        return

    def flood_reveal(self, row,col):
        if not (0 <= row < config.GRID_ROWS and 0 <= col < config.GRID_COLS): #make sure the cell is in the grid
            return
        cell = self.board[row][col]
        if cell.is_flag or cell.is_revealed: #if flag or reveal you cant reveal
            return

        cell.is_revealed=True# passes so reveal
        print("Cell revealed: ", row,col)

        if cell.adjacent_mines > 0: #stop if neighbor mine
            return

        for dr in (-1, 0, 1): #
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                self.flood_reveal(row + dr, col + dc)

    def toggle_flag(self, click_pos_x, click_pos_y):
        return

    def check_win(self):
        return

    def reveal_all_mines(self):
        return
    
    def handle_first_click(self, cell):
        return