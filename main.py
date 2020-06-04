import pygame
import time
import sys
from pygame.locals import *
from pathfinding import Pathfinding
from node import Node
from grid import Grid
from settings import *

def main():
    flags = FULLSCREEN | DOUBLEBUF
    screen = pygame.display.set_mode(SCREEN_SIZE, flags)
    screen.fill((0,0,0))
    grid = Grid(screen)
    finding = Pathfinding()
    screen.set_alpha(None)
    pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    start_alg = False

    # Booleans to determine if keys are pressed down
    shift_pressed = False
    q_key_pressed = False
    w_key_pressed = False


    while True:

        for event in pygame.event.get():
            # Handle exit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            pressed = pygame.key.get_pressed()

            # Toggle key booleans
            if event.type == pygame.KEYDOWN:
                if pressed[pygame.K_LSHIFT]:
                    shift_pressed = True
                if pressed[pygame.K_q]:
                    q_key_pressed = True
                if pressed[pygame.K_w]:
                    w_key_pressed = True
            if event.type == pygame.KEYUP:
                if pressed[pygame.K_LSHIFT] == False:
                    shift_pressed = False
                if pressed[pygame.K_q] == False:
                    q_key_pressed = False
                if pressed[pygame.K_w] == False:
                    w_key_pressed = False

            # Start selected algorithm
            if pressed[pygame.K_RETURN] and grid.start_node and grid.end_node:
                start_alg = True
                finding.open_list.add(grid.start_node)

            # Clear grid
            if pressed[pygame.K_SPACE]:
                grid.empty_grid(screen)
                finding = Pathfinding()

            # Exit application
            if pressed[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()

        # Change nodes under where mouse clicked
        if pygame.mouse.get_pressed()[0]:
            if shift_pressed:   # Erase node
                grid.update_node(event, 'blank')
            elif q_key_pressed: # Start Node
                grid.update_node(event, 'start')
            elif w_key_pressed: # End Node
                grid.update_node(event, 'end')
            else:               # Wall Node
                grid.update_node(event, 'wall')

        # Continue pathfinding algorithm if not finished
        if start_alg:
            finding.continue_pathfinding(grid)

        if finding.finished:
            # Draw result path
            for i in range(len(finding.path)):
                if i == 0 or i == len(finding.path) - 1:
                    continue
                node = finding.path[i]
                grid.draw_node(node[0], node[1], 'path')

            start_alg = False
            finding.finished = False


        pygame.display.flip() # Update display


if __name__ == "__main__":
    main()


