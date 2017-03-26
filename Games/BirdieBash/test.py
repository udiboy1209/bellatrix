import math
import random

import pygame
from pygame.locals import *

pygame.init()
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
BLUE  = (  255,   0, 0)
BLACK = (  0,   0,   0)
x = 50
y = 500
direction = 0

while 1:
    screen.fill(BLACK)
    if (x + 50) <=  1280 and direction == 0:
        x += 5
        pygame.draw.circle(screen, BLUE, (x, y), 35, 0)
    elif (x - 50) >=  0 and direction == 1:
        x -= 5
        pygame.draw.circle(screen, BLUE, (x, y), 35, 0)
    elif (x + 50) >=  1280 and direction == 0:
        direction = 1
    elif (x - 50) <=  0 and direction == 1:
        direction = 0

    pygame.display.flip()
