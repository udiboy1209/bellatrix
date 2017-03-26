import pygame
import cv2

(width, height) = (800,600)

screen = pygame.display.set_mode((width, height))
screen.fill((0,255,0))
pygame.display.set_caption('HackU game')

pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
