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

# imports from custom classes
from objects.ball import Ball
from objects.paddle import Paddle
from objects.wall import Wall
from objects.brick import Brick
from objects.button import Button

# this code is from https://stackoverflow.com/questions/46698824/python-deep-copy-without-using-copy-module
# it was copied on 1.12.24 at 14:21 and has been altered to allow copy of any element in the list

def mydeepcopy(L):
    """
    Returns a deep Copy of the Given list 

    Parameters:
        list : any kind fo list, no matter how many dimensions

    Returns:
        list : a deep copy of the given list 
    """
    if isinstance(L, list):
        ret = []
        for i in L:
            ret.append(mydeepcopy(i))
    else:
        ret = L

    return ret

# end of copied code

if __name__ == '__main__':
    # initialize pygame
    pygame.init()
    pygame.font.init()

    # pygame setting variables
    FPS = 50

    # create a game screen
    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 700
    screen = pygame.display.set_mode(size=(DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # create fonts
    HEADLINE_FONT = pygame.font.Font(None, 64)
    NORMAL_FONT = pygame.font.Font(None, 32)

    # initialize the clock for FPS calculation
    clock = pygame.time.Clock()

    # initialize a ball
    ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red')

    # initialize a second ball
    ball2 = Ball(x = DISPLAY_WIDTH//2, y = 300, dx = 0, dy = -1, radius = 10, speed = 5, color='red')

    # initialize a paddle
    paddle_height = 10
    paddle_width = 50
    paddle = Paddle(DISPLAY_WIDTH//2, DISPLAY_HEIGHT-paddle_height-20, paddle_width, paddle_height)

    # Create the Perimiter of the Window
    ceiling = Wall(0, 0, DISPLAY_WIDTH, -20)
    rightwall = Wall(DISPLAY_WIDTH, 0, 20, DISPLAY_HEIGHT)
    leftwall = Wall(0, 0, -20, DISPLAY_HEIGHT)

    # Create a test Brick
    Brick1 = Brick(400, 400, 50, 50)

    # Create grid of Bricks
    def create_bricks(position_x=10, position_y=DISPLAY_HEIGHT/7, amount_per_row=10, amount_per_column=5, percent_height=0.2, distance=5, DISPLAY_WIDTH = DISPLAY_WIDTH,  DISPLAY_HEIGHT = DISPLAY_HEIGHT):
        """
        Generates any amount of bricks in a grid described by the parameters

        Parameters:
        position_x: The x-coordinate of the top left corner of the top left brick of the grid
        position_y: The y-coordinate of the top left corner of thetop left  brick of the grid
        width: The width of every brick
        height: The height of every brick
        amount_per_row: The amount of bricks per row of the grid
        amount_per_column: The amount of bricks per colum of the grid
        distance: The distance between neighbouring bricks

        Returns: list_of_bricks: Each brick including the position of its top left corner, width and height is returned as an element in this list
        """
        list_of_bricks =[]
        space_x_direction = DISPLAY_WIDTH - 2*position_x
        space_y_direction = DISPLAY_HEIGHT*percent_height
        if position_x+(amount_per_row+distance-1)*amount_per_row <= DISPLAY_WIDTH and position_y+(amount_per_column+distance-1)*amount_per_column <= DISPLAY_HEIGHT:
            for x_brick in range(0,amount_per_row,1):
                for y_brick in range(0,amount_per_column,1):
                    NewBrick = Brick(position_x+x_brick*(space_x_direction/(amount_per_row)), position_y+y_brick*(space_y_direction/(amount_per_column)), (space_x_direction-((amount_per_row-1)*distance))/(amount_per_row), (space_y_direction-(amount_per_column-1)*distance)/amount_per_column)
                    list_of_bricks.append(NewBrick)
            return list_of_bricks        
        else:
            raise TypeError("The bricks don't fit on the display!")
    
    menu_running = True
    highscore_running = False
    game_running = False
    paddle.mleft = False
    paddle.mright = False

    
    # if any object is added to the scene it has to be added to this list
    objects = [paddle, ceiling, rightwall, leftwall, Brick1, ball2, ball]    # lists of objects, the ball can collide with 
    ball.setCollidables(mydeepcopy(objects))
    ball2.setCollidables(mydeepcopy(objects))
    running = True
    while running:
        while menu_running:

            #always draw a black screen. then add objects as needed.
            screen.fill((0,0,0)) #0,0,0 is RGB color code for black

            #create Headline
            title_text = HEADLINE_FONT.render("Mainmenu", True, "red")
            screen.blit(title_text, (DISPLAY_WIDTH // 2 - title_text.get_width() // 2, 60))

            #create play button
            start_button = Button(text = "PLAY", color_text = "black", color_button = "red", x = 2, y = 2.5, x_button = 2, y_button = 2, font = HEADLINE_FONT, screen = screen, display_width = DISPLAY_WIDTH, display_height = DISPLAY_HEIGHT)
            start_button.draw()

            #create highscore button
            highscore_button = Button(text = "HIGHSCORE", color_text = "black", color_button = "red", x = 2, y = 1.4, x_button = 2, y_button = 2, font = HEADLINE_FONT, screen = screen, display_width = DISPLAY_WIDTH, display_height = DISPLAY_HEIGHT)
            highscore_button.draw()

            #update
            pygame.display.flip()

            #looking for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(event.pos): #when button is clicked, menu is getting closed and the game opens
                        menu_running = False
                        game_running = True
                        print("The menu was closed and the game was opened")
                        brick_grid = create_bricks(10, DISPLAY_HEIGHT/7, 10, 5, 0.2, 5, DISPLAY_WIDTH, DISPLAY_HEIGHT) #generates list which represents brick grid
                        print(brick_grid)
                    if highscore_button.is_clicked(event.pos): #when button is clicked, menu is getting closed and the highscore opens
                        menu_running = False
                        highscore_running = True
                        print("The menu was closed and the highscore was opened")


        while highscore_running:

            #always draw a black screen. then add objects as needed.
            screen.fill((0,0,0)) #0,0,0 is RGB color code for black

            #create return to menu button
            return_to_menu_button = Button(text = "RETURN TO MENU", color_text = "black", color_button = "red", x = 1, y = 1, x_button = 1, y_button = 1, font = NORMAL_FONT, screen = screen, display_width = DISPLAY_WIDTH, display_height = DISPLAY_HEIGHT)
            return_to_menu_button.draw()

            #update
            pygame.display.flip()

            #looking for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if return_to_menu_button.is_clicked(event.pos): #when button is clicked, highscore is getting closed and the menu opens
                        highscore_running = False
                        menu_running = True
                        print("The highscore was closed and the menu was opened")

                        
        
        
        while game_running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        paddle.mleft = True
                    if event.key == pygame.K_RIGHT  or event.key == pygame.K_d:
                        paddle.mright = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        paddle.mleft = False
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        paddle.mright = False

            # always draw a black screen. then add objects as needed.
            screen.fill((0,0,0)) #0,0,0 is RGB color code for black

            # Draw the grid of bricks
            for brick in range(0, len(brick_grid), 1):
                brick_grid[brick].draw(screen)

            # draw the ball
            ball.draw(screen)
            ball2.draw(screen)
            # move the ball one step
            ball.move()

            ball2.move()

            #draw the paddle
            paddle.draw(screen)

            #draw the test Brick
            Brick1.draw(screen)

            # Collide the Ball with the given list of objects
            ball.collide(paddle, screen, debugging=True)  
            ball2.collide(paddle, screen, debugging=True)       

            # move the paddle
            if paddle.mleft:
                paddle.move_left()
            elif paddle.mright:
                paddle.move_right(screen)

            # check if the ball has left the screen at the bottom, if yes, create a new one
            if ball.y > screen.get_height(): #note the top-left defined coordinate system :)
                print("The ball has left the screen")
                
                #create a new ball at the top
                objects.remove(ball)
                del ball
                ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red', collidables_list=mydeepcopy(objects))
                objects.append(ball)
                ball2.setCollidables(mydeepcopy(objects))

            #update
            pygame.time.wait(1) #slow things down by waiting 1 millisecond
            pygame.display.update()
            clock.tick(FPS)

    pygame.quit() # Call the quit() method outside the while loop to end the application.
