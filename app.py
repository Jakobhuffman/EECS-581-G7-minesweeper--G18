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

# --- Game Difficulty (board size/mines) ---
# Create clearly-labeled Game Difficulty (separate from AI Difficulty)
# Position the game difficulty controls below the AI buttons to avoid overlap
label_y = config.AI_BUTTON_Y + 40
game_diff_label = pygame_gui.elements.UITextBox(
    html_text="<b>Game Difficulty</b> (board size & mines)",
    relative_rect=pygame.Rect((0, label_y), (config.WINDOW_WIDTH, 30)),
    manager=manager,
    object_id='#game_diff_text'
)
button_width = 100
button_spacing = 20
total_width = button_width * 3 + button_spacing * 2
start_x = config.WINDOW_WIDTH // 2 - total_width // 2
# place the difficulty buttons beneath the label
game_diff_y = label_y + 40

gd_easy_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((start_x, game_diff_y), (button_width, 30)),
    text='Easy',
    manager=manager
)
gd_normal_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((start_x + (button_width + button_spacing), game_diff_y), (button_width, 30)),
    text='Normal',
    manager=manager
)
gd_hard_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((start_x + 2 * (button_width + button_spacing), game_diff_y), (button_width, 30)),
    text='Hard',
    manager=manager
)

current_difficulty = 'normal'
config.set_difficulty(current_difficulty)
gd_normal_button.disable()

ai_buttons = {easy_button: 'easy', medium_button: 'medium', hard_button: 'hard', start_button: None}
all_welcome_elements = [text_box, ai_text, start_button, easy_button, medium_button, hard_button]
ai_solver: AISolver = None
selected_button = None
player_turn = True
ai_move_timer = 0

# Whether the last text the player entered in the bomb number box was invalid
wasBadInput: bool = False

running = True

while running:
    dt = clock.tick(config.FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # Let the UI manager process events for its widgets
        manager.process_events(event)

        # Handle UI button events
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Game difficulty buttons
            if event.ui_element == gd_easy_button:
                config.set_difficulty('easy')
                gd_easy_button.disable(); gd_normal_button.enable(); gd_hard_button.enable()
                continue
            if event.ui_element == gd_normal_button:
                config.set_difficulty('normal')
                gd_normal_button.disable(); gd_easy_button.enable(); gd_hard_button.enable()
                continue
            if event.ui_element == gd_hard_button:
                config.set_difficulty('hard')
                gd_hard_button.disable(); gd_easy_button.enable(); gd_normal_button.enable()
                continue

            # AI / Start buttons
            if event.ui_element in ai_buttons:
                # Attempt to parse mine count from textbox
                try:
                    mineCount = int(text_box.get_text())
                except Exception:
                    wasBadInput = True
                    continue

                if not (config.MIN_MINES <= mineCount <= config.MAX_MINES):
                    wasBadInput = True
                    continue

                wasBadInput = False
                # selected button visuals
                if selected_button:
                    try:
                        selected_button.unselect()
                    except Exception:
                        pass
                selected_button = event.ui_element
                try:
                    selected_button.select()
                except Exception:
                    pass

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

                # hide welcome UI
                game_diff_label.hide(); gd_easy_button.hide(); gd_normal_button.hide(); gd_hard_button.hide()
                for element in all_welcome_elements:
                    try:
                        element.hide()
                    except Exception:
                        pass

        # Mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If we aren't in a player-controlled phase, ignore the click
            if board.phase not in ["playing", "ai"] or (board.phase == 'ai' and not player_turn):
                continue

            # Convert pixel to cell coordinates
            grid_x = event.pos[0] - config.GRID_POS_X
            grid_y = event.pos[1] - config.GRID_POS_Y
            cell_col = grid_x // config.CELL_SIZE
            cell_row = grid_y // config.CELL_SIZE

            # If the click was outside the cell grid, ignore it
            if cell_col < 0 or cell_col >= config.GRID_COLS or cell_row < 0 or cell_row >= config.GRID_ROWS:
                continue

            # Left click -> reveal
            if event.button == 1:
                board.reveal(cell_row, cell_col)
                if board.phase == 'ai':
                    player_turn = False

            # Right click -> toggle flag
            if event.button == 3:
                board.toggle_flag(cell_row, cell_col)

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            # Restart (R)
            if event.key == pygame.K_r and (board.phase in ["playing", "won", "lost", "ai"]):
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

            # Escape -> go back to welcome
            if event.key == pygame.K_ESCAPE:
                board = BoardGame()
                # show welcome UI again
                try:
                    game_diff_label.show(); gd_easy_button.show(); gd_normal_button.show(); gd_hard_button.show()
                except Exception:
                    pass
                for element in all_welcome_elements:
                    try:
                        element.show()
                    except Exception:
                        pass
                ai_solver = None

    # Update the UI manager so widgets have a chance to animate / process internal state
    try:
        manager.update(dt)
    except Exception:
        pass

    # AI turn handling: if it's an AI game and it's AI's turn, allow a small timer then make a move
    if board.phase == 'ai' and ai_solver and not player_turn:
        ai_move_timer += dt
        if ai_move_timer > 0.3:
            ai_solver.make_move()
            player_turn = True
            ai_move_timer = 0

    if board.phase == 'ready':
        # Redraw welcome screen but don't create new elements
        draw_welcome(manager, screen, wasBadInput, True)

    if board.phase in ['playing', 'won', 'lost', 'ai']:
        screen.fill((0, 0, 0))
        draw_board(manager, screen, board)

    # Draw UI elements so buttons/textboxes are visible
    try:
        manager.draw_ui(screen)
    except Exception:
        pass

    pygame.display.flip()

pygame.quit()
sys.exit()
