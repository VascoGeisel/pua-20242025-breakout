import pygame

class Paddle(pygame.Rect):
    """
    A class to represent a paddle that can move left or right within screen boundaries.
    It inherits from pygame.Rect to handle position and size, and includes functionality for drawing and moving.

    Attributes:
    x (int): The x-coordinate of the paddle's top-left corner.
    y (int): The y-coordinate of the paddle's top-left corner.
    width (int): The width of the paddle.
    height (int): The height of the paddle.
    speed (int): The speed at which the paddle moves.
    color (str): The color of the paddle (in a format pygame understands).
    """

    def __init__(self, x, y, width=50, height=10, speed=10, color='white'):
        """
        Initialize a new paddle object with position, size, speed, and color.

        Parameters:
        x (int): The initial x-coordinate of the paddle's top-left corner.
        y (int): The initial y-coordinate of the paddle's top-left corner.
        width (int, optional): The width of the paddle. Default is 50.
        height (int, optional): The height of the paddle. Default is 10.
        speed (int, optional): The speed at which the paddle moves. Default is 10.
        color (str, optional): The color of the paddle. Default is 'white'.
        """
        self._x = x
        self._y = y
        super().__init__(x, y, width, height)

        self.speed = speed
        self.color = color

    def draw(self, screen):
        """
        Draw the paddle on the provided screen at its current position.

        Parameters:
        screen (pygame.Surface): The surface to draw the paddle on.
        """
        pygame.draw.rect(screen, 
                         pygame.Color(self.color), 
                         self)

    def move_left(self):
        """
        Move the paddle left by its speed, ensuring it does not go past the left edge of the screen.

        This method checks if the paddle's left edge is greater than 0 (left boundary), 
        and if so, moves the paddle left by `self.speed`.
        """
        if self.left > 0:  # Don't move more than the left boundary
            self.move_ip(-self.speed, 0)  # Move in place (relative movement)

    def move_right(self, screen):
        """
        Move the paddle right by its speed, ensuring it does not go past the right edge of the screen.

        Parameters:
        screen (pygame.Surface): The surface to check the width of the screen for the right boundary.
        """
        if self.right < screen.get_width():  # Don't move more than the right boundary
            self.move_ip(self.speed, 0)

    def __str__(self):
        """
        Return a string representation of the paddle's current state, including position and speed.

        Returns:
        str: A string describing the paddle's current position (x, y) and speed.
        """
        return "paddle: x={}, y={}, speed={}".format(self.x, self.y, self.speed)
