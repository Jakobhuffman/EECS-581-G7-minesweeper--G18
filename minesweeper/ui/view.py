#view.py
#Author: Delaney Gray
#Date: 9-08

import pygame
import pygame_gui
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FONT_NAME, FONT_SIZE, HELP_TEXT

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