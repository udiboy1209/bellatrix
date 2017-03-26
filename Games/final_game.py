import math
import random
import bisect
from os import listdir
import pygame
from pygame.locals import *
import time
import sys
sys.path.insert(0, '/home/darknight/Desktop/Pygames/Yahoo/Games/BirdieBash')
sys.path.insert(0, '/home/darknight/Desktop/Pygames/Yahoo/Games/Football')

import birdie
import foot

common_path = "/home/darknight/Desktop/Pygames/Yahoo/Games/BirdieBash/resources/images/"

background = pygame.image.load("main.jpg")
start_screen = pygame.image.load(common_path + "start_game.png")

pygame.init()
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))

while 1:
    screen.blit(background, (0, 0))
    # screen.blit(start_screen, (205, 50))
    pygame.display.flip()

    rect1 = pygame.Rect((50, 50), (500, 500))
    rect1.top = 500
    rect1.left = 20

    rect2 = pygame.Rect((50, 50), (300, 300))
    rect2.top = 200
    rect2.left = 500


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
            if event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if rect1.collidepoint(position):
                    foot.play()
                if rect2.collidepoint(position):
                    birdie.play()

# birdie.play()
