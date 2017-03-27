import math
import random
import bisect
from os import listdir
import pygame
from pygame.locals import *
import time


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

def play(time_started):
    

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
    game_start = False
    badguystart = [610, 450, 0, False, 0]
    gif_times = [0.1,0.1,0.1,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.2,0.2,0.2,0.2]
    speed = [2, 3, 4, 2, 3, 4]
    score_points = [10, 20, 30, 10, 20, 30]
    common_path = "./BirdieBash/resources/images/"
    font = pygame.font.Font("./BirdieBash/resources/fonts/csb.ttf", 27)
    pygame.font.init()

    background = pygame.image.load(common_path + "background.png")
    game_over = pygame.image.load(common_path + "game_over.png")
    card = pygame.image.load(common_path + "card.png")
    start_screen = pygame.image.load(common_path + "start_game.png")
    menu = pygame.image.load("Menu.png")
    menu_rect = pygame.Rect(menu.get_rect())
    menu_rect.top = 30
    menu_rect.left = 610
    birds = []
    for bird_type_number in range(1,4):
        birds.append(pygame.image.load(common_path + "bird" + str(bird_type_number) + ".png"))
    i = 0
    for bird_type_number in range(0,3):
        birds.append(pygame.transform.flip(birds[i], True, False))
        i += 1
    temp = birds

    running = 1
    exitcode = 0
    score = 0
    time_spent = 0
    time_changed = 0.0

    text_color = (195, 0, 1)
    count = 1
    time_spent = 0
    while running:
        screen.fill(0)
        screen.blit(background, (0, 0))
        if game_start:
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
            screen.blit(menu, (610, 30))
            game_duration = game_time + time_started - pygame.time.get_ticks()
            user_score = 10;
            update_time = 0.005*((game_time - game_duration) / 1000 % 60) + 0.35
            pygame.draw.rect(screen, text_color, (width - ((255.0/game_time)*game_duration + 30), 78, (252.0/game_time)*game_duration, 20))
            badtimer -= update_time
            position = pygame.mouse.get_pos()
            if badtimer <= 0:
                temp = y_coordinate
                y_coordinate = random.randint(200, height - 200)
                if y_coordinate <= temp + 200 or y_coordinate >= temp - 200:
                    if y_coordinate <= temp + 200:
                        if y_coordinate - 200 < 200:
                            y_coordinate = 200
                    else:
                        if y_coordinate + 200 > height - 200:
                            y_coordinate = height - 200
                choice = random.choice(
                    [[width + 30, y_coordinate, 0, False, 0, 1], [-20, y_coordinate, 2, False, 0, 1]])

                if choice[2] == 0:
                    choice[5] = weighted_choice([(4,50), (5,30), (6,20)])
                if choice[2] == 1:
                    choice[5] = weighted_choice([(1,50), (2,30), (3,20)])

                badguys.append(choice)
                badtimer = 125 - (badtimer1 * 2)
                if badtimer1 >= 35:
                    badtimer1 = 35
                else:
                    badtimer1 += 5
            index = 0
            for badguy in badguys:
                if badguy[0] < -60:
                    badguys.pop(index)
                elif badguy[0] > width + 60:
                    badguys.pop(index)
                elif badguy[1] < -60:
                    badguys.pop(index)
                elif badguy[1] > height + 60:
                    badguys.pop(index)
                elif badguy[2] == 0:
                    if badguy[3]:
                        time_elapsed = (pygame.time.get_ticks() - badguy[4]) / 1000.00
                        badguy[1] += 40*time_elapsed + 0.5*9.8*time_elapsed*time_elapsed
                        badguy[0] -= 3
                    else:
                        badguy[0] -= speed[badguy[5]-1]

                    screen.blit(birds[badguy[5] - 1], (badguy[0], badguy[1]))
                elif badguy[2] == 2:
                    if badguy[3]:
                        time_elapsed = (pygame.time.get_ticks() - badguy[4]) / 1000.00
                        badguy[1] += 40*time_elapsed + 0.5*9.8*time_elapsed*time_elapsed
                        badguy[0] += 3
                    else:
                        badguy[0] += speed[badguy[5] - 1]

                    screen.blit(birds[badguy[5] - 1], (badguy[0], badguy[1]))
                index += 1
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    if event.type == MOUSEBUTTONDOWN:
                        position = pygame.mouse.get_pos()
                        index = 0
                        for badguy in badguys:
                            badrect = pygame.Rect(birds[badguy[5] - 1].get_rect())
                            badrect.top = badguy[1]
                            badrect.left = badguy[0]
                            if badrect.collidepoint(position):
                                score += score_points[badguy[5] - 1]
                                badguy[3] = True
                                badguy[4] = pygame.time.get_ticks()
                            index += 1
                        if menu_rect.collidepoint(position):
                            return

            if pygame.time.get_ticks() >= game_time:
                running = 0
                exitcode = 0
        else:
            screen.blit(start_screen, (205, 50))
            if badguystart[1] > height + 60:
                    game_time = game_time + pygame.time.get_ticks()
                    game_start = True

            # screen.blit(gbird_images_list[gbird_image_index], (badguystart[0], badguystart[1]))
            # screen.display.flip()

            if badguystart[3]:
                time_elapsed = (pygame.time.get_ticks() - badguystart[4]) / 1000.00
                badguystart[1] += 40*time_elapsed + 0.5*9.8*time_elapsed*time_elapsed
            screen.blit(birds[0], (badguystart[0], badguystart[1]))
            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                    if event.type == MOUSEBUTTONDOWN:
                        position = pygame.mouse.get_pos()
                        badrect = pygame.Rect(birds[0].get_rect())
                        badrect.top = badguystart[1]
                        badrect.left = badguystart[0]
                        if badrect.collidepoint(position):
                            badguystart[3] = True
                            badguystart[4] = pygame.time.get_ticks()

            if (time_spent == gif_times[count]):
                time_changed = round(pygame.time.get_ticks()/1000.0,1)
                gbird_image_index = (gbird_image_index + 1) % 14
                count += 1

            time_spent = round(pygame.time.get_ticks()/1000.0 - time_changed,1)


    if exitcode == 0:
        screen.blit(background, (0, 0))
        screen.blit(game_over, (250, 150))
        screen.blit(menu, (610, 30))
        menu_rect = pygame.Rect(menu.get_rect())
        menu_rect.top = 30
        menu_rect.left = 610
        font = pygame.font.Font("./BirdieBash/resources/fonts/csb.ttf", 45)
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
        # while 1:
        #     for event in pygame.event.get():
        #         if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
        #             position = pygame.mouse.get_pos()
        #             if menu_rect.collidepoint(position):
        #                 return

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
