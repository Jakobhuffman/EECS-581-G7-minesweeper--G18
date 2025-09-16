#view.py
#Author: Delaney Gray
#Date: 9-08

import pygame
import pygame_gui
from config import WINDOW_WIDTH, FONT_NAME, FONT_SIZE, HELP_TEXT, CELL_SIZE, GRID_POS_X, GRID_POS_Y, FLAGS_REMAINING_X, FLAGS_REMAINING_Y
    
from minesweeper.board import BoardGame


def draw_welcome(manager, screen, text_only=False):
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