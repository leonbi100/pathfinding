import pygame
import time
import sys
from pygame.locals import *


# GLOBAL VARS
SCREEN_SIZE = (750, 750)    
GRID_SIZE = (30, 30)
GRID_MARGIN = 1
NODE_SIZE = (SCREEN_SIZE[0] / GRID_SIZE[0], SCREEN_SIZE[1] / GRID_SIZE[1])


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
COLORS_DICT = {'blank': WHITE, 'start': GREEN, 'end': RED, 'wall': BLACK, 'path': YELLOW, 'child': BLUE}

class Grid:
    def __init__(self, screen):
        self.nodes = [[]]
        self.screen = screen
        self.start_node = None
        self.end_node = None

        self.empty_grid(screen)

    def empty_grid(self, screen):
        """ Clears the grid and sets all values in 2D array to be blank Nodes."""

        self.nodes = [[Node('blank', x, y) for x in range(GRID_SIZE[0])] for y in range(GRID_SIZE[1])]

        for y in range(GRID_SIZE[1]):
            for x in range(GRID_SIZE[0]):
                self.draw_node(x, y, 'blank')

    def draw_node(self, x_val, y_val, node_type):
        """ 
        Sets Node at x, y coordinate to be value node_type and draws
        corresponding color on screen.
        """

        self.nodes[y_val][x_val].set_node(node_type)
        color = COLORS_DICT[node_type]

        pygame.draw.rect(self.screen, color, 
            [(NODE_SIZE[0] + GRID_MARGIN) * x_val + GRID_MARGIN, 
            (NODE_SIZE[1] + GRID_MARGIN) * y_val + GRID_MARGIN, 
            NODE_SIZE[0], NODE_SIZE[1]])

    def update_node(self, event, node_type):
        """
        Changes node under current mouse position to node corresponding
        to user input.

        q_key = start node
        w_key = end node
        shift_key = blank node (erase) 
        """
    
        pos = pygame.mouse.get_pos()
        x_val = int((pos[0] - 18) / NODE_SIZE[0])
        y_val = int((pos[1] - 15) / NODE_SIZE[1])

        # replace old start and end nodes
        if node_type == 'start':
            if self.start_node != None:
                coor = self.start_node.get_coor()
                self.draw_node(coor[0], coor[1], 'blank')
                self.start_node = Node('blank', x_val, y_val)
            else:
                self.start_node = Node('start', x_val, y_val)
        if node_type == 'end':
            if self.end_node != None:
                coor = self.end_node.get_coor()
                self.draw_node(coor[0], coor[1], 'blank')
                self.end_node = Node('blank', x_val, y_val)
            else:
                self.end_node = Node('end', x_val, y_val)

        # Consider case where wall is written over start or end node
        if node_type == 'wall' and self.start_node != None:
            if self.start_node.get_coor() == (x_val, y_val):
                self.start_node = None

        if node_type == 'wall' and self.end_node != None:
            if self.end_node.get_coor() == (x_val, y_val):
                self.end_node = None

        self.draw_node(x_val, y_val, node_type)


class Node:
    def __init__(self, node_type, x, y):
        self.x = x
        self.y = y
        self.node_type = node_type
        self.color = COLORS_DICT[node_type]
        
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def set_node(self, node_type):
        self.node_type = node_type
        self.color = COLORS_DICT[node_type]

    def get_type(self):
        return self.node_type

    def get_color(self):
        return self.color

    def get_coor(self):
        return (self.x, self.y)


class Pathfinding:

    def __init__(self):
        self.open_list = set()
        self.closed_list = set()
        self.finished = False
        self.path = []

    def continue_pathfinding(self, grid):
            # Finished
            if len(self.open_list) <= 0:
                self.finished = True
                return None

            # Find node with least f value
            current_node = min(self.open_list, key=lambda n: n.f)
            self.open_list.remove(current_node)
            self.closed_list.add(current_node)

            # Found end node and return
            if current_node.get_coor() == grid.end_node.get_coor():
                path = []
                curr = current_node
                while curr != None:
                    path.append(curr.get_coor())
                    curr = curr.parent
                self.finished = True
                self.path = path

            # Look at all adjacent child nodes
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
                child_pos = (current_node.get_coor()[0] + new_position[0], current_node.get_coor()[1] + new_position[1])

                # Make sure in grid
                if child_pos[0] > (len(grid.nodes) - 1) or child_pos[0] < 0 or child_pos[1] > (len(grid.nodes[0]) -1) or child_pos[1] < 0:
                    continue

                # Make sure not wall
                if grid.nodes[child_pos[1]][child_pos[0]].get_type() == 'wall':
                    # change color to indicate hit wall?
                    continue

                skip = False
                for node in self.closed_list:
                    if node.get_coor() == child_pos:
                        skip = True
                        break
                if skip:
                    continue

                # Create new node
                new_child = Node('blank', child_pos[0], child_pos[1])
                new_child.parent = current_node
                children.append(new_child)

            # Loop through children
            for child in children:

                # Make sure child not in closed list
                if child in self.closed_list:
                    continue

                # Calculate f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.get_coor()[0] - grid.end_node.get_coor()[0]) ** 2) + ((child.get_coor()[1] - grid.end_node.get_coor()[1]) ** 2)
                child.f = child.g + child.h

                # Child in open list
                skip = False
                for open_node in self.open_list:
                    if child == open_node and child.g >= open_node.g:
                        skip = True
                        break
                if skip:
                    self.closed_list.add(child)
                    continue

                self.open_list.add(child)
                if child.get_coor() != grid.start_node.get_coor() and child.get_coor() != grid.end_node.get_coor():
                    grid.draw_node(child.get_coor()[0], child.get_coor()[1], 'child')

            pygame.display.flip()


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


