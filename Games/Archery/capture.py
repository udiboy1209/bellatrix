#!/usr/bin/env python

import cv2
import numpy as np
import pygame
from pygame import surfarray
import time
import math
import random
import bisect
from os import listdir
# from pygame.locals import *

def get_sector(x,y):
    center_x = 395.0
    center_y = 350.0
    slope = 90
    distance = ((y-center_y)**2+(x-center_x)**2)**0.5
    if (center_x-x != 0): slope = math.degrees(math.atan2((y-center_y),(x-center_x)))
    print(distance,slope)
    if(distance<=71): return 7
    if(distance<=165):
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

scores_file = open('scores.txt', 'ab')

pygame.init()
# width, height = 1280, 960
width, height = 800, 600
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
font = pygame.font.Font("resources/fonts/csb.ttf", 27)
pygame.font.init()

background = pygame.image.load("resources/images/Archery-Bg.jpg")
game_over = pygame.image.load("resources/images/game_over.png")
card = pygame.image.load("resources/images/card.png")
board = pygame.image.load("resources/images/archery_board.png")

running = 1
exitcode = 0
score = 0
shots = 100
text_color = (195, 0, 1)

gbird_images_list = []
rev_count = False

gbird_images = [f for f in listdir("resources/images/gbird")]
index = 0
for img in gbird_images:
    gbird_images_list.append(pygame.image.load("resources/images/gbird/" + img))
    index += 1

cap = cv2.VideoCapture(0)

FINAL_MIN = np.array([0, 210, 0])
FINAL_MAX = np.array([255, 255, 255])

screen = pygame.display.set_mode((width, height))
screen.fill((0,255,0))
# pygame.draw.rect(screen,(0,255,0),pygame.Rect(200,50,800,600))
pygame.display.set_caption('HackU game')

pygame.display.flip()

MEAN_BOUNDARY_SIZE = 100.0
sum_boundary = []
sum_quad = None
mean_quad = None
mean_boundary = None
sum_boundary_count = 0
nfcount = 0
max_hit = None

