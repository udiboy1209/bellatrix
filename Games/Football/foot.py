import math
import random
import time
from os import listdir
import pygame
from pygame.locals import *
import time

def play():
    scores_file = open('scores.txt', 'ab')

    pygame.init()
    width, height = 1280, 960
    screen = pygame.display.set_mode((width, height))
    screen.set_alpha(0)
    keys = [False, False, False, False]

    game_time = 10000000000
    game_start = True
    font = pygame.font.Font("./Football/resources/fonts/csb.ttf", 27)
    pygame.font.init()

    common_path = "./Football/resources/images/"

    background = pygame.image.load(common_path + "background.jpg")
    gk_ready = pygame.image.load(common_path + "ready.png")
    gk_rtdive = pygame.image.load(common_path + "thoda_dive.png")
    gk_rdive = pygame.image.load(common_path + "pura_dive.png")
    gk_ltdive = pygame.image.load(common_path + "left_thoda_dive.png")
    gk_ldive = pygame.image.load(common_path + "left_pura_dive.png")
    game_over = pygame.image.load(common_path + "game_over.png")
    card = pygame.image.load(common_path + "card.png")
    start_screen = pygame.image.load(common_path + "start_game.png")
    menu = pygame.image.load("Menu.png")
    menu_rect = pygame.Rect(menu.get_rect())
    menu_rect.top = 30
    menu_rect.left = 610

    delay = False
    full_dive = False

    running = 1
    exitcode = 0
    score = 0
    time_spent = 0
    time_changed = 0.0

    text_color = (195, 0, 1)

    gk_pos = [540, 380]

    gk_pic = gk_ready

    time_at_paused = 0

    time_paused = False

    dive = False



    while running:
        screen.fill(0)
        screen.set_alpha(0)
        screen.blit(background, (0, 0))
        screen.blit(menu, (610, 30))
        if game_start:
            if not time_paused:
                screen.blit(card, (20, 20))
                screen.blit(card, (width - 300, 20))
                score_text = font.render("GAME SCORE", True, text_color)
                score_text_rect = score_text.get_rect()
                score_text_rect.left = 67
                score_text_rect.top = 30
                screen.blit(score_text, score_text_rect)
                time_text = font.render("TIME LEFT", True, text_color)
                time_text_rect = time_text.get_rect()
                time_text_rect.top = 30
                time_text_rect.left = width - 235
                screen.blit(time_text, time_text_rect)
                user_score = font.render(str(score), True, text_color)
                user_score_rect = score_text.get_rect()
                user_score_rect.top = 60
                user_score_rect.left = 145
                screen.blit(user_score, user_score_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit(0)
                    if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                        if event.type == MOUSEBUTTONDOWN:
                            position = pygame.mouse.get_pos()
                            gk_rect = pygame.Rect((gk_pos[0], gk_pos[1], gk_pic.get_width(), gk_pic.get_height()))
                            if gk_pic == gk_ltdive:
                                gk_rect.top
                            gk_rect.top = gk_pos[1]
                            gk_rect.left = gk_pos[0]
                            if gk_rect.collidepoint(position):
                                score += 10
                            if menu_rect.collidepoint(position):
                                return

                    if event.type == pygame.KEYUP:
                        if event.key == K_LEFT:
                            keys[2] = False
                        if event.key == K_s:
                            keys[3] = False
                        if event.key == K_RIGHT:
                            keys[1] = False
                        if event.key == K_w:
                            keys[0] = False

                keyp = pygame.key.get_pressed()

                if keyp[K_w]:
                    keys[0] = True
                if keyp[K_RIGHT]:
                    keys[1] = True
                if keyp[K_LEFT]:
                    keys[2] = True
                if keyp[K_s]:
                    keys[3] = True


                if (keys[0] or keys[3]) and (keys[1] or keys[2]):
                    if keys[0] and keys[1]:
                        gk_pic = gk_rtdive

                    if keys[3] and keys[1]:
                        gk_pic = gk_rdive
                        gk_pos[1] += 180
                        full_dive = True

                    if keys[2] and keys[0]:
                        gk_pic = gk_ltdive

                    if keys[2] and keys[3]:
                        gk_pic = gk_ldive
                        gk_pos[1] += 180
                        full_dive = True

                    dive = True
                        

                    # for index in range(0,4):
                    #     keys[index] = False
                else:
                    if keys[1]:
                        if gk_pos[0] >= width - 400:
                            gk_pos[0] = gk_pos[0]
                        else:
                            gk_pos[0] += 5
                    if keys[2]:
                        if gk_pos[0] <= 200:
                            gk_pos[0] = gk_pos[0]
                        else:
                            gk_pos[0] -= 5

                screen.blit(gk_pic, (gk_pos[0], gk_pos[1]))
                pygame.display.flip()

                if dive:
                    # pygame.event.set_allowed(None)
                    # for index in range(0,4):
                    #     keys[index] = False
                    # time_at_paused = pygame.time.get_ticks()
                    # time_paused = True
                    # delay = False
                    gk_pic = gk_ready
                    if full_dive:
                        gk_pos[1] -= 180
                        full_dive = False
                    dive = False


                if pygame.time.get_ticks() >= game_time:
                    running = 0
                    exitcode = 0

            else:
                if pygame.time.get_ticks() - time_at_paused > 2000:
                    time_paused = False
                    pygame.event.set_blocked(None)
                    for index in range(0,4):
                        keys[index] = False
                    delay = False
                    full_dive = False


        else:
            screen.blit(start_screen, (205, 50))
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    if event.type == MOUSEBUTTONDOWN:
                        game_start = True

    if exitcode == 0:
        screen.blit(background, (0, 0))
        screen.blit(game_over, (250, 150))
        font = pygame.font.Font("./Football/resources/fonts/csb.ttf", 45)
        scores_file.write(str(score) + "\n")
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
