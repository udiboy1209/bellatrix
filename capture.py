#!/usr/bin/env python

import cv2
import numpy as np
import pygame
from pygame import surfarray
import time

cap = cv2.VideoCapture(0)

FINAL_MIN = np.array([0, 210, 0])
FINAL_MAX = np.array([255, 255, 255])

(width, height) = (800,600)

screen = pygame.display.set_mode((width, height))
screen.fill((0,255,0))
pygame.display.set_caption('HackU game')

pygame.display.flip()

MEAN_BOUNDARY_SIZE = 100.0
sum_boundary = []
sum_quad = None
mean_quad = None
mean_boundary = None
sum_boundary_count = 0

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

print "Calibration complete..."

fps = 2
t_frame = 1./fps
curr_frame_delay = 0
curr_frame_start = 0
skip_render = False

# if mean_boundary is not None and len(mean_boundary)==4:

while True:
    curr_frame_start = time.time()
    ret, frame = cap.read()

    #quad
    src_points = np.float32([mean_quad[0][0],mean_quad[1][0],mean_quad[2][0],mean_quad[3][0]])

    #800x600 things
    dst_points = np.float32([[800,0],[0,0],[0,600],[800,600]])
    perspectiveT = cv2.getPerspectiveTransform(src_points, dst_points)

    cropped_frame = cv2.warpPerspective(frame, perspectiveT, (800,600))
    screen.fill((np.random.random()*255,np.random.random()*255,np.random.random()*255))

    if not skip_render:
        pygame.display.flip()

        pygame_frame = surfarray.array3d(screen)
        pygame_frame = np.swapaxes(pygame_frame, 0, 1)
        pygame_frame = cv2.cvtColor(pygame_frame, cv2.COLOR_BGR2RGB)

        diff_frame = np.abs(cropped_frame-pygame_frame)
        gray_scale = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_scale, 127, 255, cv2.THRESH_BINARY)

        cv2.imshow('diff', thresh)
        cv2.imshow('cropped', cropped_frame)
        cv2.imshow('pygame', pygame_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    curr_frame_delay = time.time() - curr_frame_start
    if t_frame > curr_frame_delay:
        skip_render = False
        time.sleep(t_frame - curr_frame_delay)
    else:
        print("Update too slow\nOvershoot: %f" % (curr_frame_delay - t_frame))
        skip_render = True

