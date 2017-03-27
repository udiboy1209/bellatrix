import math
import random
import bisect
from os import listdir
import pygame
from pygame.locals import *
import time

common_path = "./Archery/resources/images/"

def get_sector(x,y):
    center_x = 635.0
    center_y = 555.0
    slope = 90
    distance = ((y-center_y)**2+(x-center_x)**2)**0.5
    if (center_x-x != 0): slope = math.degrees(math.atan2((y-center_y),(x-center_x)))
    if(distance<=133): return 7
    if(distance<=297):
        if(slope>=30 and slope<=90):return 3
        if(slope>=90 and slope<=150):return 4
        if(slope>=-30 and slope<=30):return 2
        if(slope>=-90 and slope<=-30):return 1
        if(slope>=-150 and slope<=-90):return 6
        if((slope>=150 and slope<=180) or (slope>=-180 and slope<=-150)):return 5
    else: return 0

def get_score(sector):
    if(sector==1): return 20
    if(sector==2): return 60
    if(sector==3): return 40
    if(sector==4): return 80
    if(sector==5): return 10
    if(sector==6): return 90
    if(sector==7): return 100
    else: return 0

def weighted_choice(choices):
    values, weights = zip(*choices)
    total = 0
    cum_weights = []
    for w in weights:
        total += w
        cum_weights.append(total)
    x = random.random() * total
    i = bisect.bisect(cum_weights, x)
    return values[i]

def play():

    scores_file = open('scores.txt', 'ab')

    pygame.init()
    width, height = 1280, 960
    screen = pygame.display.set_mode((width, height))
    # x, y, direction, hit or not, hit time, bird type
    badguys = [[-50, 450, 2, False, 0, 1]]
    badtimer = 125
    badtimer1 = 0

    y_coordinate = 40
    game_time = 60000
    badguystart = [610, 450, 0, False, 0]
    speed = [2, 3, 4, 2, 3, 4]
    score_points = [10, 20, 30, 10, 20, 30]
    font = pygame.font.Font("./Archery/resources/fonts/csb.ttf", 27)
    pygame.font.init()

    background = pygame.image.load(common_path + "Archery-Bg.jpg")
    game_over = pygame.image.load(common_path + "game_over.png")
    card = pygame.image.load(common_path + "card.png")
    board = pygame.image.load(common_path + "archery_board.png")
    menu = pygame.image.load("Menu.png")

    running = 1
    exitcode = 1
    score = 0
    shots = 5
    text_color = (195, 0, 1)

    gbird_images_list = []
    rev_count = False

    while running:
        screen.fill(0)
        screen.blit(background, (0, 0))
        screen.blit(card, (20, 20))
        screen.blit(board, (100, 100))
        screen.blit(card, (width - 300, 20))
        screen.blit(menu, (610, 30))
        menu_rect = pygame.Rect(menu.get_rect())
        menu_rect.top = 30
        menu_rect.left = 610
        score_text = font.render("GAME SCORE", True, text_color)
        score_text_rect = score_text.get_rect()
        score_text_rect.left = 67
        score_text_rect.top = 30
        screen.blit(score_text, score_text_rect)
        time_text = font.render("SHOTS LEFT", True, text_color)
        time_text_rect = time_text.get_rect()
        time_text_rect.top = 30
        time_text_rect.left = width - 245
        screen.blit(time_text, time_text_rect)
        user_score = font.render(str(score), True, text_color)
        user_score_rect = score_text.get_rect()
        user_score_rect.top = 60
        user_score_rect.left = 145
        screen.blit(user_score, user_score_rect)
        shots_left = font.render(str(shots), True, text_color)
        shots_left_rect = score_text.get_rect()
        shots_left_rect.top = 60
        shots_left_rect.left = width - 175
        screen.blit(shots_left, shots_left_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                shots -= 1
                if event.type == MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    score += get_score(get_sector(position[0],position[1]))
                    if menu_rect.collidepoint(position):
                        return

        if shots == 0:
            running = 0
            exitcode = 0


    if exitcode == 0:
        screen.blit(background, (0, 0))
        screen.blit(game_over, (250, 150))
        font = pygame.font.Font("./Archery/resources/fonts/csb.ttf", 45)
        scores_file.write(str(score) + "\n")
        screen.blit(menu, (610, 30))
        score_text = font.render("SCORE : " + str(score), True, text_color)
        scores_file.close()
        scores_file = open('scores.txt', 'r')
        scores = scores_file.readlines()
        scores_file.close()
        scores = [score_line.strip() for score_line in scores]
        scores.sort(key=float, reverse = True)
        best_score_text = font.render("BEST SCORE : " + scores[0], True, text_color)
        best_score_rect = best_score_text.get_rect()
        best_score_rect.left = 440
        best_score_rect.top = 440
        score_text_rect = score_text.get_rect()
        score_text_rect.left = 520
        score_text_rect.top = 350
        screen.blit(score_text, score_text_rect)
        screen.blit(best_score_text, best_score_rect)

    while 1:
        menu_rect = pygame.Rect(menu.get_rect())
        menu_rect.top = 30
        menu_rect.left = 610
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if event.type == MOUSEBUTTONDOWN:
                    if menu_rect.collidepoint(position):
                        return
        pygame.display.flip()
