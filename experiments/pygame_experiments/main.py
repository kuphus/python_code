import pygame, sys
from settings import *
from level import Level


#setting up the game
pygame.init()

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill('blue')
    level.draw()

    pygame.display.update()
    clock.tick(60)