def calibrate_screen(frame):

    global mean_boundary,MEAN_BOUNDARY_SIZE,sum_boundary,sum_boundary_count
    global mean_quad,sum_quad

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Threshold according to values
    frame_threshold = cv2.inRange(rgb_frame, FINAL_MIN, FINAL_MAX)
    if int(cv2.__version__.split('.')[0])<3:
        contours, hierarchy = cv2.findContours(frame_threshold,
                                    cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    else:
        im2, contours, hierarchy = cv2.findContours(frame_threshold,
                                    cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    screenRect = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
                screenRect = approx
                break


    if screenRect is not None:
        cv2.drawContours(frame, [screenRect], -1, (0,0,255), 3)
        minX = min(screenRect[1][0][0],screenRect[2][0][0])
        maxX = min(screenRect[0][0][0],screenRect[3][0][0])
        minY = max(screenRect[0][0][1],screenRect[1][0][1])
        maxY = max(screenRect[2][0][1],screenRect[3][0][1])

        if maxX-minX>0 and maxY-minY>0 and sum_boundary_count<MEAN_BOUNDARY_SIZE:
            if sum_boundary_count==0:
                sum_boundary.append([minX,maxX,minY,maxY])
                sum_quad = screenRect
            else:
                sum_boundary = np.insert(sum_boundary,0,[minX,maxX,minY,maxY],axis=0)
                sum_quad = sum_quad+screenRect
            sum_boundary_count = sum_boundary_count + 1
            print (sum_boundary_count/MEAN_BOUNDARY_SIZE)*100," % complete..."

    if sum_boundary_count>=MEAN_BOUNDARY_SIZE and mean_boundary is None:
        mean_boundary = np.sum(sum_boundary,axis=0)/sum_boundary_count
        mean_quad = sum_quad/sum_boundary_count


raw_input("Press any key to continue to calibration...")
print "Calibration begins..."

#########################
## Calibration Routine ##
#########################

while True:
    ret, frame = cap.read()

    if mean_boundary is None:
        calibrate_screen(frame)
    if mean_boundary is not None:
        break
    cv2.imshow('contour', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print "Calibration complete..."

fps = 30
t_frame = 1./fps
curr_frame_delay = 0
curr_frame_start = 0
skip_render = False
execute = True
fn = 0
dilate_kernel = np.ones((7,7), np.uint8)

kptrace = []

gbird_image_index = 0
while running:
    ret, frame = cap.read()

    if execute:
        curr_frame_start = time.time()

        screen.fill(0)
        screen.blit(background, (0, 0))
        screen.blit(card, (20, 20))
        screen.blit(board, (20, 20))
        screen.blit(card, (width - 300, 20))
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
        if max_hit:
            pygame.draw.circle(screen, (0, 0, 255),
                               (int(max_hit.pt[0]),int(max_hit.pt[1])),
                               5)

        pygame.display.flip()

        #quad
        src_points = np.float32([mean_quad[0][0],mean_quad[1][0],
                                 mean_quad[2][0],mean_quad[3][0]])

        #800x600 things
        dst_points = np.float32([[width,0],[0,0],[0,height],[width,height]])
        perspectiveT = cv2.getPerspectiveTransform(src_points, dst_points)

        cropped_frame = cv2.warpPerspective(frame, perspectiveT, (width,height))

        # render

        pygame_frame = surfarray.array3d(screen)
        pygame_frame = np.swapaxes(pygame_frame, 0, 1)
        pygame_frame = cv2.cvtColor(pygame_frame, cv2.COLOR_BGR2RGB)

        last_pygame_frame = pygame_frame


       # cimg = cv2.cvtColor(cropped_frame,cv2.COLOR_BGR2GRAY)
       # circles = cv2.HoughCircles(cimg,cv2.HOUGH_GRADIENT,1,1.20, param1=50, param2=30,minRadius=0,maxRadius=0)

       # print circles
       # if circles is not None:
       #     circles = np.uint16(np.around(circles))
       #     for i in circles[0,:]:
# draw #the outer circle
       #         cv2.circle(cropped_frame,(i[0],i[1]),i[2],(0,255,0),2)
# draw #the center of the circle
       #         cv2.circle(cropped_frame,(i[0],i[1]),2,(0,0,255),3)


        hsv_crop = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)
        hsv_pgam = cv2.cvtColor(pygame_frame, cv2.COLOR_BGR2RGB)
        diff_frame = np.abs(hsv_crop-hsv_pgam)
        thresh1 = cv2.inRange(diff_frame, np.array([100,100,0],np.uint8),
                    np.array([255,255,255],np.uint8))
        thresh2 = cv2.inRange(diff_frame, np.array([100,100,0],np.uint8),
                    np.array([255,255,255],np.uint8))
        thresh3 = cv2.inRange(diff_frame, np.array([0,50,0],np.uint8),
                    np.array([255,255,255],np.uint8))
        thresh = thresh1
        thresh = 255-thresh
        thresh = cv2.dilate(thresh, dilate_kernel)

        blob_params = cv2.SimpleBlobDetector_Params()

        blob_params.filterByCircularity = True
        blob_params.filterByConvexity = True
        blob_params.filterByInertia = True
        blob_params.filterByArea = True
        blob_params.minArea = 500
        blob_params.maxArea = 1000
        blob_params.minInertiaRatio = 0.2
        blob_params.maxInertiaRatio = 0.8
        blob_params.minCircularity = 0.2
        blob_params.minConvexity = 0.2

        detector = cv2.SimpleBlobDetector_create(blob_params)
        keypoints = detector.detect(thresh)

        max_hit = None


        if len(kptrace)>20:
            kptrace = []

        if len(keypoints) > 0:
            kptrace.extend(keypoints)
            nfcount = 0
            print("Keypoints detected")
        else:
            nfcount = nfcount + 1
            if nfcount>5:
                nfcount = 0
                if len(kptrace) > 0:
                    max_hit = max(kptrace, key=lambda x:x.size)
                    kptrace = []
                    print("%s - %d" % (max_hit.pt, max_hit.size))


        im_with_keypoints = cv2.drawKeypoints(cropped_frame, kptrace,
                    np.array([]), (0,0,255),
                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imshow('pygame', pygame_frame)
        cv2.imshow('diff', diff_frame)
        cv2.imshow('thresh', thresh)
        cv2.imshow('cropped', im_with_keypoints)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    if max_hit:
        shots -= 1
        position = max_hit.pt
        score += get_score(get_sector(position[0],position[1]))

    if shots == 0:
        running = 0
        exitcode = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        running = 0
        exitcode = 0

    curr_frame_delay = time.time() - curr_frame_start
    if t_frame > curr_frame_delay:
        execute = False
        # time.sleep(t_frame - curr_frame_delay)
    else:
        print(curr_frame_delay - t_frame)
        execute = True
        # print("Update too slow\nOvershoot: %f" % (curr_frame_delay - t_frame))


if exitcode == 0:
    screen.blit(background, (0, 0))
    screen.blit(game_over, (170, 110))
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
    best_score_rect.left = 195
    best_score_rect.top = 300
    score_text_rect = score_text.get_rect()
    score_text_rect.left = 275
    score_text_rect.top = 210
    screen.blit(score_text, score_text_rect)
    screen.blit(best_score_text, best_score_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
