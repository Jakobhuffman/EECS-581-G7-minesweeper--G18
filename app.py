# app.py
# Controls the execution flow of the game
# Inputs: Accepts mouse/keyboard inputs through a GUI; no other inputs
# Outputs: None
# Authors: Michael Buckendahl, C. Cooper, Blake J
# Creation Date: 08/25/2025

import pygame
import pygame_gui
import config
import sys
from minesweeper.ui.view import draw_welcome, draw_board, draw_ai_selection
from minesweeper.board import BoardGame
from minesweeper.ai_solver import AISolver


pygame.init()

# Creates the window in which the game will run
screen=pygame.display.set_mode((config.WINDOW_WIDTH ,config.WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper") # simple window title
clock=pygame.time.Clock() # sets up a clock to manage how fast the screen updates

# Sets up the pygame_gui UIManager which will handle UI elements that we use to get
# the mine count and create a button to start the game
manager = pygame_gui.UIManager((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

board: BoardGame = BoardGame()

# The draw_welcome function has two modes, one to draw the screen and one to create the UI
# elements. Here we call it to create the UI elements and get references to them. We do this outside
# the main loop so that we only create them once.
text_box, _ = draw_welcome(manager, screen, False, False)
ai_text, start_button, easy_button, medium_button, hard_button = draw_ai_selection(manager)
ai_buttons = {easy_button: 'easy', medium_button: 'medium', hard_button: 'hard', start_button: None}
all_welcome_elements = [text_box, ai_text, start_button, easy_button, medium_button, hard_button]
ai_solver: AISolver = None
selected_button = None
player_turn = True
ai_move_timer = 0

# Whether the last text the player entered in the bomb number box was invalid
wasBadInput: bool = False

running=True
while running:
    dt = clock.tick(config.FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            break

        # This is a call to the UIManager to handle any UI events for the elements it is managing
        # (the text box and button in this case). Note that we are not assigning the result of this call
        # to anything, as we don't need to. This is a side-effect call, it just processes the event and
        # updates the managers internal state.
        manager.process_events(event)
        
        # If a UI button was pressed
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Try to get the mine count from the text box and start the game
            try:
                mineCount = int(text_box.get_text())
                if config.MIN_MINES <= mineCount <= config.MAX_MINES:
                    wasBadInput = False
                    # Update button visuals for selection
                    if selected_button:
                        selected_button.unselect()
                    selected_button = event.ui_element
                    selected_button.select()

                    if event.ui_element in ai_buttons:
                        difficulty = ai_buttons[event.ui_element]
                        board = BoardGame()
                        board.total_mines = mineCount
                        player_turn = True

                        if difficulty:
                            board.phase = 'ai'
                            ai_solver = AISolver(board, difficulty)
                        else:
                            board.phase = 'playing'
                            ai_solver = None
                        
                        for element in all_welcome_elements:
                            element.hide()
                        if selected_button:
                            selected_button.unselect() # Deselect for next time menu is shown
                else:
                    wasBadInput = True
            except: # If it couldn't be converted to an int, print an error
                wasBadInput = True
        # If the mouse was clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # If we aren't in a player-controlled phase, ignore the click
            if board.phase not in ["playing", "ai"] or (board.phase == 'ai' and not player_turn):
                continue

            # Get the cell position of the click
            gridPositionX = event.pos[0] - config.GRID_POS_X
            gridPositionY = event.pos[1] - config.GRID_POS_Y

            cellX = gridPositionX // config.CELL_SIZE
            cellY = gridPositionY // config.CELL_SIZE

            # If the click was outside the cell grid, ignore it
            if cellX < 0 or cellX >= config.GRID_COLS or cellY < 0 or cellY >= config.GRID_ROWS:
                continue

            # If it was left clicked, reveal the cell
            if event.button == 1:
                board.reveal(cellX, cellY)
                if board.phase == 'ai':
                    player_turn = False # AI's turn now

            # If it was right clicked, toggle the flag of the cell
            if event.button == 3:
                board.toggle_flag(cellX, cellY)

        # If a key was pressed
        if event.type == pygame.KEYDOWN:
            # If the pressed key was R and the game is over or being played
            if event.key == pygame.K_r and (board.phase in ["playing", "won", "lost", "ai"]):
                # Restart the game
                mineCount = board.total_mines
                is_ai_game = ai_solver is not None
                difficulty = ai_solver.difficulty if is_ai_game else None

                board = BoardGame()
                board.total_mines = mineCount
                player_turn = True

                if is_ai_game:
                    board.phase = 'ai'
                    ai_solver = AISolver(board, difficulty)
                else:
                    board.phase = 'playing'
                    ai_solver = None
            # If the game is over and they press escape, go back to the welcome screen
            elif event.key == pygame.K_ESCAPE and (board.phase in ["won", "lost"]):
                board.phase = "ready"
                player_turn = True
                ai_solver = None
                for element in all_welcome_elements:
                    element.show()
                if selected_button:
                    selected_button.unselect()

    manager.update(dt)

    if board.phase == 'ai' and not player_turn and board.phase not in ['won', 'lost']:
        ai_move_timer += dt
        if ai_move_timer > 0.5: # Add a small delay for the AI move
            if ai_solver:
                ai_solver.make_move()
            player_turn = True # Player's turn again
            ai_move_timer = 0

    if (board.phase == 'ready'):
        # Redraw welcome screen but don't create new elements
        draw_welcome(manager, screen, wasBadInput, True)

    if (board.phase in ['playing', 'won', 'lost', 'ai']):
        screen.fill((0, 0, 0)) # This will be the call to draw_board
        draw_board(manager, screen, board)

    pygame.display.flip()

    clock.tick(config.FPS)

pygame.quit()
sys.exit()
