import pygame
import time
import sys
from pygame.locals import *
from settings import *
from node import Node

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