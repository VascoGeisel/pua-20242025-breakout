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
    left = False
    right = False

    # create a counter for the collision detection System (may remove in future)
    frames_since_collision = 0

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

        #show score
        Score_position = Score.get_rect(center=(100,200))
        screen.blit(Score, Score_position)
        # draw the ball
        ball.draw(screen)

        # move the ball one step
        ball.move()

        #draw the paddle
        paddle.draw(screen)

        ## Collision Detection / Reflection
        # TODO: Move into another class or at least funciton
        # TODO: normalize the ball movement Vector, so its not becomming infinitly fast
        # TODO: Make the Reflection not independent of the Speed of the Paddle
        # TODO: IMPORTANT! If ball collides in corner and should collide with both wall and ceiling, 15 frames of immunity are to large
        # This code will be moved to another potion in the future but for now it will remain here for ease of development
        
        frames_since_collision += 1                                     # increment the collision counter, so there wont be any colisions right after each other

        if frames_since_collision >= 15:                                # check for recent collision (15 is completly arbitrary, may change in the future)
            
            objects = [paddle, ceiling, rightwall, leftwall]            # lists of objects, the ball can collide with (TODO: move to top)
            collision_index = ball.collidelist(objects) 
            if collision_index >= 0:                                    # chechs if Ball collides with any collidable objects
                print(f"A collision was detected, the last colision was {frames_since_collision} ago") 
                frames_since_collision = 0                              # reset counter
                for i in range(len(objects)):                           # iterate over all the collidable objects
                    pygame.draw.line(screen, (255, 0, 255), objects[collision_index].get_edges()[i][0], objects[collision_index].get_edges()[i][1], 1) # only for debugging, draws outlines ob colided objects
                    if ball.clipline(objects[collision_index].get_edges()[i]):  # checks wich edge of collidable object ball collides with
                        if i == 0 or i == 4:                            # horizontal surfaces
                            # print(f"A Horziontal Surface was hit")
                            ball.dx = ball.dx
                            ball.dy = -ball.dy                  

                        elif i == 1 or i == 2:                          # vertical surfaces
                            # print(f"A vertical Surface was hit")      
                            ball.dx = -ball.dx
                            ball.dy = ball.dy
                        
                        if objects[collision_index] == paddle:          # checks if paddle was hit
                            randomnumber = (random.randrange(-5000, +5000)+ random.randrange(-5000, +5000)) * 0.0001    # create displacement according to gaussian distribution around 0, so its clean
                            ball.dx += randomnumber                     # changes dx of ball by random number 
                            print(f"The Paddle was hit, dx has been changed by {randomnumber}")

                        break                                           # DO NOT REMOVE Limits collisions per frame per ball by 1 
            
        

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

