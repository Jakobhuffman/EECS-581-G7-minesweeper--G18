# minesweeper/ai_solver.py
# Contains the logic for the AI solver.
# Inputs: Game board state
# Outputs: AI move (reveal or flag a cell)
# Author(s): Gemini Code Assist
# Creation Date: 10/27/2023

import random
from minesweeper.board import BoardGame
import config

class AISolver:
    """
    An AI solver for the Minesweeper game with different difficulty levels.
    """
    def __init__(self, board: BoardGame, difficulty: str):
        self.board = board
        self.difficulty = difficulty

    def make_move(self):
        """
        Makes a move based on the selected difficulty.
        Returns a tuple (action, (row, col)) or None if no move is made.
        """
        if self.difficulty == 'easy':
            return self.easy_move()
        elif self.difficulty == 'medium':
            return self.medium_move()
        elif self.difficulty == 'hard':
            return self.hard_move()
        return None

    def get_neighbors(self, row, col):
        """Returns a list of neighbor coordinates for a given cell."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < config.GRID_ROWS and 0 <= c < config.GRID_COLS:
                    neighbors.append((r, c))
        return neighbors

    def easy_move(self):
        """Makes a random move on a hidden, un-flagged cell."""
        hidden_cells = []
        for r in range(config.GRID_ROWS):
            for c in range(config.GRID_COLS):
                cell = self.board.board[r][c]
                if not cell.is_revealed and not cell.is_flag:
                    hidden_cells.append((r, c))
        
        if hidden_cells:
            row, col = random.choice(hidden_cells)
            # Board.reveal expects (row, col)
            self.board.reveal(row, col)
            return ('reveal', (row, col))
        return None

    def _find_basic_move(self):
        """Finds a move using basic logic without executing it."""
        for r in range(config.GRID_ROWS):
            for c in range(config.GRID_COLS):
                cell = self.board.board[r][c]
                if cell.is_revealed and cell.adjacent_mines > 0:
                    neighbors = self.get_neighbors(r, c)
                    hidden_neighbors = [n for n in neighbors if not self.board.board[n[0]][n[1]].is_revealed]
                    flagged_neighbors = [n for n in neighbors if self.board.board[n[0]][n[1]].is_flag]

                    # Rule 1: If hidden neighbors == cell's number, flag them all.
                    if len(hidden_neighbors) - len(flagged_neighbors) == cell.adjacent_mines - len(flagged_neighbors) and len(hidden_neighbors) > len(flagged_neighbors):
                        for row, col in hidden_neighbors:
                            if not self.board.board[row][col].is_flag:
                                return ('flag', (row, col))

                    # Rule 2: If flagged neighbors == cell's number, reveal other hidden neighbors.
                    if len(flagged_neighbors) == cell.adjacent_mines:
                        for row, col in hidden_neighbors:
                            if not self.board.board[row][col].is_flag:
                                return ('reveal', (row, col))
        return None

    def medium_move(self):
        """Applies basic logic, otherwise makes a random move."""
        move = self._find_basic_move()
        if move:
            action, (row, col) = move
            if action == 'flag':
                self.board.toggle_flag(row, col)
                return ('flag', (row, col))
            elif action == 'reveal':
                self.board.reveal(row, col)
                return ('reveal', (row, col))
        # If no logical move, make a random one
        return self.easy_move()

    def hard_move(self):
        """Applies medium logic + 1-2-1 pattern, otherwise random."""
        # Try basic logic first
        move = self._find_basic_move()
        if move:
            action, (row, col) = move
            if action == 'flag':
                self.board.toggle_flag(row, col)
                return ('flag', (row, col))
            elif action == 'reveal':
                self.board.reveal(row, col)
                return ('reveal', (row, col))

        # 1-2-1 Pattern (Horizontal)
        for r in range(config.GRID_ROWS):
            for c in range(config.GRID_COLS - 2):
                c1, c2, c3 = self.board.board[r][c], self.board.board[r][c+1], self.board.board[r][c+2]
                if c1.is_revealed and c2.is_revealed and c3.is_revealed and \
                   c1.adjacent_mines == 1 and c2.adjacent_mines == 2 and c3.adjacent_mines == 1:
                    # Check for hidden neighbors above or below
                    for offset in (-1, 1):
                        nr = r + offset
                        if 0 <= nr < config.GRID_ROWS:
                            nc1 = self.board.board[nr][c]
                            nc2 = self.board.board[nr][c+1]
                            nc3 = self.board.board[nr][c+2]
                            if not nc1.is_revealed and not nc2.is_revealed and not nc3.is_revealed:
                                # Flag outer
                                if not nc1.is_flag:
                                    self.board.toggle_flag(nr, c)
                                    return ('flag', (nr, c))
                                if not nc3.is_flag:
                                    self.board.toggle_flag(nr, c + 2)
                                    return ('flag', (nr, c + 2))
                                # Reveal inner
                                if not nc2.is_flag:
                                    self.board.reveal(nr, c + 1)
                                    return ('reveal', (nr, c + 1))

        # 1-2-1 Pattern (Vertical)
        for c in range(config.GRID_COLS):
            for r in range(config.GRID_ROWS - 2):
                c1, c2, c3 = self.board.board[r][c], self.board.board[r+1][c], self.board.board[r+2][c]
                if c1.is_revealed and c2.is_revealed and c3.is_revealed and \
                   c1.adjacent_mines == 1 and c2.adjacent_mines == 2 and c3.adjacent_mines == 1:
                    # Check for hidden neighbors left or right
                    for offset in (-1, 1):
                        nc = c + offset
                        if 0 <= nc < config.GRID_COLS:
                            nc1 = self.board.board[r][nc]
                            nc2 = self.board.board[r+1][nc]
                            nc3 = self.board.board[r+2][nc]
                            if not nc1.is_revealed and not nc2.is_revealed and not nc3.is_revealed:
                                # Flag outer
                                if not nc1.is_flag:
                                    self.board.toggle_flag(r, nc)
                                    return ('flag', (r, nc))
                                if not nc3.is_flag:
                                    self.board.toggle_flag(r + 2, nc)
                                    return ('flag', (r + 2, nc))
                                # Reveal inner
                                if not nc2.is_flag:
                                    self.board.reveal(r + 1, nc)
                                    return ('reveal', (r + 1, nc))

        # Fallback to random move
        return self.easy_move()
