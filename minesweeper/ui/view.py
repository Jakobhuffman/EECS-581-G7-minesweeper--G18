#view.py
#Author: Delaney Gray
#Date: 9-08

import pygame
import pygame_gui
from config import WINDOW_WIDTH, FONT_NAME, FONT_SIZE, HELP_TEXT, CELL_SIZE, GRID_POS_X, GRID_POS_Y, FLAGS_REMAINING_X, FLAGS_REMAINING_Y, NUM_MINES_TEXT, MINES_ERROR_BAD_INPUT_TEXT, WON_TEXT, LOST_TEXT

from minesweeper.board import BoardGame


def draw_welcome(manager: pygame_gui.UIManager, screen: pygame.Surface, wasBadInput: bool = False, text_only: bool = False) -> tuple[pygame_gui.elements.UITextEntryBox, pygame_gui.elements.UIButton] | None:
    """Draws the games' welcome screen, which allows the user to enter a number of mines and start the game

    Args:
        manager (pygame_gui.UIManager): The pygame_gui UIManager instance handling this
        screen (pygame.Surface): The screen to draw on
        wasBadInput (bool, optional): Whether the last mine count the user entered was bad. Defaults to False.
        text_only (bool, optional): Whether to draw the screen. Defaults to False.

    Returns:
        tuple[pygame_gui.elements.UITextEntryBox, pygame_gui.elements.UIButton] | None: None if text_only, else instances of the game's mine count box and start button
    """
    if text_only:
        screen.fill((0, 0, 0))

        # title
        title_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE + 12)
        title_surface = title_font.render("Welcome to Minesweeper", True, (255, 255, 0))
        screen.blit(title_surface, ((WINDOW_WIDTH - title_surface.get_width()) // 2, 60))

        #help text
        help_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        lines = HELP_TEXT.split('\n')
        for i, line in enumerate(lines):
            text_surface = help_font.render(line, True, (200, 200, 200))
            screen.blit(text_surface, (50, 140 + i * 30))

        # Print a message to enter 10-20 mines, or an error message if they tried to put in an invalid input
        minesText = help_font.render(NUM_MINES_TEXT, True, (200, 200, 200)) if not wasBadInput else help_font.render(MINES_ERROR_BAD_INPUT_TEXT, True, (200, 50, 50))
        screen.blit(minesText, (WINDOW_WIDTH // 2 - 100, 330))

        manager.draw_ui(screen)

    else:
        #bomb input box 
        textbox = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 100, 350), (200, 30)),
            manager=manager
        )

        # Start game button
        start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 50, 400), (100, 40)),
            text='Start Game',
            manager=manager
        )

        return textbox, start_button

from config import CELL_SIZE, COLOR_1_NEAR_MINE, COLOR_2_NEAR_MINE, COLOR_3_NEAR_MINE, COLOR_4_NEAR_MINE,COLOR_5_NEAR_MINE, COLOR_6_NEAR_MINE, COLOR_7_NEAR_MINE,COLOR_8_NEAR_MINE,COLOR_CELL_COVERED,COLOR_CELL_FLAGGED,COLOR_CELL_UNCOVERED,COLOR_CELL_MINE,COLOR_GRID_LINES

def draw_board(manager: pygame_gui.UIManager, screen: pygame.Surface, board: BoardGame):
    font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

    for y, row in enumerate(board.board):
        for x, cell in enumerate(row):
            rect = pygame.Rect(
                GRID_POS_X + x * CELL_SIZE,
                GRID_POS_Y + y * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )

            if not cell.is_revealed:
                if cell.is_flag:
                    pygame.draw.rect(screen, COLOR_CELL_FLAGGED, rect)
                    flag_text = font.render("F", True, (0, 0, 0))
                    screen.blit(flag_text, (rect.x + 5, rect.y + 2))
                else:
                    pygame.draw.rect(screen, COLOR_CELL_COVERED, rect)
            else:
                if cell.is_mine:
                    pygame.draw.rect(screen, COLOR_CELL_MINE, rect)
                    mine_text = font.render("M", True, (0, 0, 0))
                    screen.blit(mine_text, (rect.x + 5, rect.y + 2))
                elif cell.adjacent_mines > 0:
                    pygame.draw.rect(screen, COLOR_CELL_UNCOVERED, rect)
                    num_color = get_number_color(cell.adjacent_mines)
                    num_text = font.render(str(cell.adjacent_mines), True, num_color)
                    screen.blit(num_text, (rect.x + 5, rect.y + 2))
                else:
                    pygame.draw.rect(screen, COLOR_CELL_UNCOVERED, rect)

            pygame.draw.rect(screen, COLOR_GRID_LINES, rect, 1)

    # Flags remaining
    flags_left = board.total_mines - board.used_flags
    flags_text = font.render(f"Flags Left: {flags_left}", True, (255, 255, 255))
    screen.blit(flags_text, (FLAGS_REMAINING_X, FLAGS_REMAINING_Y)) 

    manager.draw_ui(screen)

    message_font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    message_y = GRID_POS_Y + len(board.board) * CELL_SIZE + 20 

    if board.phase == "playing":
        lines = HELP_TEXT.split('\n')
        for i, line in enumerate(lines):
            help_text_surface = message_font.render(line, True, (200, 200, 200))
            screen.blit(help_text_surface, (50, message_y + i * 30))

    elif board.phase == "lost":
        lost_text_surface = message_font.render(LOST_TEXT, True, (255, 0, 0))
        screen.blit(lost_text_surface, ((WINDOW_WIDTH - lost_text_surface.get_width()) // 2, message_y))

    elif board.phase == "won":
        won_text_surface = message_font.render(WON_TEXT, True, (0, 255, 0))
        screen.blit(won_text_surface, ((WINDOW_WIDTH - won_text_surface.get_width()) // 2, message_y))



def get_number_color(number: int):
    return {
        1: COLOR_1_NEAR_MINE,
        2: COLOR_2_NEAR_MINE,
        3: COLOR_3_NEAR_MINE,
        4: COLOR_4_NEAR_MINE,
        5: COLOR_5_NEAR_MINE,
        6: COLOR_6_NEAR_MINE,
        7: COLOR_7_NEAR_MINE,
        8: COLOR_8_NEAR_MINE,
    }.get(number, (255, 255, 255))