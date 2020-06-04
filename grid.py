import pygame
import time
import sys
from pygame.locals import *
from node import Node
from settings import *

class Grid:
    def __init__(self, screen):
        self.nodes = [[]]
        self.screen = screen
        self.start_node = None
        self.end_node = None

        self.empty_grid(screen)

    def empty_grid(self, screen):
        """ Clears the grid and sets all values in 2D array to be blank Nodes."""
        self.start_node = None
        self.end_node = None
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