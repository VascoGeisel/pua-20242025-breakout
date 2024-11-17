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

# example imports from custom classes
from objects.ball import Ball
from objects.paddle import Paddle

if __name__ == '__main__':
    pygame.init()

    # pygame setting variables
    FPS = 50

    # create a game screen
    DISPLAY_WIDTH = 600
    DISPLAY_HEIGHT = 800
    screen = pygame.display.set_mode(size=(DISPLAY_WIDTH, DISPLAY_HEIGHT))

    # initialize the clock for FPS calculation
    clock = pygame.time.Clock()

    # initialize a ball
    ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red')

    # initialize a paddle
    paddle_height = 10
    paddle_width = 50
    paddle = Paddle(DISPLAY_WIDTH//2, DISPLAY_HEIGHT-paddle_height, paddle_width, paddle_height)

    running = True
    left = False
    right = False

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left = False
            if event.key == pygame.K_RIGHT:
                right = False

        # always draw a black screen. then add objects as needed.
        screen.fill((0,0,0)) #0,0,0 is RGB color code for black

        # draw the ball
        ball.draw(screen)

        # move the ball one step
        ball.move()

        #draw the paddle
        paddle.draw(screen)

        # move the paddle
        if left:
            paddle.move_left()
        elif right:
            paddle.move_right(screen)

        # check if the ball has left the screen at the bottom, if yes, create a new one
        if ball.y > screen.get_height(): #note the top-left defined coordinate system :)
            print("The ball has left the screen")

            #create a new ball at the top
            ball = Ball(x = DISPLAY_WIDTH//2, y = 30, dx = 0, dy = 1, radius = 10, speed = 5, color='red')

        #update
        pygame.time.wait(1) #slow things down by waiting 1 millisecond
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit() # Call the quit() method outside the while loop to end the application.

