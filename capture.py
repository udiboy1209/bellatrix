#!/usr/bin/env python

import cv2
import numpy as np
import pygame

cap = cv2.VideoCapture(0)

cv2.namedWindow('video')
cv2.namedWindow('cropped')
FINAL_MIN = np.array([0, 210, 0])
FINAL_MAX = np.array([255, 255, 255])

# (width, height) = (1300,700)

# screen = pygame.display.set_mode((width, height))
# screen.fill((0,255,0))
# pygame.display.set_caption('HackU game')

# pygame.display.flip()

while True:
    ret, frame = cap.read()

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

#     print(screenRect[0][0])
#     if screenRect:
#         minX = min(screenRect[0][0][0],screenRect[1][0][0])
#         maxX = min(screenRect[2][0][0],screenRect[3][0][0])
#         minY = max(screenRect[0][0][1],screenRect[3][0][1])
#         maxY = max(screenRect[2][0][1],screenRect[1][0][1])

#         cropped_frame = frame[minX:maxX, minY:maxY]
#         cv2.imshow('cropped', cropped_frame)

    cv2.drawContours(frame, [screenRect], -1, (0,0,255), 3)

    cv2.imshow('video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
