import pygame
import random
import sys
import os
import math
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

class Wall(pygame.Rect):
    """
    A Class to represent any type of Wall or similar object that is able to reflect the ball but is itself immovable.

    Attributes:
    x (int): The x-coordinate of the paddle's top-left corner.
    y (int): The y-coordinate of the paddle's top-left corner.
    width (int): The width of the paddle.
    height (int): The height of the paddle.
    color (str): The color of the paddle (in a format pygame understands).

    """
    def __init__(self, x, y, width=50, height=10, color='white'):
        """
        Initialize a new Wall object with position, size and color.

        Parameters:
        x (int): The initial x-coordinate of the paddle's top-left corner.
        y (int): The initial y-coordinate of the paddle's top-left corner.
        width (int, optional): The width of the paddle. Default is 50.
        height (int, optional): The height of the paddle. Default is 10.
        color (str, optional): The color of the paddle. Default is 'white'.
        """
        self._x = x
        self._y = y
        super().__init__(x, y, width, height)
    
    def draw(self, screen):
        """
        Draw the paddle on the provided screen at its current position.

        Parameters:
        screen (pygame.Surface): The surface to draw the paddle on.
        """
        pygame.draw.rect(screen, 
                         pygame.Color(self.color), 
                         self)
    
    def __str__(self):
        """
        Return a string representation of the paddle's current state, including position and speed.

        Returns:
        str: A string describing the paddle's current position (x, y) and speed.
        """
        return "paddle: x={}, y={}".format(self.x, self.y)
    
    def get_edges(self):
        """
        Returns the four lines which define the edges of the Rectangle.
        The Order is: 
            1: Top Edge
            2: Top Right Corner

        Returns:
        List: A list discribing 4 Lines (the edges of the Object) each made up of 2 lists discribing a point
        """
        self.top_edge = [self.topleft, self.topright]
        self.right_edge = [self.topright, self.bottomright]
        self.left_edge = [self.topleft, self.bottomleft]
        self.bottom_edge = [self.bottomleft, self.bottomright]

        return self.top_edge, self.right_edge, self.left_edge, self.bottom_edge
        