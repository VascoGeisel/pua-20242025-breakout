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
    SCORE_FONT = pygame.font.Font(None, 30)
    HEADLINE_FONT = pygame.font.Font(None, 64)
    
    #Text creation
    Score = SCORE_FONT.render("Hello KITty", True, "green")

    # initialize the clock for FPS calculation
    clock = pygame.time.Clock()

    # initialize a ball
    ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red')

    # initialize a second ball
    ball2 = Ball(x = DISPLAY_WIDTH//2+50, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red')

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
    
    menu_running = True
    game_running = False
    paddle.mleft = False
    paddle.mright = False

    # if any object is added to the scene it has to be added to this list
    objects = [paddle, ceiling, rightwall, leftwall, Brick1, ball2, ball]    # lists of objects, the ball can collide with 
    ball.setCollidables(mydeepcopy(objects))
    ball2.setCollidables(mydeepcopy(objects))
    
    while menu_running:

        # always draw a black screen. then add objects as needed.
        screen.fill((0,0,0)) #0,0,0 is RGB color code for black

        #create Headline
        title_text = HEADLINE_FONT.render("Mainmenu", True, "red")
        screen.blit(title_text, (DISPLAY_WIDTH // 2 - title_text.get_width() // 2, 100))

        #create start button with text
        start_button_position = pygame.Rect(DISPLAY_WIDTH // 2 - 75, DISPLAY_HEIGHT // 2 - 25, 150, 50)
        pygame.draw.rect(screen, "red", start_button_position)
        start_button_text = HEADLINE_FONT.render("PLAY", True, "black")
        screen.blit(start_button_text, (DISPLAY_WIDTH // 2 - start_button_text.get_width() // 2, DISPLAY_HEIGHT // 2 - start_button_text.get_height() // 2))

        #update
        pygame.display.flip()

        #when button is clicked, menu is getting closed and the game opens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_position.collidepoint(event.pos):
                    menu_running = False
                    game_running = True
                    print("The menu was closed and the game was opened")
              
    
    while game_running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle.mleft = True
            if event.key == pygame.K_RIGHT:
                paddle.mright = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                paddle.mleft = False
            if event.key == pygame.K_RIGHT:
                paddle.mright = False

        # always draw a black screen. then add objects as needed.
        screen.fill((0,0,0)) #0,0,0 is RGB color code for black

        #show score
        Score_position = Score.get_rect(center=(100,200))
        screen.blit(Score, Score_position)
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
            ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red', collidables_list=mydeepcopy(objects))


        #update
        pygame.time.wait(1) #slow things down by waiting 1 millisecond
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit() # Call the quit() method outside the while loop to end the application.

