import pygame
import pygame_gui
import config
import sys
from minesweeper.ui.view import draw_welcome
from minesweeper.board import BoardGame


pygame.init()

screen=pygame.display.set_mode((config.WINDOW_WIDTH ,config.WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")
clock=pygame.time.Clock()
manager = pygame_gui.UIManager((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
board = BoardGame()
text_box, start_button = draw_welcome(manager, screen)


running=True
while running:
    dt = clock.tick(config.FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == start_button:
            print("Start clicked. Mines:", text_box.get_text())
            board.phase = 'playing'
            text_box.hide()
            start_button.hide()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                L_click_pos=event.pos
                print(L_click_pos)
            if event.button == 3:
                R_click_pos=event.pos
                print(R_click_pos)

    manager.update(dt)
    if (board.phase == 'ready'):
        draw_welcome(manager, screen, True)

    if (board.phase == 'playing'):
        screen.fill((0, 0, 0)) # This will be the call to draw_board

    pygame.display.flip()

    clock.tick(config.FPS)

pygame.quit()
sys.exit()