#!/usr/bin/env python

import cv2
import numpy as np
import pygame
from pygame import surfarray
import time
import math

pygame.init()
cap = cv2.VideoCapture(0)

FINAL_MIN = np.array([100, 200, 130])
FINAL_MAX = np.array([200, 255, 200])

(width, height) = (800,600)

screen = pygame.display.set_mode((width, height))
screen.fill((0,255,0))
pygame.display.set_caption('HackU game')

pygame.display.flip()

MEAN_BOUNDARY_SIZE = 50.0
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

    cv2.drawContours(frame, contours, -1, (255,0,0), 1)
    screenRect = None
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02* peri, True)

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

fps = 22
t_frame = 1./fps
curr_frame_delay = 0
curr_frame_start = 0
skip_render = False
execute = True
score = 0

kptrace = []

# if mean_boundary is not None and len(mean_boundary)==4:

myfont = pygame.font.Font(None, 60)

while True:
    ret, frame = cap.read()

    if execute:
        curr_frame_start = time.time()

        #quad
        src_points = np.float32([mean_quad[0][0],mean_quad[1][0],
                                 mean_quad[2][0],mean_quad[3][0]])

        #800x600 things
        dst_points = np.float32([[800,0],[0,0],[0,600],[800,600]])
        perspectiveT = cv2.getPerspectiveTransform(src_points, dst_points)

        cropped_frame = cv2.warpPerspective(frame, perspectiveT, (800,600))
        # cropped_frame = np.swapaxes(cropped_frame,0,1)
        # cropped_frame = cv2.resize(cropped_frame,(800,600),
        #             interpolation=cv2.INTER_CUBIC)
        # cropped_frame = cv2.flip(cropped_frame,0)
        color = (100,100,100)

        screen.fill((255, 255, 255))
        pygame.draw.line(screen,color,(200,300),(600,300),3)
        pygame.draw.line(screen,color,(400,100),(400,500),3)
        pygame.draw.circle(screen,color,(400,300),200,3)
        pygame.draw.circle(screen,(200,200,200),(400,300),100)
        if max_hit:
            pygame.draw.circle(screen, (0, 0, 255),
                               (int(max_hit.pt[0]),int(max_hit.pt[1])),
                               int(max_hit.size/2))
        label_full = myfont.render("%d" % 100, 1, color)
        screen.blit(label_full, (362.5, 275))

        label_1 = myfont.render("%d" % 40, 1, color)
        screen.blit(label_1, (275, 375))
        label_2 = myfont.render("%d" % 60, 1, color)
        screen.blit(label_2, (275, 175))
        label_3 = myfont.render("%d" % 20, 1, color)
        screen.blit(label_3, (475, 375))
        label_4 = myfont.render("%d" % 80, 1, color)
        screen.blit(label_4, (475, 175))

        label_score = myfont.render("SCORE: %d" % score, 1, color)
        screen.blit(label_score, (480, 50))


        # render
        pygame.display.flip()

        pygame_frame = surfarray.array3d(screen)
        pygame_frame = np.swapaxes(pygame_frame, 0, 1)
        pygame_frame = cv2.cvtColor(pygame_frame, cv2.COLOR_BGR2RGB)

        last_pygame_frame = pygame_frame

        hsv_crop = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        hsv_pgam = cv2.cvtColor(pygame_frame, cv2.COLOR_BGR2HSV)
        diff_frame = np.abs(hsv_crop-hsv_pgam)
        thresh = cv2.inRange(diff_frame, np.array([0,100,100],np.uint8),
                    np.array([255,255,255],np.uint8))
        thresh = 255-thresh

        blob_params = cv2.SimpleBlobDetector_Params()

        blob_params.filterByCircularity = False
        blob_params.filterByConvexity = False
        blob_params.filterByInertia = True
        blob_params.minInertiaRatio = 0.2

        detector = cv2.SimpleBlobDetector_create(blob_params)
        keypoints = detector.detect(thresh)

        max_hit = None

        if len(keypoints) > 0:
            kptrace.extend(keypoints)
            nfcount = 0
        else:
            nfcount = nfcount + 1
            if nfcount>10:
                nfcount = 0
                if len(kptrace) > 0:
                    max_hit = max(kptrace, key=lambda x:x.size)
                    kptrace = []
                    print("%s - %d" % (max_hit.pt, max_hit.size))
                    angle = math.degrees(math.atan2(max_hit.pt[1]-300.,max_hit.pt[0]-400.))
                    angle = (angle+360.)%360.
                    distance = math.sqrt((max_hit.pt[1]-300.0)**2+(max_hit.pt[0]-400.0)**2)
                    if distance<100:
                        score = score+100
                    elif distance<200:
                        if angle>0 and angle<90:
                            score = score + 20
                        elif angle>90 and angle<180:
                            score = score + 40
                        elif angle>180 and angle<270:
                            score = score + 60
                        elif angle>270 and angle<360:
                            score = score + 80
                        else:
                            score = score + 0

                    else:
                        score = score + 0



        im_with_keypoints = cv2.drawKeypoints(cropped_frame, kptrace,
                    np.array([]), (0,0,255),
                    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # im2, contours, hierarchy = cv2.findContours(thresh,
        #                             cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(cropped_frame, contours, -1, (0,0,255),3)


        cv2.imshow('diff', diff_frame)
        cv2.imshow('thresh', thresh)
        cv2.imshow('cropped', im_with_keypoints)
        #cv2.imshow('pygame', pygame_frame)

    cv2key = cv2.waitKey(1)
    if cv2key & 0xFF == ord('q'):
        break
    if cv2key & 0xFF == ord('c'):
        kptrace = []
        score = 0

        # fn = (fn+1)%10

    curr_frame_delay = time.time() - curr_frame_start
    if t_frame > curr_frame_delay:
        execute = False
        # time.sleep(t_frame - curr_frame_delay)
    else:
        execute = True
        # print("Update too slow\nOvershoot: %f" % (curr_frame_delay - t_frame))

