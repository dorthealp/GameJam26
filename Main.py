import pygame
from sys import exit

pygame.init()   # initalizes
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("TEST")  # set name of the window
clock = pygame.time.Clock() # controlls the framerate

while True:
    for event in pygame.event.get(): # get all the events
        if event.type == pygame.QUIT:
            pygame.quit()   # unitializes
            exit()  # safely exit
    
    pygame.display.update() # draw all our elements and update everything
    clock.tick(60)  # do not run faster than 60 fps
    