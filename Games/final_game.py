import math
import random
import bisect
from os import listdir
import pygame
from pygame.locals import *
import time
import sys
sys.path.insert(0, './BirdieBash')
sys.path.insert(0, './Football')
sys.path.insert(0, './Archery')

import birdie
import foot
import arc

common_path = "./BirdieBash/resources/images/"

background = pygame.image.load("main.jpg")
#menu = pygame.image.load("Menu.png")
start_screen = pygame.image.load(common_path + "start_game.png")

pygame.init()
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))

while 1:
    screen.blit(background, (0, 0))
    #screen.blit(menu, (400, 10))
    # screen.blit(start_screen, (205, 50))
    pygame.display.flip()

    rect1 = pygame.Rect((50, 50), (500, 500))
    rect1.top = 500
    rect1.left = 20

    rect2 = pygame.Rect((50, 50), (300, 300))
    rect2.top = 200
    rect2.left = 500

    rect3 = pygame.Rect((50, 50), (300, 300))
    rect3.top = 500
    rect3.left = 900


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
            if event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if rect1.collidepoint(position):
                    foot.play()
                elif rect2.collidepoint(position):
                    birdie.play(pygame.time.get_ticks())
                elif rect3.collidepoint(position):
                    arc.play()

    pygame.display.flip()

# birdie.play()
