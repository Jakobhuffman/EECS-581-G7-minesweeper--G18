import pygame
import pygame_gui
import config
import sys


pygame.init()

screen=pygame.display.set_mode((config.WINDOW_WIDTH ,config.WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")
clock=pygame.time.Clock()

running=True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                L_click_pos=event.pos
                print(L_click_pos)
            if event.button == 3:
                R_click_pos=event.pos
                print(R_click_pos)


    screen.fill(config.COLOR_BACKGROUND)

    pygame.display.flip()

    clock.tick(config.FPS)

pygame.quit()
sys.exit()