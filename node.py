import pygame
import time
import sys
from pygame.locals import *
from settings import *

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