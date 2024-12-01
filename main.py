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

    #Text creation
    Score = SCORE_FONT.render("Hello KITty", True, "green")

    # initialize the clock for FPS calculation
    clock = pygame.time.Clock()

    # initialize a ball
    ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red')

    # initialize a paddle
    paddle_height = 10
    paddle_width = 50
    paddle = Paddle(DISPLAY_WIDTH//2, DISPLAY_HEIGHT-paddle_height-20, paddle_width, paddle_height)

    # Create the Perimiter of the Window
    ceiling = Wall(0, 0, DISPLAY_WIDTH, -20)
    rightwall = Wall(DISPLAY_WIDTH, 0, 20, DISPLAY_HEIGHT)
    leftwall = Wall(0, 0, -20, DISPLAY_HEIGHT)
    

    running = True
    paddle.mleft = False
    paddle.mright = False

    objects = [paddle, ceiling, rightwall, leftwall]    # lists of objects, the ball can collide with 
    ball.setCollidables(objects)
    
    while running:

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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

        # move the ball one step
        ball.move()

        #draw the paddle
        paddle.draw(screen)

        # Collide the Ball with the given list of objects
        ball.collide(paddle)         

        # move the paddle
        if paddle.mleft:
            paddle.move_left()
        elif paddle.mright:
            paddle.move_right(screen)

        # check if the ball has left the screen at the bottom, if yes, create a new one
        if ball.y > screen.get_height(): #note the top-left defined coordinate system :)
            print("The ball has left the screen")

            #create a new ball at the top
            ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red', collidables_list=objects)
            ball.setCollidables(objects)

        #update
        pygame.time.wait(1) #slow things down by waiting 1 millisecond
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit() # Call the quit() method outside the while loop to end the application.

