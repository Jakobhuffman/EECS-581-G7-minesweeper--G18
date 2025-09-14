# app.py
# Controls the execution flow of the game
# Authors: Michael Buckendahl, C. Cooper, Blake J
# Creation Date: 08/25/2025

import pygame
import pygame_gui
import config
import sys
from minesweeper.ui.view import draw_welcome, draw_board
from minesweeper.board import BoardGame


pygame.init()

screen=pygame.display.set_mode((config.WINDOW_WIDTH ,config.WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")
clock=pygame.time.Clock()
manager = pygame_gui.UIManager((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
board: BoardGame = BoardGame()
text_box, start_button = draw_welcome(manager, screen)


running=True
while running:
    dt = clock.tick(config.FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            break

        manager.process_events(event)

        # If the start button was clicked
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == start_button:
            # Try to get the mine count from the text box and start the game
            try:
                mineCount = int(text_box.get_text())

                # If the count is within the mine bounds, start the game
                if(config.MIN_MINES <= mineCount <= config.MAX_MINES):
                    print("Start clicked. Mines:", str(mineCount))
                    board = BoardGame()
                    board.total_mines = mineCount
                    board.phase = 'playing'
                    text_box.hide()
                    start_button.hide()
                else:
                    print(f"Bad mine count: {mineCount}")
            except: # If it couldn't be converted to an int, print an error
                print("Bad mine count:", text_box.get_text())

        # If the mouse was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # If we aren't playing, ignore the click
            if board.phase != "playing":
                continue

            # Get the cell position of the click
            gridPositionX = event.pos[0] - config.GRID_POS_X
            gridPositionY = event.pos[1] - config.GRID_POS_Y

            cellX = gridPositionX // config.CELL_SIZE
            cellY = gridPositionY // config.CELL_SIZE

            # If the click was outside the cell grid, ignore it
            if cellX < 0 or cellX >= config.GRID_COLS or cellY < 0 or cellY >= config.GRID_ROWS:
                continue

            print(f"Clicked on cell {cellX}, {cellY}")

            # If it was left clicked, reveal the cell
            if event.button == 1:
                board.reveal(cellX, cellY)

            # If it was right clicked, toggle the flag of the cell
            if event.button == 3:
                board.toggle_flag(cellX, cellY)

        # If a key was pressed
        if event.type == pygame.KEYDOWN:
            # If the pressed key was R and the game is being played
            if event.key == pygame.K_r and (board.phase == "playing" or board.phase == "won" or board.phase == "lost"):
                # Restart the game
                mineCount = board.total_mines
                board = BoardGame()
                board.total_mines = mineCount
                board.phase = "playing"
                print(f"Restarted game with {mineCount} mines.")
            
            # If the game is over and they press escape, go back to the welcome screen
            elif event.key == pygame.K_ESCAPE and (board.phase == "won" or board.phase == "lost"):
                board.phase = "ready"
                text_box.show()
                start_button.show()

    manager.update(dt)
    if (board.phase == 'ready'):
        draw_welcome(manager, screen, True)

    if (board.phase == 'playing' or board.phase == "won" or board.phase == "lost"):
        screen.fill((0, 0, 0)) # This will be the call to draw_board
        draw_board(manager, screen, board)

    pygame.display.flip()

    clock.tick(config.FPS)

pygame.quit()
sys.exit()