from objects.wall import Wall

# do not import any other modules (not all of them are used in this template)
import pygame
import random
import sys
import os
import math
from pathlib import Path
from datetime import datetime
import pandas as pd
import numpy as np

class Brick(Wall):
    """
    A Class to represent the Bricks that sould be destroyed by the Player
    Tihs ist WIP so there are no funcitons so far
    """
    def __init__(self, x, y, width=50, height=10):
        """
        Initialize a new Brick object with position, size and color.

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
    
