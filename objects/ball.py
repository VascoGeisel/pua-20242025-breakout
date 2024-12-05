import pygame
import math
import random
from objects.brick import Brick

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
        self.allow_collisions = [1]*len(self.collidables)
        print(self.allow_collisions)
        self.radius = int(radius)
        self.speed = speed
        self.color = color
        self.diameter = int(self.radius * 2)
        self.width = self.diameter
        self.height = self.diameter
        self.x = int(x)
        self.y = int(y)
        self.dx = dx
        self.dy = dy
        self.dx_old = dx
        self.dy_old = dy
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

        self.dy_old = self.dy
        self.dx_old = self.dx
        
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
    
    def setCollidables(self, collidables_list = None):
        """
        Sets the List of Collidable Objects to the given List (there ist also an add funciton)

        Parameters:
            list: a list of wich objects the Collidables should be set to
        """
        if collidables_list == None:
            collidables_list = self.collidables

        if self in collidables_list:
            collidables_list.remove(self)
            print(f"removed self list ist: {collidables_list}")

        self.collidables = collidables_list
        self.allow_collisions = [1]*len(self.collidables)
        print(self.allow_collisions)

    def addCollidables(self, collidables_list = None):
        """
        Not reliable yet
        Adds to the list of collidable Objects the given list

        Parameters:
            list: a list of wich objects to add to the collidables 
        """
        if collidables_list == None:
            return
        
        for i in collidables_list:
            if i not in self.collidables:
                self.collidables.append(i)

        if self in collidables_list:
            collidables_list.remove(self)
            print(f"removed self list ist: {collidables_list}")
        
        self.collidables = collidables_list
        self.allow_collisions = [1]*len(self.collidables)

    def removeCollidables(self, to_remove):
        """
        not reliable yet
        removes a given object (only one at a time) form the collidable objecs

        Parameters:
            object: object that sould be removed from the collidable objects
        
        Error:
            ValueError: 
                if the given object ist not in the collidable ist
        """
        if to_remove in self.collidables:
            self.collidables.remove(to_remove)
        else:
            raise ValueError(f"{to_remove} is not in Collidables, cannot remove if not present")
        
        self.allow_collisions = [1]*len(self.collidables)




    def collide(self, paddle, screen, debugging = False):
        """
        Collides the Ball with any other Obejct in the collidables list

        Parameters: 
            paddle : 
                the Paddel to check for the possible movement of the Paddel

            screen :
                to display the edges the ball bounces off of

            bool: 
                set debugging = True to enable debugging Standard is False
        
        """
        ## Collision Detection / Reflection
        # TODO: normalize the ball movement Vector, so its not becomming infinitly fast - Not neccesary
        
            
        collision_index = self.collidelist(self.collidables) 
        

        if collision_index >= 0:                                    # chechs if Ball collides with any collidable objects
            if self.allow_collisions[collision_index]:              # checks if the Collision is a repetiotion
                if type(self.collidables[collision_index]) != Ball:
                    self.frames_since_collision = 0                              # reset counter
                    for collidable_index in [0, 3, 1, 2]:                         # iterate over all the collidable objects
                        if debugging:
                            pygame.draw.line(screen, (255, 0, 255), self.collidables[collision_index].get_edges()[collidable_index][0], self.collidables[collision_index].get_edges()[collidable_index][1], 8) # only for debugging, draws outlines ob colided objects
                        if self.clipline(self.collidables[collision_index].get_edges()[collidable_index]):  # checks wich edge of collidable object ball collides with
                            print(f"clips with colidable_index: {collidable_index}")
                            if collidable_index == 0 or collidable_index == 3:                            # horizontal surfaces
                                # print(f"A Horziontal Surface was hit")
                                self.dx = self.dx
                                self.dy = -self.dy       

                                self.dy_old = self.dy
                                self.dx_old = self.dx           

                            elif collidable_index == 1 or collidable_index == 2:                          # vertical surfaces
                                # print(f"A vertical Surface was hit")     
                                print(type(self.collidables[collision_index]))
                                self.dx = -self.dx
                                self.dy = self.dy

                                self.dy_old = self.dy
                                self.dx_old = self.dx
                            
                            if self.collidables[collision_index] == paddle:          # checks if paddle was hit
                                randomnumber = (random.randrange(-700, +700)+ random.randrange(-700, +700)) * 0.0001    # create displacement according to gaussian distribution around 0, so its clean
                                if paddle.mleft:
                                    randomnumber = (random.randrange(-2000, 0)+ random.randrange(-2000, 0)) * 0.0001    # create a displacement (gaussian) depending on movement of paddle
                                elif paddle.mright:
                                    randomnumber = (random.randrange(0, +2000)+ random.randrange(0, +2000)) * 0.0001

                                self.dx += randomnumber
                                self.dx_old = self.dx                     # changes dx of ball by random number 
                                print(f"The Paddle was hit, dx has been changed by {randomnumber}")

                            # break                                           # DO NOT REMOVE Limits collisions per frame per ball by 1 

                else:
                    print("Collision with ball")
                    self.dx_old = self.dx
                    self.dy_old = self.dy
                    self.dx = self.collidables[collision_index].dx_old
                    self.dy = self.collidables[collision_index].dy_old
                    pass
            else:
                for i in range(len(self.allow_collisions)):
                    if i != collision_index:
                        self.allow_collisions[i] = 1

            self.allow_collisions[collision_index] = 0      # sets collision list to 0 to avoid repetioton
            print(self.allow_collisions)                    
        
        else:                                               # resets repetiotion list
            for i in range(len(self.allow_collisions)):
                self.allow_collisions[i] = 1

    def get_edges(self):
        """
        Returns the four lines which define the edges of the Rectangle.
        The Order is: 
            1: Top Edge
            2: Right Edge
            3: Left Edge
            4: Bottom Edge

        Returns:
        List: A list discribing 4 Lines (the edges of the Object) each made up of 2 lists discribing a point
        """
        self.top_edge = [self.topleft, self.topright]
        self.right_edge = [self.topright, self.bottomright]
        self.left_edge = [self.topleft, self.bottomleft]
        self.bottom_edge = [self.bottomleft, self.bottomright]

        print(self.top_edge, self.right_edge, self.left_edge, self.bottom_edge)

        return self.top_edge, self.right_edge, self.left_edge, self.bottom_edge
        