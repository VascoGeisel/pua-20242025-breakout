import pygame
import math
import random

class Ball(pygame.Rect):
    """
    A class to represent a ball that moves on the screen, inheriting from pygame.Rect.
    The ball is defined by its position, velocity, speed, radius, and color.

    Attributes:
    radius (int): The radius of the ball.
    speed (int): The speed at which the ball moves.
    color (str): The color of the ball (in a format pygame understands).
    diameter (int): The diameter of the ball (calculated from the radius).
    x (int): The x-coordinate of the ball's center.
    y (int): The y-coordinate of the ball's center.
    dx (float): The x-component of the direction vector (movement direction).
    dy (float): The y-component of the direction vector (movement direction).
    """

    def __init__(self, x, y, radius=15, dx=0, dy=1, speed=5, color='white', collidables_list = None):
        """
        Initialize a new ball object with position, velocity, speed, and color.

        Parameters:
        x (int): The initial x-coordinate of the ball's center.
        y (int): The initial y-coordinate of the ball's center.
        radius (int, optional): The radius of the ball. Default is 15.
        dx (float, optional): The x-component of the direction vector. Default is 0.
        dy (float, optional): The y-component of the direction vector. Default is 1.
        speed (int, optional): The speed at which the ball moves. Default is 5.
        color (str, optional): The color of the ball. Default is 'white'.
        """
        if collidables_list == None:
            collidables_list = []

        self.collidables = collidables_list
        self.radius = int(radius)
        self.speed = speed
        self.color = color
        self.diameter = int(self.radius * 2)
        self.x = int(x)
        self.y = int(y)
        self.dx = dx
        self.dy = dy
        self.frames_since_collision = 0
        
        # rectangles in pygame are defined by the top-left corner and dimensions
        super().__init__(self.x - self.radius, 
                         self.y - self.radius, 
                         self.diameter, 
                         self.diameter)

    def draw(self, screen, show_box=False):
        """
        Draw the ball on the provided screen at its current position.

        Parameters:
        screen (pygame.Surface): The surface to draw the ball on.
        show_box (bool, optional): Whether to show the bounding box of the ball for debugging. Default is False.
        """
        pygame.draw.circle(screen, 
                           pygame.Color(self.color),
                           self.center, 
                           self.radius)
        
        if show_box:  # For collision debugging, show the bounding box
            pygame.draw.rect(screen, 
                             pygame.Color('white'), 
                             self,
                             1)  # last number is the box width

    def move(self):
        """
        Move the ball in the direction defined by the direction vector (dx, dy) at the specified speed.

        The direction vector (dx, dy) is normalized to ensure consistent movement speed, 
        and the ball's position is updated accordingly.
        """
        # Normalize the direction vector so that the movement per frame is given by self.speed
        num = math.sqrt(self.dx * self.dx + self.dy * self.dy)
        self.dx = self.dx / num
        self.dy = self.dy / num
        
        step_x = self.speed * self.dx
        step_y = self.speed * self.dy

        self.x += step_x
        self.y += step_y

    def __str__(self):
        """
        Returns a string representation of the ball's current state, including position and velocity.

        Returns:
        str: A string describing the ball's current position (x, y), direction (dx, dy), and speed.
        """
        return "ball: x={}, y={}, dx={}, dy={}, speed={}".format(self.x, self.y, self.dx, self.dy, self.speed)
    
    def collide(self, paddle, collidables_list = None, ):
        if collidables_list == None:
            collidables_list = self.collidables

        self.collidables = collidables_list

                ## Collision Detection / Reflection
        # TODO: Move into another class or at least funciton
        # TODO: normalize the ball movement Vector, so its not becomming infinitly fast
        # TODO: Make the Reflection not independent of the Speed of the Paddle
        # TODO: IMPORTANT! If ball collides in corner and should collide with both wall and ceiling, 15 frames of immunity are to large
        # This code will be moved to another potion in the future but for now it will remain here for ease of development
        
        self.frames_since_collision += 1                                     # increment the collision counter, so there wont be any colisions right after each other

        if self.frames_since_collision >= 15:                                # check for recent collision (15 is completly arbitrary, may change in the future)
            
                
            collision_index = self.collidelist(self.collidables) 
            if collision_index >= 0:                                    # chechs if Ball collides with any collidable objects
                print(f"A collision was detected, the last colision was {self.frames_since_collision} ago") 
                self.frames_since_collision = 0                              # reset counter
                for collidable_index in range(len(self.collidables)):                           # iterate over all the collidable objects
                    # pygame.draw.line(screen, (255, 0, 255), self.collidables[collision_index].get_edges()[collidable_index][0], objects[collision_index].get_edges()[collidable_index][1], 1) # only for debugging, draws outlines ob colided objects
                    if self.clipline(self.collidables[collision_index].get_edges()[collidable_index]):  # checks wich edge of collidable object ball collides with
                        if collidable_index == 0 or collidable_index == 4:                            # horizontal surfaces
                            # print(f"A Horziontal Surface was hit")
                            self.dx = self.dx
                            self.dy = -self.dy                  

                        elif collidable_index == 1 or collidable_index == 2:                          # vertical surfaces
                            # print(f"A vertical Surface was hit")      
                            self.dx = -self.dx
                            self.dy = self.dy
                        
                        if self.collidables[collision_index] == paddle:          # checks if paddle was hit
                            randomnumber = (random.randrange(-700, +700)+ random.randrange(-700, +700)) * 0.0001    # create displacement according to gaussian distribution around 0, so its clean
                            if paddle.mleft:
                                randomnumber = (random.randrange(-2000, 0)+ random.randrange(-2000, 0)) * 0.0001
                            elif paddle.mright:
                                randomnumber = (random.randrange(0, +2000)+ random.randrange(0, +2000)) * 0.0001

                            self.dx += randomnumber                     # changes dx of ball by random number 
                            print(f"The Paddle was hit, dx has been changed by {randomnumber}")

                        break                                           # DO NOT REMOVE Limits collisions per frame per ball by 1 
            
        