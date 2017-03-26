import math
import random
from os import listdir
import pygame
from pygame.locals import *
import time

scores_file = open('scores.txt', 'ab')

pygame.init()
width, height = 1280, 960
screen = pygame.display.set_mode((width, height))
# x, y, direction, hit or not, hit time
badguys = [[-50, 450, 2, False, 0]]
badtimer = 125
badtimer1 = 0

y_coordinate = 40
game_time = 60000
game_start = False
badguystart = [610, 450, 0, False, 0]
speed = 2
font = pygame.font.Font("resources/fonts/csb.ttf", 27)
pygame.font.init()

background = pygame.image.load("resources/images/background.png")
game_over = pygame.image.load("resources/images/game_over.png")
card = pygame.image.load("resources/images/card.png")
birdie1 = pygame.image.load("resources/images/bird1.png")
rev_birdie1 = pygame.transform.flip(birdie1, True, False)
birdie2 = pygame.image.load("resources/images/bird2.png")
rev_birdie2 = pygame.transform.flip(birdie1, True, False)
birdie3 = pygame.image.load("resources/images/bird3.png")
rev_birdie3 = pygame.transform.flip(birdie1, True, False)
running = 1
exitcode = 0
score = 0

text_color = (195, 0, 1)

gbird_images_list = []
rev_count = False

gbird_images = [f for f in listdir("resources/images/gbird")]
index = 0
for img in gbird_images:
    gbird_images_list.append(pygame.image.load("resources/images/gbird/" + img))
    index += 1

gbird_image_index = 0
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
        game_duration = game_time - pygame.time.get_ticks()
        user_score = 10;
        update_time = 0.01*((game_time - game_duration) / 1000 % 60) + 0.3
        pygame.draw.rect(screen, text_color, (width - ((255.0/game_time)*game_duration + 30), 78, (252.0/game_time)*game_duration, 20))
        badtimer -= update_time
        position = pygame.mouse.get_pos()
        if badtimer <= 0:
            temp = y_coordinate
            y_coordinate = random.randint(100, height - 100)
            if y_coordinate <= temp + 100 or y_coordinate >= temp - 100:
                if y_coordinate <= temp + 100:
                    if y_coordinate - 100 < 100:
                        y_coordinate = 100
                else:
                    if y_coordinate + 100 > height - 100:
                        y_coordinate = height - 100
            choice = random.choice(
                [[width + 30, y_coordinate, 0, False, 0], [-20, y_coordinate, 2, False, 0]])
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
                    badguy[0] -= speed

                screen.blit(rev_birdie1, (badguy[0], badguy[1]))
            elif badguy[2] == 2:
                if badguy[3]:
                    time_elapsed = (pygame.time.get_ticks() - badguy[4]) / 1000.00
                    badguy[1] += 40*time_elapsed + 0.5*9.8*time_elapsed*time_elapsed
                    badguy[0] += 3
                else:
                    badguy[0] += speed

                screen.blit(birdie1, (badguy[0], badguy[1]))
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
                        badrect = pygame.Rect(birdie1.get_rect())
                        badrect.top = badguy[1]
                        badrect.left = badguy[0]
                        if badrect.collidepoint(position):
                            score += 10
                            badguy[3] = True
                            badguy[4] = pygame.time.get_ticks()
                        index += 1

        if pygame.time.get_ticks() >= game_time:
            running = 0
            exitcode = 0
    else:
        text = font.render("Hit the bird to start the game!", True, (255, 255, 255))
        textRect = text.get_rect()
        # screen.blit(gbird_images_list[gbird_image_index], (50, 50))
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery - 100
        screen.blit(text, textRect)
        if badguystart[1] > height + 60:
                game_time = game_time + pygame.time.get_ticks()
                game_start = True

        if badguystart[3]:
            time_elapsed = (pygame.time.get_ticks() - badguystart[4]) / 1000.00
            badguystart[1] += 40*time_elapsed + 0.5*9.8*time_elapsed*time_elapsed
        screen.blit(birdie1, (badguystart[0], badguystart[1]))
        pygame.display.flip()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN or event.type == MOUSEBUTTONDOWN:
                if event.type == MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    badrect = pygame.Rect(birdie1.get_rect())
                    badrect.top = badguystart[1]
                    badrect.left = badguystart[0]
                    if badrect.collidepoint(position):
                        badguystart[3] = True
                        badguystart[4] = pygame.time.get_ticks()
        if rev_count:
            gbird_image_index -= 1
            if gbird_image_index == 0:
                rev_count = False
        else:
            gbird_image_index += 1
            if gbird_image_index == (len(gbird_images_list) - 1):
                rev_count = True


if exitcode == 0:
    screen.blit(background, (0, 0))
    screen.blit(game_over, (250, 150))
    font = pygame.font.Font("resources/fonts/csb.ttf", 45)
    scores_file.write(str(score) + "\n")
    score_text = font.render("SCORE : " + str(score), True, text_color)
    scores_file.close()
    scores_file = open('scores.txt', 'r')
    scores = scores_file.readlines()
    scores_file.close()
    scores = [score_line.strip() for score_line in scores]
    scores.sort(key=float, reverse = True)
    print scores
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
